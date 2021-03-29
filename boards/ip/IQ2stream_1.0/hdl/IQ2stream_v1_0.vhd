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

library ieee;
use ieee.std_logic_1164.all;
use ieee.numeric_std.all;
use ieee.std_logic_unsigned.all;

entity IQ2stream_v1_0 is
	generic (

		-- Parameters of Axi Master Bus Interface M00_AXIS
		C_M00_AXIS_TDATA_WIDTH	: integer	:= 32;
		SAMPLES_PER_BLOCK   	: integer	:= 128
	);
	port (
		enable_in         : in  std_logic;
        IQ_sample_in      : in  std_logic_vector(31 downto 0);
        valid_in          : in  std_logic;
        tlast_out         : out  std_logic;
        sample_no         : out std_logic_vector(15 downto 0);
        samplesPerBlock   : in  std_logic_vector(15 downto 0);

		-- Ports of Axi Master Bus Interface M00_AXIS
		m00_axis_aclk	  : in std_logic;
		m00_axis_aresetn  : in std_logic;
		m00_axis_tvalid	  : out std_logic;
		m00_axis_tdata	  : out std_logic_vector(C_M00_AXIS_TDATA_WIDTH-1 downto 0);
		m00_axis_tstrb	  : out std_logic_vector((C_M00_AXIS_TDATA_WIDTH/8)-1 downto 0);
		m00_axis_tlast	  : out std_logic;
		m00_axis_tready	  : in std_logic
	);
end IQ2stream_v1_0;

architecture arch_imp of IQ2stream_v1_0 is

	-- Total number of output data                                              
	--constant NUMBER_OF_OUTPUT_WORDS : integer := 8;                                   
	-- the number of input words and output words.                                    
	--constant depth : integer := NUMBER_OF_OUTPUT_WORDS;                               
    -- FIFO write pointer                                               
	--signal read_pointer : integer range 0 to SAMPLES_PER_BLOCK-1; 
	signal read_pointer : std_logic_vector(C_M00_AXIS_TDATA_WIDTH-1 downto 0); 
	
	signal tx_en	: std_logic := '1';
	--The master has issued all the streaming data stored in FIFO
	signal tx_done	: std_logic;
	signal validOut	: std_logic;
 	                                                       

begin


	                                                                  
                                                           
	-- axis_interface to axi_stream_data_fifo
	validOut         <= valid_in and m00_axis_tready and enable_in;
	m00_axis_tvalid  <= validOut;
	m00_axis_tlast   <= '1' when (read_pointer = samplesPerBlock-1) and validOut = '1' else '0';                     
	tlast_out        <= '1' when (read_pointer = samplesPerBlock-1) and validOut = '1' else '0';                     
    m00_axis_tdata   <= IQ_sample_in;
    m00_axis_tstrb   <= (others => '1');
    sample_no        <= read_pointer(15 downto 0);
    --sample_no      <= std_logic_vector(to_unsigned(read_pointer,sample_no'length));
	
	
	--read_pointer pointer

	process(m00_axis_aclk)                                                       
	begin                                                                            
	  if (rising_edge (m00_axis_aclk)) then                                            
	    if(m00_axis_aresetn = '0'or enable_in = '0') then                                                
	      read_pointer <= (others  =>  '0');                                                         
	      tx_done  <= '0';                                                           
	    else                                                                         
	      if (read_pointer <= samplesPerBlock-1) then                         
	        if (validOut = '1') then                                                    
	          -- read pointer is incremented after every read from the FIFO          
	          -- when FIFO read signal is enabled.                                   
	          read_pointer <= read_pointer + 1;                                      
	          tx_done <= '0';                                                        
	        end if;                                                                  
	      elsif (read_pointer = samplesPerBlock) then                         
	        -- tx_done is asserted when SAMPLES_PER_BLOCK numbers of streaming data
	        -- has been out. 
	        read_pointer <= (others  =>  '0');                                                        
	        tx_done <= '1';                                                          
	      end  if;                                                                   
	    end  if;                                                                     
	  end  if;                                                                        
	end process;              
	
end arch_imp;