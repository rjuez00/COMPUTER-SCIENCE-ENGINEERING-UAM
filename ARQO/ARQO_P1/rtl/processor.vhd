--------------------------------------------------------------------------------
-- Procesador MIPS con pipeline curso Arquitectura 2020-2021
--
-- (INCLUIR AQUI LA INFORMACION SOBRE LOS AUTORES)
--
--------------------------------------------------------------------------------

library ieee;
use ieee.std_logic_1164.all;
use ieee.std_logic_unsigned.all;

entity processor is
   port(
      Clk         : in  std_logic; -- Reloj activo en flanco subida
      Reset       : in  std_logic; -- Reset asincrono activo nivel alto
      -- Instruction memory
      IAddr      : out std_logic_vector(31 downto 0); -- Direccion Instr
      IDataIn    : in  std_logic_vector(31 downto 0); -- Instruccion leida
      -- Data memory
      DAddr      : out std_logic_vector(31 downto 0); -- Direccion
      DRdEn      : out std_logic;                     -- Habilitacion lectura
      DWrEn      : out std_logic;                     -- Habilitacion escritura
      DDataOut   : out std_logic_vector(31 downto 0); -- Dato escrito
      DDataIn    : in  std_logic_vector(31 downto 0)  -- Dato leido
   );
end processor;

