#!/usr/bin/env python
"""
Python Packet Sniffer tool.
Author: Niket Shah
This script requires pycap (http://pycap.sourceforge.net/) and libpcap to be installed on your machine.

Usage: ./Packet_Sniffer.py --if=<interface_name>    Start capturing all packets on interface_name.

Optional Flags:
       --filter=<option>    Filter incoming packets
            --filter=tcp    Show only TCP Packets
            --filter=udp    Show only UDP Packets
            --filter=icmp   Show only ICMP Packets
            --filter=arp    Show only ARP Packets
            --filter=ethernet   Show Ethernet layer related info of all packets

       --srcport=<port_no>     Show packets having particualr Source Port No.
       --dstport=<port_no>     Show packets having particualr Destination Port No.
       --srcip=<ip_addr>       Show packets having particualr Source IP Address   
       --dstip=<ip_addr>       Show packets having particualr Destination IP Address
       --prom=<option>         'yes'/'no' value specifying whether to put the interface into promiscuous mode.       
       --help                  Print this Info                    

Example Usage:
Show all TCP packets with promiscuous mode:
./Packet_Sniffer.py --if=eth0 --filter=tcp --prom=yes
 
Show all packets sent by 192.168.0.4 : 
./Packet_Sniffer.py --if=eth0 --srcip=192.168.0.4

Show all packets sent by 192.168.0.4 using port no. 5050:      
./Packet_Sniffer.py --if=eth0 --srcip=192.168.0.4 --srcport=5050 

Packets are captured and corresponding data is displayed on terminal.
This data is dumped on terminal at very high rate. 
Please enable scroll bar of your terminal in order to check all captured packets. 
Press Ctrl^C to exit the program.  
"""

import getopt
import socket
import sys
import select
import time
import os
import re
try:
    import libnet
except ImportError:
    print """ERROR: Unable to import libnet.
Please install the Python bindings for libnet.
On Debian/Ubuntu machines this package is named 'libnet-dev'"""
    sys.exit(-3)
from libnet.constants import *

try:
    import pycap.capture
    import pycap.constants
except ImportError:
    print """ERROR: Unable to import pycap.
Please install the Python bindings for libpcap and pycap."""
    sys.exit(-3)



ARP_CONSTANTS = {'1':'ARPOP_REQUEST', '2':'ARPOP_REPLY',\
 '3':'ARPOP_REVREQUEST', '4':'ARPOP_REVREPLY',\
 '8':'ARPOP_INVREQUEST', '9':'ARPOP_INVREPLY'}

ETH_CONSTANTS = {0x0002:'ETHERTYPE_PUP', 0x0008:'ETHERTYPE_IP',\
 0x0608:'ETHERTYPE_ARP', 0x3580:'ETHERTYPE_REVARP',\
 0x0081:'ETHERTYPE_VLAN', 0xdd86:'ETHERTYPE_IPV6',\
 0x0090:'ETHERTYPE_LOOPBACK'}

IP_CONSTANTS = {'1':'IPPROTO_ICMP', '2':'IPPROTO_IGMP',\
 '5':'IPPROTO_TCP', '17':'IPPROTO_UDP'}


def Valid_IP(IP_Addr):
    """THis function validates IP Address supplied by user"""
    if(len(IP_Addr.split('.')) != 4):
        return False
    try:
        socket.inet_aton(IP_Addr)
        return True
    except socket.error:
        return False


def Valid_MAC(mac):
    """THis function validates MAC Address supplied by user"""
    xs = '([a-fA-F0-9]{2}[:|\-]?){6}'
    a = re.compile(xs).search(mac)
    if a:
        return True
    else:
        return False

def usage():
    """Print some usage information about ourselves"""
    print __doc__
    sys.exit()


def clrscr():
	"""This function clears the screen according to the OS it is on."""
	if os.name == "posix":
		os.system('clear')
	else:
		os.system('CLS')


def List_Interfaces():
    """This function returns list of legal names of nw interfaces in this machine.
    Credits: E A Faisal (http://bit.ly/azfBwy)"""
    iface_list = []
    f = open('/proc/net/dev','r')
    ifacelist = f.read().split('\n') 
    f.close()

    # remove 2 lines header
    ifacelist.pop(0)
    ifacelist.pop(0)

    # loop to check each line
    for line in ifacelist:
        ifacedata = line.replace(' ','').split(':')
        # check the data have 2 elements
        if len(ifacedata) == 2:
            iface_list.append(ifacedata[0])
    return iface_list


