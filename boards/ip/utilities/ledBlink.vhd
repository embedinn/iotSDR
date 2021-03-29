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
 use IEEE.numeric_std.all;
 
 entity ledBlink is
    Port ( 
           refclk : in  std_logic;
           led : out std_logic
    );
 end ledBlink;
 
 architecture RTL of ledBlink is
    constant max_count : natural := 16368000;
    signal Rst : std_logic;
 begin

    Rst <= '0';
 
    -- 0 to max_count counter
    compteur : process(refclk, Rst)
        variable count : natural range 0 to max_count;
    begin
        if Rst = '1' then
            count := 0;
            led <= '1';
        elsif rising_edge(refclk) then
            if count < max_count/2 then
                count := count + 1;
                led <= '1';
            elsif count < max_count then
                led <= '0';
                count := count + 1;
            else
                led <= '1';
                count := 0;
            end if;
        end if;
    end process compteur; 
 end RTL;