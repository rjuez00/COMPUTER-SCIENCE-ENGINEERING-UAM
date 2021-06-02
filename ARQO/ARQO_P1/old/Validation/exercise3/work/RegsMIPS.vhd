----------------------------------------------------------------------
-- File: RegsMIPS.vhd
-- Description: Register bank of the microprocessor MIPS
-- Date last modification: 2019-02-22

-- Authors: 
-- Sbuject: Sbuject: C.E. 1st grade
-- Laboratory group:
-- Theory group:
-- Task: 2
-- Exercise: 1
----------------------------------------------------------------------


library IEEE;
use IEEE.std_logic_1164.all;
use IEEE.std_logic_unsigned.all;
use IEEE.std_logic_arith.all;

entity RegsMIPS is
	port (
		Clk : in std_logic; -- Clock
		NRst : in std_logic; -- Asynchronous Reset in low level
		A1 : in std_logic_vector(4 downto 0); -- Address for the port Rd1
		Rd1 : out std_logic_vector(31 downto 0); -- Data of the port Rd1
		A2 : in std_logic_vector(4 downto 0); -- Address for the port Rd2
		Rd2 : out std_logic_vector(31 downto 0); -- Dataof the port Rd2
		A3 : in std_logic_vector(4 downto 0); -- Address for the port Wd3
		Wd3 : in std_logic_vector(31 downto 0); -- Input data Wd3
		We3 : in std_logic -- Enable of the register bank
	); 
end RegsMIPS;

architecture Practica of RegsMIPS is

	-- Type to store the registers
	type regs_t is array (0 to 31) of std_logic_vector(31 downto 0);
	
	-- This signal contains the registers. The access is as follow:
	-- regs(i) is the access to the register i, where i is an integer.
	-- To convert from std_logic_vector to integer it is necessary:
	-- conv_integer(slv), where slv is a std_logic_vector element.

	signal regs : regs_t;

begin  -- TASK


	process (NRst, Clk)
	begin
	 if NRst = '0' then
	   		for x in 0 to 31 loop
  			 regs(x) <= (others =>'0');
    			end loop;
	 else		
	 	if rising_edge(Clk) then
	   		if We3='1' and (A3 /= "00000") then
		    		regs(conv_integer(A3))<= Wd3;
			  end if;
	  end if;
		

  end if;
	end process;
	
  Rd1<=regs(conv_integer(A1));
Rd2<=regs(conv_integer(A2));
	------------------------------------------------------
	-- Writing of the register Wd
	------------------------------------------------------
	-- It is necessary to write the content of Wd3 in the register 
	-- pointed out by A3 when there is a rising edge of the clk 
	-- and the enable signal of writing We3 is active.
	-- The reset is asynchrnous. If the reset is active, all the registers
	-- are initialized to 0.
	


	------------------------------------------------------
	-- Reading of the register Rd1
	------------------------------------------------------
	-- It is necessary to read in Rd1 the register pointed out by A1. 
	-- The reading of R0 register, alwyas is 0.


	------------------------------------------------------
	-- Reading of the register Rd2
	------------------------------------------------------
	-- It is necessary to read in Rd2 the register pointed out by A2. 
	-- The reading of R0 register, alwyas is 0.
	

end Practica;

