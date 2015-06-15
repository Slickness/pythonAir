#!/usr/local/bin/python
from subprocess import *
import threading
import os
import time

def wirelessInterface():
    #returns a list of adapters and monitor mode adapters
    command = 'iwconfig'
    proc = Popen(args=command,stdout=PIPE,shell=False)
    iface = ''
    monitors = []
    adapters= []
    for line in proc.communicate()[0].split('\n'):
        if len(line) == 0: continue
        if ord(line[0]) != 32: #doesnt start with spaces
            iface=line[:line.find(' ')] #is the interface
        if line.find('Mode:Monitor') != -1:
            monitors.append(iface)
        else:
            if iface in adapters: continue
            else:
                adapters.append(iface)
    call(['clear'])
    #print monitors
    #print adapters
    return adapters,monitors

def PutMonitorMode(adapter):
    #takes an adapter name to put it into monitor mode
    command = "airmon-ng start wlan0" 
    proc = Popen(['airmon-ng','start',adapter],shell=False)

def StartScanningAP(mon):

    temp = "tempFile"
    with open(os.devnull, 'wb') as DN:
        Popen(['airodump-ng','-w',temp,'--output-format', 'csv','--ignore-negative-one', mon[0]],stdout= DN,stderr=DN,shell=False)
  
def stopScanning():
    #x = Popen(["ps"," aux",' |', 'grep', 'airodump-ng -w tempFile --output-format csv --ignore-negative-one mon0'],stdout=PIPE)
    x = Popen(["ps","aux"],stdout=PIPE)
    x2= Popen(["grep","airodump-ng -w tempFile --output-format csv --ignore-negative-one mon0"],stdin=x.stdout,stdout=PIPE)
    for line in x2.communicate()[0].split('\n'):
        print line



    #print x2.communicate()[0]
if __name__ == "__main__":
    adapters,mons = wirelessInterface()
    if len(mons) == 0:
        PutMonitorMode('wlan0')
    print "test"
    adapters,mons = wirelessInterface()
    print mons
    StartScanningAP(mons)

    time.sleep(10)
    stopScanning() 