architecture rtl of processor is

  component alu
    port(
      OpA : in std_logic_vector (31 downto 0);
      OpB : in std_logic_vector (31 downto 0);
      Control : in std_logic_vector (3 downto 0);
      Result : out std_logic_vector (31 downto 0);
      Zflag : out std_logic
    );
  end component;

  component reg_bank
     port (
        Clk   : in std_logic; -- Reloj activo en flanco de subida
        Reset : in std_logic; -- Reset as�ncrono a nivel alto
        A1    : in std_logic_vector(4 downto 0);   -- Direcci�n para el puerto Rd1
        Rd1   : out std_logic_vector(31 downto 0); -- Dato del puerto Rd1
        A2    : in std_logic_vector(4 downto 0);   -- Direcci�n para el puerto Rd2
        Rd2   : out std_logic_vector(31 downto 0); -- Dato del puerto Rd2
        A3    : in std_logic_vector(4 downto 0);   -- Direcci�n para el puerto Wd3
        Wd3   : in std_logic_vector(31 downto 0);  -- Dato de entrada Wd3
        We3   : in std_logic -- Habilitaci�n de la escritura de Wd3
     );
  end component reg_bank;

  component control_unit
     port (
        -- Entrada = codigo de operacion en la instruccion:
        OpCode   : in  std_logic_vector (5 downto 0);
        -- Seniales para el PC
        Branch   : out  std_logic; -- 1 = Ejecutandose instruccion branch
        -- Seniales relativas a la memoria
        MemToReg : out  std_logic; -- 1 = Escribir en registro la salida de la mem.
        MemWrite : out  std_logic; -- Escribir la memoria
        MemRead  : out  std_logic; -- Leer la memoria
        -- Seniales para la ALU
        ALUSrc   : out  std_logic;                     -- 0 = oper.B es registro, 1 = es valor inm.
        ALUOp    : out  std_logic_vector (2 downto 0); -- Tipo operacion para control de la ALU
        -- Seniales para el GPR
        RegWrite : out  std_logic; -- 1=Escribir registro
        RegDst   : out  std_logic;  -- 0=Reg. destino es rt, 1=rd
        Jump : out  std_logic -- 1 = Cambia el PC
     );
  end component;

  component alu_control is
   port (
      -- Entradas:
      ALUOp  : in std_logic_vector (2 downto 0); -- Codigo de control desde la unidad de control
      Funct  : in std_logic_vector (5 downto 0); -- Campo "funct" de la instruccion
      -- Salida de control para la ALU:
      ALUControl : out std_logic_vector (3 downto 0) -- Define operacion a ejecutar por la ALU
   );
  end component alu_control;

  signal Alu_Op2      : std_logic_vector(31 downto 0);
  signal Zflag_EX    : std_logic;
  signal Zflag_MEM : std_logic;
  signal AluControl   : std_logic_vector(3 downto 0);
  signal reg_RD_data  : std_logic_vector(31 downto 0);
  signal reg_RD_EX       : std_logic_vector(4 downto 0);
  signal reg_RD_MEM       : std_logic_vector(4 downto 0);
  signal reg_RD_WB       : std_logic_vector(4 downto 0);


  signal enable_IF_ID   : std_logic;
  signal enable_ID_EX   : std_logic;
  signal enable_EX_MEM   : std_logic;
  signal enable_MEM_WB   : std_logic;

  signal PC_next        : std_logic_vector(31 downto 0);
  signal PC_reg         : std_logic_vector(31 downto 0);
  signal pcmas4_ID       : std_logic_vector(31 downto 0);
  signal pcmas4_IF       : std_logic_vector(31 downto 0);
  signal pcmas4_EX       : std_logic_vector(31 downto 0);

  signal Instruction2016_EX    : std_logic_vector(4 downto 0);
  signal Instruction1511_EX    : std_logic_vector(4 downto 0);
  signal Instruction_ID        : std_logic_vector(31 downto 0);
  signal Instruction           : std_logic_vector(31 downto 0);
  signal Instruction_IF       : std_logic_vector(31 downto 0); -- La instrucción desde lamem de instr
  signal reg_RS_ID, reg_RT_ID : std_logic_vector(31 downto 0);
  signal reg_RS_EX, reg_RT_EX : std_logic_vector(31 downto 0);

  signal dataIn_Mem_WB     : std_logic_vector(31 downto 0); --From Data Memory
  signal dataIn_Mem_MEM     : std_logic_vector(31 downto 0); --From Data Memory
  signal Addr_Branch_MEM    : std_logic_vector(31 downto 0);
  signal Addr_Branch_EX    : std_logic_vector(31 downto 0);
  signal DDataOut_MEM    : std_logic_vector(31 downto 0);

  signal Ctrl_Jump_MEM, Ctrl_MemWrite_MEM, Ctrl_MemRead_MEM, Ctrl_MemToReg_MEM,Ctrl_Branch_MEM, Ctrl_RegWrite_MEM : std_logic;
  signal Ctrl_MemToReg_WB, Ctrl_RegWrite_WB : std_logic;
  signal Ctrl_Jump_ID, Ctrl_Branch_ID, Ctrl_MemWrite_ID, Ctrl_MemRead_ID,  Ctrl_ALUSrc_ID, Ctrl_RegDest_ID, Ctrl_MemToReg_ID, Ctrl_RegWrite_ID : std_logic;
  signal Ctrl_Jump_EX, Ctrl_Branch_EX, Ctrl_MemWrite_EX, Ctrl_MemRead_EX,  Ctrl_ALUSrc_EX, Ctrl_RegDest_EX, Ctrl_MemToReg_EX, Ctrl_RegWrite_EX : std_logic;
  --signal Ctrl_Jump, Ctrl_Branch, Ctrl_MemWrite, Ctrl_MemRead,  Ctrl_ALUSrc, Ctrl_RegDest, Ctrl_MemToReg, Ctrl_RegWrite : std_logic;
  signal Ctrl_ALUOP_ID     : std_logic_vector(2 downto 0);
  signal Ctrl_ALUOP_EX     : std_logic_vector(2 downto 0);

  signal Addr_Jump_ID      : std_logic_vector(31 downto 0);
  signal Addr_Jump_MEM      : std_logic_vector(31 downto 0);
  signal Addr_Jump_EX      : std_logic_vector(31 downto 0);
  signal Addr_Jump_dest : std_logic_vector(31 downto 0);
  signal desition_Jump     : std_logic;
  signal Alu_Res_EX        : std_logic_vector(31 downto 0);
  signal Alu_Res_MEM        : std_logic_vector(31 downto 0);
  signal Alu_Res_WB         : std_logic_vector(31 downto 0);

  signal Inm_ext_ID        : std_logic_vector(31 downto 0);
  signal Inm_ext_EX        : std_logic_vector(31 downto 0);

  
