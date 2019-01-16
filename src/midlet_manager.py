#!/usr/bin/python

from sys import exit
import argparse
from time import sleep
from wm.wmodule import WirelessModule
from wm import wmident, wmfile, wmmidlet
import logging


def connect(port, baudrate, timeout):
    try:
        print "Opening %s with %dbps..." % (args.port, args.baudrate)
        wmodule = WirelessModule(port=port, baudrate=baudrate, timeout=timeout)
        print "Done."
    except Exception as _:
        raise Exception("Error while connecting serial interface")
    if not wmident.is_responding(wmodule):
        wmodule.close()
        raise Exception("The module is not responding")
    return wmodule


if __name__ == "__main__":
    ###### PARSE COMMAND LINE PARAMETERS ######
    parser = argparse.ArgumentParser(description='Single command tool for downloading, installing and starting Gemalto MIDlets')
    parser.add_argument("--src", help="path of file to send")
    parser.add_argument("--dst", help="requested path of file on FFS")
    parser.add_argument("-d", "--download", action="store_true", help="download JAD and corresponding JAR files")
    parser.add_argument("-i", "--install", action="store_true", help="install MIDlet from JAD after downloading")
    parser.add_argument("-s", "--start", action="store_true", help="start MIDlet from JAD after installation")
    parser.add_argument("-p", "--port")
    parser.add_argument("-jp", "--javapass", default="")
    parser.add_argument("-b", "--baudrate", type=int, default=115200)
    parser.add_argument("-t", "--timeout", type=int, default=5)
    parser.add_argument("-v", "--verbose", action="store_true")
    
    args = parser.parse_args()
    
    if args.verbose:
        logging.basicConfig(level=logging.DEBUG)
    
    if not (args.install or args.start or args.download) or args.port is None:
        parser.print_help()
        exit(0)
        
    # CONNECT
    try:
        wmodule = connect(args.port, args.baudrate, args.timeout)
        
        if args.download:
            src_jad = args.src
            dst_jad = args.dst
            src_jar = args.src[:-1]+'r'
            dst_jar = args.dst[:-1]+'r'
            print "Downloading "+src_jad+" file..."
            wmfile.download(wmodule, src_jad, dst_jad)
            print "Done."
            print "Downloading "+src_jar+" file..."
            wmfile.download(wmodule, src_jar, dst_jar)
            print "Done."
        
        if args.install or args.start:
            print "Stopping "+args.dst+" MIDlet..."
            if wmmidlet.stop(wmodule, args.dst, args.javapass):
                print "Done."
            else:
                print "Error!"
            
        if args.install:
            print "Installing "+args.dst+" MIDlet..."
            if wmmidlet.install(wmodule, args.dst, args.javapass):
                print "Done."
            else:
                print "Error!"
            
        if args.start:
            print "Starting " + args.dst + " MIDlet..."
            if wmmidlet.start(wmodule, args.dst, args.javapass):
                print "Done."
            else:
                print "Error!"
        
        print "Closing " + args.port + "..."
        wmodule.close()
        
        print "All done, bye!"
        exit(0)
            
    except Exception as e:
        print e.args[0]
        exit(1)
