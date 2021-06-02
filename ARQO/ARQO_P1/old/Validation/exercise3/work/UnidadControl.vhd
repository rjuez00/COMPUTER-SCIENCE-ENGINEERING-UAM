library IEEE;
use IEEE.std_logic_1164.ALL;
use IEEE.std_LOGIC_arith.ALL;
use IEEE.std_logic_signed.ALL;

entity UnidadControl is
	Port (
		OPCode : in  std_logic_vector (5 downto 0); -- OPCode of the instruction
		Funct : in std_logic_vector(5 downto 0); -- Funct of the instruction
		-- Signals for the PC
		Jump : out  std_logic;
		--RegToPC : out std_logic;
		Branch : out  std_logic;
		--PCToReg : out std_logic;
		-- Signals to the memory
		MemToReg : out  std_logic;
		MemWrite : out  std_logic;
		
		-- Sifnals for the ALU
		ALUSrc : out  std_logic;
		ALUControl : out  std_logic_vector (2 downto 0);
		ExtCero : out std_logic;
		
		-- Signals for the GPR
		RegWrite : out  std_logic;
		RegDest : out  std_logic
        );
end UnidadControl;

architecture practice4 of UnidadControl is
	begin
	process (OPCode, Funct)
		begin
				case OPCode is
					when "100011"=> MemToReg <= '1'; --lw
									MemWrite <= '0';
									Branch <= '0';
									ALUControl <= "010";
									ALUSrc <= '1';
									RegDest <= '0';
									RegWrite <= '1';
									ExtCero <= '0';
									Jump <= '0';
								 
					when "101011"=> MemToReg <= '0'; --sw
									MemWrite <= '1';
									Branch <= '0';
									ALUControl <= "010";
									ALUSrc <= '1';
									RegDest <= '0';
									RegWrite <= '0';
									ExtCero <= '0';
									Jump <= '0';
			
					when "000100"=> MemToReg <= '0'; --beq
									MemWrite <= '0';
									Branch <= '1';
									ALUControl <= "110";
									ALUSrc <= '0';
									RegDest <= '0';
									RegWrite <= '0';
									ExtCero <= '0';
									Jump <= '0';			
			
					when "001000"=> MemToReg <= '0'; --addi NOT SURE bc im the table we did can be wrong and bc *********
									MemWrite <= '0';
									Branch <= '0';
									ALUControl <= "010";
									ALUSrc <= '1';
									RegDest <= '0';
									RegWrite <= '1';
									ExtCero <= '0';
									Jump <= '0';	
									
					when "001100"=> MemToReg <= '0'; --andi NOT USRE EITHER bc the saem
									MemWrite <= '0';
									Branch <= '0';
									Jump <= '0';
									ALUControl <= "000";
									ALUSrc <= '1';
									RegDest <= '0';
									RegWrite <= '1';
									ExtCero <= '1';
									
					when "001101"=> MemToReg <= '0'; --ori NOT USRE EITHER bc the saem
									MemWrite <= '0';
									Branch <= '0';
									Jump <= '0';
									ALUControl <= "001";
									ALUSrc <= '1';
									RegDest <= '0';
									RegWrite <= '1';
									ExtCero <= '1';
			
					when "001010"=> MemToReg <= '0'; --slti NOT SURE AGAIIIN SORRY FOR BEING SUCH A PICE OF SHIIIIIIT bc the sameeee
									MemWrite <= '0';
									Branch <= '0';
									ALUControl <= "111";
									ALUSrc <= '1';
									RegDest <= '0';
									RegWrite <= '1';
									ExtCero <= '0';
									Jump <= '0';	
			
					when "000010"=> MemToReg <= '0'; --J
									MemWrite <= '0';
									Branch <= '0';
									ALUControl <= "000";
									ALUSrc <= '0';
									RegDest <= '0';
									RegWrite <= '0';
									ExtCero <= '0';
									Jump <= '1';
								 
					when "000000" =>
						case funct is
							when "100100" => MemToReg <= '0'; 
											 MemWrite <= '0';
											 Branch <= '0';
											 ALUControl <= "000";
											 ALUSrc <= '0';
											 RegDest <= '1';
											 RegWrite <= '1';
											 ExtCero <= '0';
											 Jump <= '0';
											 
							when "100000" => MemToReg <= '0'; 
											 MemWrite <= '0';
											 Branch <= '0';
											 ALUControl <= "010";
											 ALUSrc <= '0';
											 RegDest <= '1';
											 RegWrite <= '1';
											 ExtCero <= '0';
											 Jump <= '0';
											 
							when "100010" => MemToReg <= '0'; 
											 MemWrite <= '0';
											 Branch <= '0';
											 ALUControl <= "110";
											 ALUSrc <= '0';
											 RegDest <= '1';
											 RegWrite <= '1';
											 ExtCero <= '0';
											 Jump <= '0';
											 
							when "100111" => MemToReg <= '0';
											 MemWrite <= '0';
											 Branch <= '0';
											 ALUControl <= "101";
											 ALUSrc <= '0';
											 RegDest <= '1';
											 RegWrite <= '1';
											 ExtCero <= '0';
											 Jump <= '0';
											 
							when "100101" => MemToReg <= '0'; 
											 MemWrite <= '0';
											 Branch <= '0';
											 ALUControl <= "001";
											 ALUSrc <= '0';
											 RegDest <= '1';
											 RegWrite <= '1';
											 ExtCero <= '0';
											 Jump <= '0';
											 
							when "101010" => MemToReg <= '0'; 
											 MemWrite <= '0';
											 Branch <= '0';
											 ALUControl <= "111";
											 ALUSrc <= '0';
											 RegDest <= '1';
											 RegWrite <= '1';
											 ExtCero <= '0';
											 Jump <= '0';
											 
							when others =>   MemToReg <= '0';
											 MemWrite <= '0';
											 Branch <= '0';
											 ALUControl <= "000";
											 ALUSrc <= '0';
											 RegDest <= '0';
											 RegWrite <= '0';
											 ExtCero <= '0';
											 Jump <= '0';
						end case;
						
					when others =>   MemToReg <= '0'; 
											 MemWrite <= '0';
											 Branch <= '0';
											 ALUControl <= "000";
											 ALUSrc <= '0';
											 RegDest <= '0';
											 RegWrite <= '0';
											 ExtCero <= '0';
											 Jump <= '0';
				end case;
		end process;
end practice4;
			
			
			
			
			
			
			
			
			
			
			