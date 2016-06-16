Usage Instructions
=======================================

=============================================
Usage Instructions for Airport Monitor Tool
=============================================

If you have followed the installation instructions properly, You should be able check out Munin-generated graphs by typing: http://localhost on your web browser.
Graphs should be displayed under: Airport_Monitor:*Ruter Name* category.
Make sure that Airport Extreme/Express BasStation's SNMP Parametrs are:

        | ``IP Address: 10.0.1.1``
        | ``Version:    2``
        | ``Community:  public``


=============================================
Usage Instructions for Packet Sniffer Tool
=============================================

**NOTE**
    | No space is allowed between the option and its value. 
    | Valid: --srcport=2344
    | Invalid: --srcport = 2344

^^^^^^^^^^^^^^^
Arguments
^^^^^^^^^^^^^^^
Usage: ``./Packet_Sniffer.py --if=<interface_name>``    Start capturing all packets on interface_name.

Required Arguments:
       | --if=<interface_name>   Network Interface Name

Optional Arguments:
            | --filter=<option> - Filter incoming packets
            | --filter=tcp  -  Show only TCP Packets
            | --filter=udp  -  Show only UDP Packets
            | --filter=icmp  -  Show only ICMP Packets
            | --filter=arp  -  Show only ARP Packets
            | --filter=ethernet  -  Show Ethernet layer related info of all packets

       | --srcport=<port_no> - Show packets having particualr Source Port No.

       | --dstport=<port_no> - Show packets having particualr Destination Port No.

       | --srcip=<ip_addr> - Show packets having particualr Source IP Address   

       | --dstip=<ip_addr> - Show packets having particualr Destination IP Address

       | --prom=<option> - 'yes'/'no' value specifying whether to put the interface into promiscuous mode. 
      
       | --help  - Print this Info                    

Example Usage:
Show all TCP packets with promiscuous mode:

        | ``./Packet_Sniffer.py --if=eth0 --filter=tcp --prom=yes``
 
Show all packets sent by 192.168.0.4 : 

        | ``./Packet_Sniffer.py --if=eth0 --srcip=192.168.0.4``

Show all packets sent by 192.168.0.4 using port no. 5050:

        | ``./Packet_Sniffer.py --if=eth0 --srcip=192.168.0.4 --srcport=5050``

Packets are captured and corresponding data is displayed on terminal.
This data is dumped on terminal at very high rate. 
Please enable scroll bar of your terminal in order to check all captured packets.

        | ``Press Ctrl^C to exit the program.``
