'''
Created on 22.12.2016

@author: jedzej
'''

import serial
import logging
from time import sleep

logger = logging.getLogger("WMODULE")

class WirelessModule(serial.Serial):
    '''
    Connects with Cinterion Wireless Module via com port
    Please check serial.Serial reference for general usage
    '''

    def call(self, cmd):
        ''' Calls AT command '''
        logger.debug("Sending command: " + cmd)
        sleep(0.1) 
        self.write( cmd + "\r")
    
    
    def read_till(self, *ans):
        '''
        Reads data line by line from the module until one of *ans is met
            returns tuple of (<output>, <matched_ans>)
            usage example: wm.read_till("OK","ERROR")            
        '''
        logger.debug("Waiting for: " + str(ans)) 
        outbuf = ""
        while(True):
            line = self.readline()
            outbuf += line
            if line == "":
                return (outbuf , None)
                
            for a in ans:
                #if a in line:
                if line.startswith(a):
                    logger.debug("\"" + a + "\" matched to \"" + repr(outbuf) + "\"") 
                    return (outbuf , a)
        
        
    def call_waiting(self, cmd, *ans):
        '''
        Call AT command and wait for one of *ans parameters
            returns tuple of (<output>, <matched_ans>)
            usage example: wm.read_till("ATI","OK","ERROR")
        '''
        self.call(cmd)
        return self.read_till(*ans)
                    
        
    def transmit(self, instream):
        ''' Transmit data from instream to the module until EOF is met '''
        #print instream.read()
        logger.debug("Transmitting data")
        self.write(instream.read())
        return
