--  Copyright (c) 2020, embedINN
--  All rights reserved.

--  Redistribution and use in source and binary forms, with or without
--  modification, are permitted provided that the following conditions are met:

--  1. Redistributions of source code must retain the above copyright notice, this
--     list of conditions and the following disclaimer.

--  2. Redistributions in binary form must reproduce the above copyright notice,
--     this list of conditions and the following disclaimer in the documentation
--     and/or other materials provided with the distribution.

--  3. Neither the name of the copyright holder nor the names of its
--     contributors may be used to endorse or promote products derived from
--     this software without specific prior written permission.

--  THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
--  AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
--  IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
--  DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE
--  FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
--  DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
--  SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
--  CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY,
--  OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
--  OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.


library IEEE;
use IEEE.STD_LOGIC_1164.ALL;
use IEEE.STD_LOGIC_UNSIGNED.ALL;
use IEEE.NUMERIC_STD.ALL;

library UNISIM;
use UNISIM.VComponents.all;

entity max2769_interface is
  Port (   
           enable        : in std_logic; 
           IQ_data_lsb   : out std_logic_vector(31 downto 0);
           IQ_data_msb   : out std_logic_vector(31 downto 0);
           IQ_valid      : out std_logic := '0';
           
           G_I0          : in  std_logic;
           G_I1          : in  std_logic;
           G_Q0          : in  std_logic;
           G_Q1          : in  std_logic;
           G_CLKOUT      : in  std_logic;
           
           G_ANT_FLG     : in  std_logic;
           G_LD          : in  std_logic;
           
           G_PGM         : out std_logic := '0';
           G_SHDN        : out std_logic := '1';
           G_IDLE        : out std_logic := '1'

  );
end max2769_interface;

architecture Behavioral of max2769_interface is


signal IQ_nibble_lsb    : std_logic_vector(3  downto 0);
signal IQ_nibble_msb    : std_logic_vector(3  downto 0);
signal IQ_word_msb      : std_logic_vector(31 downto 0);
signal IQ_word_lsb      : std_logic_vector(31 downto 0);
signal IQ_word_reg      : std_logic_vector(31 downto 0);
signal IQ_valid_s       : std_logic;

signal nibble_counter   : std_logic_vector(2  downto 0) := "000";
signal clk_16_386       : std_logic;


begin

    clk_16_386 <= G_CLKOUT;
    
    IQ_word_stream : process(clk_16_386)
    begin
        if(rising_edge(clk_16_386)) then
        
            IQ_nibble_lsb <=  G_Q1 & G_Q0 & G_I1 & G_I0;
            IQ_nibble_msb <=  G_I0 & G_I1 & G_Q0 & G_Q1;
            --IQ_nibble <=  '0' & nibble_counter;
            IQ_word_lsb   <=  IQ_nibble_lsb & IQ_word_lsb(31 downto 4);
            IQ_word_msb   <=  IQ_nibble_msb & IQ_word_lsb(31 downto 4);
            --IQ_word_msb   <=  IQ_word_msb(27 downto 0) & IQ_nibble;

            nibble_counter <= nibble_counter + 1; 
            
        end if;
    end process;
    
    IQ_data_out: process(clk_16_386)
    begin
    
        if(rising_edge(clk_16_386)) then
            if nibble_counter = "001" and enable = '1' then
                IQ_valid        <= '1';
                IQ_data_lsb         <= IQ_word_lsb;
                IQ_data_msb         <= IQ_word_msb;
            else
                IQ_valid        <= '0';
            end if;    
        end if;
    end process;

end Behavioral;
