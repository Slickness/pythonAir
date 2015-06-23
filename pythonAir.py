#!/usr/local/bin/python
from subprocess import *
import threading
import os
import glob
import time
import csv
import codecs


def nonull(stream):
    for line in stream:
        yield line.replace('\x00', '')
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
    #command = "airmon-ng start wlan0"
    proc = Popen(['airmon-ng','start',adapter],shell=False)

def StartScanningAP(mon):

    temp = "tempFile"
    with open(os.devnull, 'wb') as DN:
        Popen(['airodump-ng','-w',temp,'--output-format', 'csv','--ignore-negative-one', mon],stdout= DN,stderr=DN,shell=False)
  
def stopScanning():
    #x = Popen(["ps"," aux",' |', 'grep', 'airodump-ng -w tempFile --output-format csv --ignore-negative-one mon0'],stdout=PIPE)

    time.sleep(5)
    x = Popen(["sudo","killall","airodump-ng"],stdout=PIPE)
    #x2= Popen(["grep","airodump-ng -w tempFile --output-format csv --ignore-negative-one mon0"],stdin=x.stdout,stdout=PIPE)
    #for line in x2.communicate()[0].split('\n'):
     #   print line
def stopMonitorMode(mon):
    Popen(['airmon-ng','stop',mon],shell=False)
    #print mon
def ViewScan(file):

    bssid = []
    clients = []
    lists = "b"

    with codecs.open(file,'rb', 'utf-8') as f:
        reader = csv.reader(nonull(f))
        for row in reader:
            if len(row) > 0:
                if row[0] == "Station MAC":
                    lists = "s"
                if lists == "b":
                    bssid.append(row)
                if lists == "s":
                    clients.append(row)
    del bssid[0]
    bssid2 = sorted(bssid,key=lambda APs: APs[8])
    return bssid2,clients
def getNewFile():
    # files = []
    # for file in glob.glob("tempFile-*.csv"):
    #
    #     files.append(file)
    # print files
    file = max(glob.iglob('tempFile-*.csv'), key=os.path.getctime)
    return file
    #print x2.communicate()[0]

if __name__ == "__main__":
    # adapters,mons = wirelessInterface()
    # if len(mons) == 0:
    #     PutMonitorMode('wlan0')
    # print "test"
    # adapters,mons = wirelessInterface()
    # print mons
    # StartScanningAP(mons)
    #
    #
    file = getNewFile()
    print file
    # if '\0' in open(file).read():
    #     print "you have null bytes in your input file"
    # else:
    #     print "you don't"
    # stopScanning()
    #
    bssid,clients = ViewScan("tempFile-01.csv")
    #print bssid
    #print clients
