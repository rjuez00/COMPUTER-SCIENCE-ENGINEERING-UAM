----------------------------------------------------------------------
-- File: MemProgVectores.vhd
-- Description: Template for the prorammemory MIPS
-- Date last modification: 2019-03-29

-- Authors: Sofía Martínez (2019), Alberto Sánchez (2012-2018), Ángel de Castro (2010-2015)
-- Sbuject: Sbuject: C.E. 1st grade
-- Laboratory group:
-- Theory group:
-- Task: 4
-- Exercise: 3
----------------------------------------------------------------------


library IEEE;
use IEEE.std_logic_1164.ALL;
use IEEE.std_LOGIC_arith.ALL;
use IEEE.std_logic_unsigned.ALL;

entity MemProgVectores is
	port (
		MemProgAddr : in std_logic_vector(31 downto 0); -- Address of the program memory
		MemProgData : out std_logic_vector(31 downto 0) -- Operation code
	);
end MemProgVectores;

architecture Simple of MemProgVectores is

begin

	LecturaMemProg: process(MemProgAddr)
	begin
		-- The memory gives back a value for each address.
		-- These values are the program codes for each instruction,
		-- which are located in its address.
		case MemProgAddr is
			when X"00000000" => MemProgData <= X"8c0f2000";
			when X"00000004" => MemProgData <= X"000f8020";
			when X"00000008" => MemProgData <= X"020f8020";
			when X"0000000C" => MemProgData <= X"020f8020";
			when X"00000010" => MemProgData <= X"020f8020";
			when X"00000014" => MemProgData <= X"20080000";
			when X"00000018" => MemProgData <= X"0110982a";
			when X"0000001C" => MemProgData <= X"1260000a";
			when X"00000020" => MemProgData <= X"8d112004";
			when X"00000024" => MemProgData <= X"8d12201c";
			when X"00000028" => MemProgData <= X"0012c820";
			when X"0000002C" => MemProgData <= X"0332c820";
			when X"00000030" => MemProgData <= X"0332c820";
			when X"00000034" => MemProgData <= X"0332c820";
			when X"00000038" => MemProgData <= X"02399820";
			when X"0000003C" => MemProgData <= X"ad132034";
			when X"00000040" => MemProgData <= X"21080004";
			when X"00000044" => MemProgData <= X"08000006";
			when X"00000048" => MemProgData <= X"08000012";

			when others => MemProgData <= X"00000000"; -- Rest of empty memory
		end case;
	end process LecturaMemProg;

end Simple;

