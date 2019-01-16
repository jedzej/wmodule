#!/usr/bin/python
import binascii
import logging
import os
logger = logging.getLogger("WMFILE")

def __crc32_from_file(filename):
    fhandle = open(filename, 'rb')
    crc = binascii.crc32(fhandle.read())
    fhandle.close()
    return crc


def download(wmodule, src_path, dst_path):
    # calling AT^SJDL and waiting for CONNECT answer

#        raise AttributeError("File " + src_path + " does not exist!") 
    file_size = str(os.stat(src_path).st_size)
    ans = wmodule.call_waiting("AT^SJDL=1,"+file_size+",\""+dst_path+"\"", "CONNECT","ERROR")
    if ans[1] != "CONNECT":
        raise IOError("Module does not respond!")
    
    # transmiting the content
    filestream = open(src_path, 'rb')
    wmodule.transmit(filestream)
    filestream.close()
    
    # check CRC
    response = wmodule.read_till("CRC32","ERROR")
    local_crc = ("0x%x" % (0xFFFFFFFF & __crc32_from_file(src_path)))
    ind = response[0].find("0x");
    remote_crc = response[0][ind:ind+10]
    logger.debug("CRC: local \"%s\", remote \"%s\"" % (local_crc, remote_crc))
    if local_crc not in remote_crc:
        raise ValueError("CRC mismatch!")
