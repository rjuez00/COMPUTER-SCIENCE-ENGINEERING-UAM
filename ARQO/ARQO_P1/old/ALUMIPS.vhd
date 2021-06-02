----------------------------------------------------------------------
-- File: ALUMIPS.vhd
-- Description: ALU of the microprocessor MIPS
-- Date last modification: 

-- Authors: 
-- Sbuject: Sbuject: C.E. 1st grade
-- Laboratory group:
-- Theory group:
-- Task: 2
-- Exercise: 2
----------------------------------------------------------------------


library IEEE;
use IEEE.std_logic_1164.ALL;
use IEEE.std_LOGIC_arith.ALL;
use IEEE.std_logic_signed.ALL;

entity ALUMIPS is
	Port (
		Op1 : in std_logic_vector (31 downto 0);
		Op2 : in std_logic_vector (31 downto 0);
		ALUControl : in std_logic_vector (2 downto 0);
		Res : out std_logic_vector (31 downto 0);
		Z : out std_logic
		);
end ALUMIPS;

architecture Practica of ALUMIPS is

signal blade : std_logic_vector (31 downto 0);


begin
	
	Res<=blade;
	
	process(ALUControl, Op1, Op2)
	begin
		Blade <=(others => '0');
		case ALUControl is
			when "010" => Blade <= Op1 + Op2;
			when "110" => Blade<= Op1 - Op2;
			when "000" => Blade <= Op1 and Op2;
			when "001" => Blade <= Op1 or Op2;
			when "101" => Blade <= Op1 nor Op2;
			when "111" => 
				if Op1(31) = Op2(31) then
					if Op1<Op2 then
						Blade <= X"00000001";
					else 
						Blade <=X"00000000";
					end if;
				--continue with other cases here
				elsif op1(31) /= Op2(31) then
					if op1(31) = '1' then
						Blade <= X"00000001";
					else 
						Blade <= X"00000000";
					end if;
				end if;
			when others => Blade <= X"00000000";
		end case;
		
	end process;
	
	z<= '1' when Blade=X"00000000" else '0';
	


end Practica;
