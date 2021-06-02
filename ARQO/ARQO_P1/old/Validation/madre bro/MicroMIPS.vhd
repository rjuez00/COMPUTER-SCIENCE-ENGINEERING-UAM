----------------------------------------------------------------------
-- File: MicroMIPS.vhd
-- Description: Complete microprocessor and linking
-- Date last modification: 2019-04-10
-- Authors: Sofía Xiao Fernández and Rodrigo Juez
-- Sbuject: Sbuject: C.E. 1st grade
-- Laboratory group: 2191
-- Theory group: 219
-- Task: 4
-- Exercise: 3
----------------------------------------------------------------------



library IEEE;
use IEEE.std_logic_1164.ALL;
use IEEE.std_LOGIC_arith.ALL;
use IEEE.std_logic_unsigned.ALL;


entity MicroMIPS is
	--MEM[whaetever] means the memory that is modified with sw
	port (
		Clk : in std_logic; -- Clock
		NRst: in std_logic;
		-- this signal is cut into pieces to obtain the different registers, inmediates or jump address
		MemProgData: in std_logic_vector(31 downto 0); 
		-- the data obtained from the MEM[whatever]
		MemDataDataRead: in std_logic_vector(31 downto 0);
		-- enable for writing in the MEM[whatever]
		MemDataWe: out std_logic;
		--this is the PC normally is updated by 4 every clock
		MemProgAddr: out std_logic_vector(31 downto 0);
		-- THIS IS THE RESULT OF THE ALU and is also connected to the MEM[whatever] address
		MemDataAddr: out std_logic_vector(31 downto 0);
		-- this signal is the data to be written in the MEM[whatever]
		MemDataDataWrite: out std_logic_vector(31 downto 0)
	);
	end MicroMIPS;

architecture Practica of MicroMIPS is
	component UnidadControl
	port (
		OPCode : in  std_logic_vector (5 downto 0); -- OPCode of the instruction
		Funct : in std_logic_vector(5 downto 0); -- Funct of the instruction
		-- Signals for the PC
		Jump : out  std_logic;
		-- RegToPC : out std_logic;
		Branch : out  std_logic;
		-- PCToReg : out std_logic;
		-- Signals to the memory
		MemToReg : out  std_logic;
		MemWrite : out  std_logic;
		
		-- Signals for the ALU
		ALUSrc : out  std_logic;
		ALUControl : out  std_logic_vector (2 downto 0);
		ExtCero : out std_logic;
		
		-- Signals for the GPR
		RegWrite : out  std_logic;
		RegDest : out  std_logic
        );
	end component;

	component RegsMIPS
	port (
		Clk : in std_logic; -- Clock
		NRst : in std_logic; -- Asynchronous Reset in low level
		A1 : in std_logic_vector(4 downto 0); -- Address for the port Rd1
		Rd1 : out std_logic_vector(31 downto 0); -- Data of the port Rd1
		A2 : in std_logic_vector(4 downto 0); -- Address for the port Rd2; not used, recives any value
		Rd2 : out std_logic_vector(31 downto 0); -- Dataof the port Rd2; open
		A3 : in std_logic_vector(4 downto 0); -- Address for the port Wd3
		Wd3 : in std_logic_vector(31 downto 0); -- Input data Wd3
		We3 : in std_logic -- Enable of the register bank; always activated
	); 
	end component;
	
	component ALUMIPS
	port (
		Op1 : in std_logic_vector (31 downto 0);
		Op2 : in std_logic_vector (31 downto 0);
		ALUControl : in std_logic_vector (2 downto 0); -- 010
		Res : out std_logic_vector (31 downto 0);
		Z : out std_logic -- open 
		);
	end component;
	
	-- Declaration of auxiliary signal
		signal PC:  std_logic_vector(31 downto 0):=	(others => '0');
		signal PCSrc: std_logic;
		signal JUMP0AUX: std_logic_vector(31 downto 0);
		signal JUMP1AUX: std_logic_vector(31 downto 0);
		signal ExtSignoforsll: std_logic_vector(31 downto 0);
		signal signExtend: std_logic_vector(31 downto 0);
		signal MemProgAddrplus4: std_logic_vector(31 downto 0);
		signal ImmplusMemProgAddrplus4: std_logic_vector (31 downto 0);
		signal toPC: std_logic_vector(31 downto 0);

	--ALU
		signal Op1AUX: std_logic_vector(31 downto 0);
		signal Op2AUX: std_logic_vector(31 downto 0);
		signal ResAUX: std_logic_vector(31 downto 0);
		signal zAUX: std_logic;

	--Register Bank
		signal RegsA3AUX: std_logic_vector(4 downto 0);
		signal RegsWd3AUX: std_logic_vector(31 downto 0);
		-- this is because we cannot connect direct the output of the register to the ALU
		signal RD2AUX: std_logic_vector(31 downto 0);
		
	--UnidadControl
		signal JumpAUX:  std_logic;
		signal BranchAUX: std_logic;
		signal MemToRegAUX: std_logic;
		signal MemWriteAUX: std_logic;
		signal ALUSrcAUX: std_logic;
		signal ALUControlAUX: std_logic_vector(2 downto 0);
		signal ExtCeroAUX: std_logic;
		signal RegWriteAUX: std_logic;
		signal RegDestAUX: std_logic;

