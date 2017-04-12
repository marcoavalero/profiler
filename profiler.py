#!/usr/bin/python

# Most of this script was borrowed from: 
# http://askubuntu.com/questions/56266/how-to-log-memory-and-cpu-usage-of-an-application
# Credits to the users muru and Stefano Palazzo

import time
import string
import sys
import commands
import signal
import logging
from logging.handlers import TimedRotatingFileHandler

def signal_term_handler(signal, frame):
    print 'Exiting'
    sys.exit(0)
 

def get_cpumem(pid):
    d = [i for i in commands.getoutput("ps auxwww").split("\n")
        if i.split()[1] == str(pid)]
    return (float(d[0].split()[2]), float(d[0].split()[3]), float(d[0].split()[5])/1024) if d else None

if __name__ == '__main__':
    signal.signal(signal.SIGTERM, signal_term_handler)
    if not (len(sys.argv) >= 2 and len(sys.argv) <= 4) or not all(i in string.digits for i in sys.argv[1]):
        print("usage: %s PID" % sys.argv[0])
        exit(2)

    pid  = sys.argv[1]
    freq = int(sys.argv[2])

    logDir = '/tmp/profiler/'
    if len(sys.argv) == 4:
        name = str(sys.argv[3])
        logName = 'pid-'+str(pid)+'-'+name+'.log'
    else:
        name = str(sys.argv[1])
        logName = 'pid-'+str(pid)+'.log'

    logger = logging.getLogger(name)
    hdlr = TimedRotatingFileHandler(logDir+logName, when="W0", interval=1, backupCount=2)
    formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
    hdlr.setFormatter(formatter)
    logger.addHandler(hdlr) 
    logger.setLevel(logging.INFO)
    logger.info("Starting")

    try:
        while True:
            x = get_cpumem(sys.argv[1])
            if not x:
                logger.info("Process does not exist or died. Exiting...")
                exit(1)
            logger.info("%%CPU %%MEM MEM(MB): %.2f %.2f %.2f"%x)
            time.sleep(freq)
    except KeyboardInterrupt:
        print
        exit(0)