begin
  Instruction <= Instruction_IF;
  PC_next <= Addr_Jump_dest when desition_Jump = '1' else PCmas4_IF;

  PC_counter: process(clk, reset,
                    enable_IF_ID, pcmas4_IF, Instruction_IF) --IF/ID
  begin
    if reset = '1' then
      pcmas4_ID <= (others=>'0');
      Instruction_ID <= (others=>'0');
    elsif rising_edge(clk) and enable_IF_ID='1' then
      pcmas4_ID <= pcmas4_IF;
      Instruction_ID <= Instruction_IF;
    end if;
  end process;


  
  PC_counter2: process(clk, reset,
                      Instruction_ID, reg_RS_ID, reg_RT_ID, Ctrl_Branch_ID, Ctrl_MemWrite_ID, Ctrl_MemRead_ID,  
                      Ctrl_ALUSrc_ID,  Ctrl_RegDest_ID, Ctrl_MemToReg_ID, Ctrl_RegWrite_ID, enable_ID_EX, Inm_ext_ID,
                      Ctrl_ALUOP_ID, pcmas4_ID, Addr_Jump_ID, Ctrl_Jump_ID) --ID/EX
  begin
    if reset = '1' then
      Inm_ext_EX <= (others => '0');
      Instruction1511_EX <= (others => '0');
      Instruction2016_EX <= (others => '0');
      pcmas4_EX <= (others => '0');
      Addr_Jump_EX <= (others => '0');
      
      reg_RS_EX <= (others => '0');
      reg_RT_EX <= (others => '0');
      
      Ctrl_Jump_EX <= '0';
      Ctrl_Branch_EX <= '0';
      Ctrl_MemWrite_EX <= '0';
      Ctrl_MemRead_EX <= '0';
      Ctrl_ALUSrc_EX <= '0';
      Ctrl_RegDest_EX <= '0';
      Ctrl_MemToReg_EX <= '0';
      Ctrl_RegWrite_EX <= '0';
      Ctrl_ALUOP_EX <= (others => '0');

    elsif rising_edge(clk) and enable_ID_EX='1' then
      Inm_ext_EX <= Inm_ext_ID;
      Instruction2016_EX <= Instruction_ID(20 downto 16);
      Instruction1511_EX <= Instruction_ID(15 downto 11);
      pcmas4_EX <= pcmas4_ID;
      Addr_Jump_EX <= Addr_Jump_ID;

      reg_RS_EX <= reg_RS_ID;
      reg_RT_EX <= reg_RT_ID;

      Ctrl_Jump_EX <= Ctrl_Jump_ID; --pasa de fase
      Ctrl_Branch_EX <= Ctrl_Branch_ID; --pasa de fase
      Ctrl_MemWrite_EX <= Ctrl_MemWrite_ID; --pasa de fase
      Ctrl_MemRead_EX <= Ctrl_MemRead_ID; --pasa de fase
      Ctrl_ALUSrc_EX <= Ctrl_ALUSrc_ID; --done
      Ctrl_RegDest_EX <= Ctrl_RegDest_ID;--done
      Ctrl_MemToReg_EX <= Ctrl_MemToReg_ID; --pasa de fase
      Ctrl_RegWrite_EX <= Ctrl_RegWrite_ID; --pasa de fase
      Ctrl_ALUOP_EX <= Ctrl_ALUOP_ID; --done
    end if;
  end process;
  


  


  PC_counter3: process(clk,reset,
                      enable_EX_MEM, Addr_Jump_EX, reg_RD_EX, Ctrl_Jump_EX,
                      Ctrl_Branch_EX, Ctrl_MemWrite_EX, Ctrl_MemRead_EX, 
                      Ctrl_MemToReg_EX, Ctrl_RegWrite_EX, Alu_Res_EX,
                      Addr_Branch_EX, Zflag_EX, reg_RT_EX) --EX/MEM
  begin
    if reset = '1' then
      reg_RD_MEM <= (others => '0');
      Addr_Jump_MEM <= (others => '0');
      
      Ctrl_Jump_MEM <= '0';
      Ctrl_MemWrite_MEM <= '0';
      Ctrl_MemRead_MEM <= '0';
      Ctrl_MemToReg_MEM <= '0';
      Ctrl_RegWrite_MEM <= '0';
      Ctrl_Branch_MEM <= '0';
      
      Zflag_MEM <= '0';
      
      Alu_Res_MEM <= (others => '0');
      Addr_Branch_MEM <= (others => '0');
      Ctrl_Jump_MEM <= '0';
      DDataOut_MEM <= (others => '0');
      
    elsif rising_edge(clk) and enable_EX_MEM='1' then --not finished
      Addr_Jump_MEM <= Addr_Jump_EX;
      reg_RD_MEM <= reg_RD_EX;

      Ctrl_Jump_MEM <= Ctrl_Jump_EX; --no pasa de fase
      Ctrl_Branch_MEM <= Ctrl_Branch_EX; --no pasa de fase
      Ctrl_MemWrite_MEM <= Ctrl_MemWrite_EX;--TODO // NO PASA DE FASE
      Ctrl_MemRead_MEM <= Ctrl_MemRead_EX; --TODO // NO PASA DE FASE
      Ctrl_MemToReg_MEM <= Ctrl_MemToReg_EX; --pasa de fase
      Ctrl_RegWrite_MEM <= Ctrl_RegWrite_EX; --pasa de fase

      Alu_Res_MEM <= Alu_Res_EX;
      Addr_Branch_MEM <= Addr_Branch_EX;
      Zflag_MEM <= Zflag_EX;
      DDataOut_MEM <= reg_RT_EX; 
    end if;
  end process;
    
    
  PC_counter4: process(clk, reset,
                      enable_MEM_WB, Ctrl_MemToReg_MEM, Ctrl_RegWrite_MEM, Alu_Res_MEM, reg_RD_MEM, dataIn_Mem_MEM) --MEM/WB
  begin
    if reset = '1' then
      Ctrl_RegWrite_WB <= '0';
      Ctrl_MemToReg_WB <= '0';
      Alu_Res_WB <= (others => '0');
      reg_RD_WB <= (others => '0');
      dataIn_Mem_WB <= (others => '0');
      
    elsif rising_edge(clk) and enable_MEM_WB='1' then
      Ctrl_MemToReg_WB <= Ctrl_MemToReg_MEM; --pasa de fase
      Ctrl_RegWrite_WB <= Ctrl_RegWrite_MEM;--pasa de fase
      Alu_Res_WB <= Alu_Res_MEM;
      reg_RD_WB <= reg_RD_MEM;
      dataIn_Mem_WB <= dataIn_Mem_MEM;
    end if;  
  end process;

  enable_IF_ID <= '1';
  enable_ID_EX <= '1';
  enable_EX_MEM <= '1';
  enable_MEM_WB <= '1';

  

  PC_reg_proc: process(Clk, Reset)
  begin
    if Reset = '1' then
      PC_reg <= (others => '0');
    elsif rising_edge(Clk) then
      PC_reg <= PC_next;
    end if;
  end process;
   


  pcmas4_IF    <= PC_reg + 4;
  IAddr       <= PC_reg;
  Instruction_IF <= IDataIn;
  
  --?? <= ?? when Instruction = "000000000000000000000000000000000"

  RegsMIPS : reg_bank
  port map (
    Clk   => Clk,
    Reset => Reset,
    A1    => Instruction_ID(25 downto 21),
    Rd1   => reg_RS_ID,
    A2    => Instruction_ID(20 downto 16),
    Rd2   => reg_RT_ID,
    A3    => reg_RD_wb,
    Wd3   => reg_RD_data,
    We3   => Ctrl_RegWrite_WB
  );

  UnidadControl : control_unit
  port map(
    OpCode   => Instruction_ID(31 downto 26),
    -- Señales para el PC
    --Jump   => CONTROL_JUMP,
    Branch   => Ctrl_Branch_ID,
    -- Señales para la memoria
    MemToReg => Ctrl_MemToReg_ID,
    MemWrite => Ctrl_MemWrite_ID,
    MemRead  => Ctrl_MemRead_ID,
    -- Señales para la ALU
    ALUSrc   => Ctrl_ALUSrc_ID,
    ALUOP    => Ctrl_ALUOP_ID,
    -- Señales para el GPR
    RegWrite => Ctrl_RegWrite_ID,
    RegDst   => Ctrl_RegDest_ID,
    Jump => Ctrl_Jump_ID
  );

  Inm_ext_ID        <= x"FFFF" & Instruction_ID(15 downto 0) when Instruction_ID(15)='1' else
                    x"0000" & Instruction_ID(15 downto 0);
  Addr_Jump_ID      <= PCmas4_ID(31 downto 28) & Instruction_ID(25 downto 0) & "00";
  Addr_Branch_EX    <= PCmas4_EX + ( Inm_ext_EX(29 downto 0) & "00");

  --Ctrl_Jump      <= '0'; --nunca salto incondicional

  desition_Jump  <= Ctrl_Jump_MEM or (Ctrl_Branch_MEM and ZFlag_MEM); 
  Addr_Jump_dest <= Addr_Jump_MEM   when Ctrl_Jump_MEM='1' else
                    Addr_Branch_MEM when Ctrl_Branch_MEM='1' else
                    (others =>'0');

  Alu_control_i: alu_control
  port map(
    -- Entradas:
    ALUOp  => Ctrl_ALUOP_EX, -- Codigo de control desde la unidad de control
    Funct  => Inm_ext_EX (5 downto 0), -- Campo "funct" de la instruccion
    -- Salida de control para la ALU:
    ALUControl => AluControl -- Define operacion a ejecutar por la ALU
  );

  Alu_MIPS : alu
  port map (
    OpA     => reg_RS_EX,
    OpB     => Alu_Op2,
    Control => AluControl,
    Result  => Alu_Res_EX,
    Zflag   => Zflag_EX
  );

  Alu_Op2    <= reg_RT_EX when Ctrl_ALUSrc_EX = '0' else Inm_ext_EX;
  reg_RD_EX     <= Instruction2016_EX when Ctrl_RegDest_EX = '0' else Instruction1511_EX;

  DAddr      <= Alu_Res_MEM;
  DDataOut   <= DDataOut_MEM;
  DWrEn      <= Ctrl_MemWrite_MEM;
  dRdEn      <= Ctrl_MemRead_MEM;
  dataIn_Mem_MEM <= DDataIn;

  reg_RD_data <= dataIn_Mem_WB when Ctrl_MemToReg_WB = '1' else Alu_Res_WB;

end architecture;
