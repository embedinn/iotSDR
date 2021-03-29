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
use IEEE.NUMERIC_STD.ALL;
use ieee.std_logic_unsigned.all;


entity at86rf215_tx_interface is

    generic (WIDTH  : integer := 32);
    
    Port (  clk_64          : in std_logic; -- DDR clk
            reset_n         : in std_logic;
            sample_rate     : in std_logic_vector(2 downto 0);
            IQsample_in     : in std_logic_vector(WIDTH-1 downto 0);
            valid           : in std_logic;
            ready           : out std_logic;
            txd_24         : out STD_LOGIC_VECTOR (1 downto 0) := "00"-- 2bit tx data for lvds signaling 
    );
    
 end at86rf215_tx_interface;

architecture Behavioral of at86rf215_tx_interface is

    constant SAMPLE_RANGE : natural := 14;
    constant I_SYNC       : std_logic_vector(1 downto 0) := "01";
    constant Q_SYNC       : std_logic_vector(1 downto 0) := "10";
    
    signal clkCounter     : std_logic_vector(3 downto 0) := (others => '0');
    signal clk32          : std_logic := '0';
    signal clk04          : std_logic := '0';
    
    signal ready_s        : std_logic := '1';
    signal ready_init_s   : std_logic := '0';
    signal sample_en      : std_logic := '0';
    signal serialize_en   : std_logic := '0';
    signal serialize_done : std_logic := '0';
    signal hold_en        : std_logic := '0';
    signal hold_done      : std_logic := '0';
    
    signal ramp           : std_logic_vector(SAMPLE_RANGE-1 downto 0) :=  (others => '0');
    signal IQSample       : std_logic_vector(31 downto 0) :=  (others => '0');
    signal IQSample_next  : std_logic_vector(31 downto 0) :=  (others => '0');
    signal txd_24_s         : STD_LOGIC_VECTOR (1 downto 0) := "00";-- 2bit tx data for lvds signaling 

    type states is (idle,serialize,hold);
    signal state_now, state_next : states := idle;
    
    signal sample_reg, sample_next : std_logic_vector(WIDTH-1 downto 0);
    
    signal bitIndex_next    : std_logic_vector(3 downto 0) := "0000";
    signal bitIndex_reg     : std_logic_vector(3 downto 0) := "0000";
    signal hold_counter     : std_logic_vector(5 downto 0) := "000000";
    signal hold_counter_reg : std_logic_vector(5 downto 0) := "000000";
    signal hold_samples     : std_logic_vector(5 downto 0) := "000000";
        
    -- AT86RF215 Source --
    -- LVDS clk is 64Mhz, the seria data is received at DDR formate
    -- 2 bits @ 64Mhz at Single data rate formate
    -- 16bit I and Q at 4Mhz => 4Msamples/sec 
    
    --IQ samples serial bits sequence
    --Bit[31:30]     Bit[29:16]   Bit[15:14]    Bit[13:0]
    --I_SYNC=0b10    I_DATA[13:0] Q_SYNC=0b01   Q_DATA[13:0]
    

begin

    sample_rate_select : process(sample_rate)
    begin
        case sample_rate is
            when "000" =>
                hold_samples <= std_logic_vector(to_unsigned(15,hold_samples'length));
                
            when others =>
                hold_samples <= std_logic_vector(to_unsigned(30,hold_samples'length));    
        
        end case;
    
    end process;

    fsm_init : process (clk_64, reset_n)
    begin
        if reset_n = '0' then
            state_now     <= idle;
        
        elsif rising_edge(clk_64) then
            state_now     <= state_next;
        end if;
            
    end process;
    

    fsm_transition: process (state_now,serialize_done,hold_done,ready_s,valid,IQsample_in)
    begin
        
          serialize_en  <= '0';
          hold_en       <= '0';
          sample_en     <= '0';
          
 
        case state_now is 
        
            -- wait for valid sample in
            when idle =>
                if valid = '1' and  ready_s = '1' then
                    sample_en     <= '1';
                    state_next    <= serialize;
                    ready_init_s  <= '1';
                else
                    state_next    <= idle; 
                    sample_en     <= '0';   
                end if;
          
            -- 2bit sent serialize          
            when serialize =>
                sample_en     <= '0';

                if (serialize_done = '1')  then
                     state_next    <= hold;
                     serialize_en  <= '0';
                      --ready_s      <= '0';
                else
                     serialize_en <= '1';
                     state_next   <= serialize;              
                     --ready_s      <= '0';

                end if;
                
            when hold => 
                --ready_s       <= '0';
                
                if (hold_done = '1')  then
                     state_next    <= idle;
                     --ready_s       <= '1';
                     hold_en       <= '0';                
                
                else
                     hold_en <= '1';
                     state_next   <= hold; 
                     --ready_s      <= '0';             
                
                end if;
            
            when others => null;
            
         end case;   
    end process;
    
    
    seq_signals : process (clk_64, reset_n)
    begin
        if reset_n = '0' then
            bitIndex_reg <= (others => '0');
        
        elsif rising_edge(clk_64) then
        
            --  Serialize state
            if(serialize_en = '1') then
                --
                if bitIndex_reg = 14 then
                    bitIndex_reg   <= (others => '0');
                    serialize_done <= '1';

                else
                    bitIndex_reg <= bitIndex_reg + 1;
                    serialize_done <= '0';
                
                end  if;
            else
                serialize_done <= '0';    
            
            end if;
            
            -- hold State
            if(hold_en = '1') then
            
            
                if hold_counter = 13 then
                    hold_counter <= (others => '0');
                    hold_done <= '1';
                else
                    hold_counter <= hold_counter + 1;
                    hold_done <= '0';
                
                end  if;
            else
                hold_done <= '0';    
            
            end if;
         end if;
            
    end process;
    
    outputs : process (clk_64, reset_n)
    begin
        if reset_n = '0' then

            sample_reg   <= (others => '0');  
            sample_next  <= (others => '0');  
        
        elsif rising_edge(clk_64) then
            if (sample_en = '1') then
                sample_next   <= I_SYNC & IQsample_in(31 downto 18) & 
                                 Q_SYNC & IQsample_in(15 downto 2);
            end if;
            
            if(serialize_en = '1') then
                sample_next   <= sample_next(29 downto 0) & "00";
                
            end if;
            
        
        end if;
        
        
    end process;    
        
    -- send last 2 bits (I_SYNC) first  
    txd_24_s <= "00" when (hold_en = '1' or hold_done = '1' or sample_en = '1') else sample_next(31 downto 30);
    txd_24 <= txd_24_s;
    
    ready  <= ready_s when (ready_init_s =  '0') else serialize_done;
    
end Behavioral;