class Packet_Capture(object):
    def __init__(self, Filter_List):
        self.Filter_List = dict(Filter_List)
        self.pcap = pycap.capture.capture(Filter_List['Interface'],\
                                                 promisc=Filter_List['Prom'])
        # Build Filter Query as per Arguments supplied by User
        Filter_Query = ""
        if Filter_List['Type'] == 'tcp':
            Filter_Query = Filter_Query + ' and (tcp)'
        if Filter_List['Type'] == 'udp':
            Filter_Query = Filter_Query + ' and (udp)'
        if Filter_List['Type'] == 'arp':
            Filter_Query = Filter_Query + ' and (arp)'
        if Filter_List['Type'] == 'icmp':
            Filter_Query = Filter_Query + ' and (icmp)'
        if Filter_List['Src_Port'] != '':
            Filter_Query = Filter_Query + ' and (src port %s)'%\
                                                    (Filter_List['Src_Port'])

        if Filter_List['Dst_Port'] != '':
            Filter_Query = Filter_Query + ' and (dst port %s)'%\
                                                    (Filter_List['Dst_Port'])

        if Filter_List['Src_IP'] != '':
            Filter_Query = Filter_Query + ' and (src %s)'%\
                                                    (Filter_List['Src_IP'])

        if Filter_List['Dst_IP'] != '':
            Filter_Query = Filter_Query + ' and (dst %s)'%\
                                                    (Filter_List['Dst_IP'])
  
        #print Filter_Query  
        self.pcap.filter(Filter_Query[5:])

    def Sniff_Packets(self):
        """ This function actually captures packets, and prints it on terminal"""
        packet = None
        while(1):
            if(packet != None):
                #print packet
                print "\n\n\t---------- Next Packet -----------"

                # Print Ethernet Level Information
                print "Source MAC Address:", packet[0].source
                print "Destination MAC Address:", packet[0].destination
                if ETH_CONSTANTS.has_key(packet[0].type):
                    print "Packet Type: ", ETH_CONSTANTS[packet[0].type]
                else:
                    print "Packet Type Constant: ", packet[0].type

                if self.Filter_List['Type'] == 'ethernet':
                    print "Raw Ethernet Layer Data: \n", packet[0].packet
                    packet=self.pcap.next()
                    continue
                
                # Print Additional Information (IP/ICMP/ARP)
                if packet[0].type == 8 and str(packet[1].protocol) not in ['0', '1']:
                    try:
                        print "Source IP Address:", packet[1].source
                        print "Destination IP Address:", packet[1].destination
                        if IP_CONSTANTS.has_key(str(packet[1].protocol)):
                            print "Protocol Type: ", IP_CONSTANTS[str(packet[1].protocol)]
                        else:
                            print "Protocol Type Constant: ", packet[1].protocol
                        print "Source Port:", packet[2].sourceport
                        print "Destination Port:", packet[2].destinationport
                        print "Data: \n", packet[3]
                    except (AttributeError, KeyError, pycap.capture.error):
                        pass
                elif packet[0].type == 1544:
                    try:
                        print "ARP Operation: ", ARP_CONSTANTS[str(packet[1].operation)]
                        print "ARP SourceHardware: ", packet[1].sourcehardware
                        print "ARP TargetHardware: ", packet[1].targethardware
                    except (AttributeError, KeyError, pycap.capture.error):
                        pass
                elif packet[0].type == 8 and packet[1].protocol == 1:
                    try:
                        print "ICMP Source: ", packet[1].source
                        print "ICMP Destination: ", packet[1].destination
                        print "ARP TimetoLive: ", packet[1].timetolive
                        print "ARP Protocol Constant: ", packet[1].protocol
                    except (AttributeError, KeyError, pycap.capture.error):
                        pass                   
                packet=self.pcap.next()
            else:
                packet=self.pcap.next()
                #raw_input("Press any key to continue")
             
        
        

def Get_Options(myargv):
    """Function to parse User Arguments and options."""
    try:            
        opt,args = getopt.getopt(myargv,"ho:v",['help', 'if=', 'filter=',\
                'srcport=', 'dstport=', 'mac=','srcip=', 'dstip=', 'prom='])
    except getopt.GetoptError, err:
        print str(err)
        usage()
        sys.exit(999)
    if len(opt) < 1:
        usage()
        
    My_Interface = List_Interfaces()[0]
    My_Type = ''
    My_Src_Port = ''
    My_Dst_Port = ''
    My_MAC = ''
    My_Src_IP = ''
    My_Dst_IP = ''
    My_Prom = False

    for option,value in opt:
        if option == "--if" and value.lower() in List_Interfaces():
            My_Interface=value.lower()
        elif option in "--filter" and value.lower() in ['tcp', 'udp', 'arp',\
                                                         'icmp', 'ethernet']:
            My_Type=value.lower()
        elif option in "--srcport" and int(value) in range (0,65536):
            My_Src_Port=value
        elif option in "--dstport" and value in range (0,65536):
            My_Dst_Port=value
        elif option in "--mac" and Valid_MAC(value) == True:
            My_MAC=value
        elif option in "--srcip" and Valid_IP(value) == True:
            My_Src_IP=value
        elif option in "--dstip" and Valid_IP(value) == True:
            My_Dst_IP=value
        elif option in "--prom" and value.lower() in ['yes', 'no']:
            if value.lower() == 'yes':
                My_Prom=True
            else:
               My_Prom=False 
        elif option in ("-h", "--help"):
            usage()
            sys.exit()
        else:
                    print "Unhandled value for: ", option
                    usage()

    return {'Interface':My_Interface, 'Type':My_Type, 'Src_Port':My_Src_Port,\
 'Dst_Port':My_Dst_Port,  'MAC':My_MAC, 'Src_IP':My_Src_IP, 'Dst_IP':My_Dst_IP,\
 'Prom':My_Prom}



def main():
    clrscr()
    optlist=[]
    optlist=Get_Options(sys.argv[1:])
    p = Packet_Capture(optlist)
    p.Sniff_Packets()

if __name__ == "__main__":
    main()
    