begin
	MemProgAddr<=PC;
	
	-- Instantiation of RegMIPS
		regs: RegsMIPS PORT MAP (
			Clk => Clk,
			NRst => NRst,
			
			A1 => MemProgData(25 downto 21),
			Rd1 => Op1AUX,
			
			A2 => MemProgData(20 downto 16),
			Rd2 => RD2AUX,
			
			A3 => RegsA3AUX,
			Wd3=> RegsWd3AUX,
			We3=> RegWriteAUX
			);
			
			
	-- Instantiation of ALUMIPS
		alu: ALUMIPS PORT MAP (
			Op1 => Op1AUX,
			Op2 => Op2AUX,
			ALUControl => ALUControlAUX,
			Res => ResAUX,
			Z => zAUX);
	
	
	-- Instation of UnidadControl
		ctrl: UnidadControl PORT MAP (
			OPCode => MemProgData(31 downto 26),
			Funct => MemProgData(5 downto 0),
			-- Signals for the PC
			Jump => JumpAUX,
			-- RegToPC : out std_logic;
			Branch => BranchAUX,
			-- Signals to the memory
			MemToReg => MemToRegAUX,
			MemWrite => MemWriteAUX,
			
			-- Signals for the ALU
			ALUSrc => ALUSrcAUX,
			ALUControl => ALUControlAUX,
			ExtCero => ExtCeroAUX,
			
			-- Signals for the GPR
			RegWrite => RegWriteAUX,
			RegDest => RegDestAUX);
	
			
	-- Separation of the Signals
	RegsA3AUX <= MemProgData(20 downto 16) when RegDestAUX = '0' else
				 MemProgData(15 downto 11);

	ExtSignoforsll(31 downto 18) <= (others=>MemProgData(15));
	ExtSignoforsll(17 downto 0) <= MemProgData(15 downto 0) & "00";

	RegsWd3AUX <= ResAUX when MemToRegAUX = '0' else
				 MemDataDataRead;
	
	Op2AUX <= RD2AUX when ALUSrcAux = '0' else
				   signExtend;
			   
	signExtend(31 downto 16) <= (others => '0') when ExtCeroAUX = '1' else 
								(others => MemProgData(15));
	signExtend(15 downto 0) <= MemProgData(15 downto 0);
	
	MemDataWe<=MemWriteAUX;
	MemDataAddr<=ResAUX;
	MemDataDataWrite<=RD2AUX;
	MemDataWe <= MemWriteAUX;

	--PC Parts
	PCSrc <= zAUX and BranchAUX;
	MemProgAddrplus4<=PC+4;
	ImmplusMemProgAddrplus4<=MemProgAddrplus4 + ExtSignoforsll;
	JUMP0AUX<= ImmplusMemProgAddrplus4 when PCSrc = '1' else
			   MemProgAddrplus4;
	   
    JUMP1AUX <= MemProgAddrplus4(31 downto 28) & MemProgData(25 downto 0) & "00";
	
	toPC<=JUMP0AUX when JumpAUX = '0' else
		  JUMP1AUX;


	process (Clk, nRst)
	begin
		if nRst = '0' then
			PC <= (others => '0');
		else
			if Clk = '1' and Clk'event then 
				PC<=toPC;
				
			end if;
		end if;


	end process;
		
	


end Practica;

