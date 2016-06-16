Project Summary
===============
I have described the project in detail below:

-------------------
Summary
-------------------

    Network Usage Monitoring is one of the important aspects of Network Management. Being a user (and great fan) of Apple Airport Extreme as well as Airport Express devices, I always wanted to develop some automated software, that will log all the traffic/packets of my home network along with some other valuable information like current status of router, no. of active nodes, incoming/outgoing traffic at each and every interface of the router etc. 

    Apart from logging this network data, I also aim to present the logged data using GUI extensions in Python or some third party stats/logs/graphing/monitoring tools like Munin, Nagios, mrtg etc. Today, remote Configuration Management of Networking Devices is performed via the Simple Network Management Protocol (SNMP).  

    SNMP uses Management Information Bases (MIBs) as it’s management information model (e.g., data models). This project aims to 1) Build a Packet Sniffing application in Python, that will capture all the packets, parse/decode the packets at different networks levels and present it (perhaps with nice GUI if possible), and 2) Fetch the other valuable information from Airport Express/Extreme routers via SNMP, and log them or feed them to third party monitoring tools.

-------------------
Scope
-------------------

    First, a packet sniffing application code will be developed using any existing open source Python modules, which will be platform independent. This Packet Sniffer will log all the incoming/outgoing packets, and parse/decode the packets at different level to show specific data (like Type of the Packet: Ethernet, TCP, IP etc., Encapsulated data at different levels: MAC Address, IP Address, TCP/UDP Port No. Etc.). 

    Second, an emphasis will be placed on utilizing a SNMP protocol to query the Airport Express/Extreme routers for statistics including the no. of wireless clients active in the network. The data fetched from these routers will be fed to Python GUI graphing libraries or monitoring tools such as Munin or MRTG.  In order to get valuable information from these routers; first we have to study the MIB structure and Oids for Airport devices. 

    I assume that Apple Inc. Further makes this available as open information; the project may also be expanded to develop a GUI, which will be able to change the configuration parameters of the Airport devices available in the network. Moreover, the network usage data fetched from the routers may be monitored for network usage bandwidth, and periodic interrupts/alarms may be generated to inform the network administrator about over usage/network traffic at any particular interface in the network.
