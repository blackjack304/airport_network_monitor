#!/usr/bin/python
#Author: Niket Shah

"""
Top Level SNMP wrapper to fetch various items of data from an Apple Airport
Express/Extreme or a Time Capsule.

To use this wrapper: place this python script (along with all other plugins) to
/etc/munin/plugins folder.

This will create a virtual host in munin for the airport named 'myairport' and
produce graphs for:

* number of connected wireless clients
* number of active DHCP leases
* rate at which clients are connected (in Mb/s)
* signal quality of connected clients (in dB)
* noise level of connected clients (in dB)
* Wireless client's traffic
"""

import sys
import os
try:
    import netsnmp
except ImportError:
    print """ERROR: Unable to import netsnmp.
Please install the Python bindings for libsnmp.
On Debian/Ubuntu machines this package is named 'libsnmp-python'"""
    sys.exit(-3)

DEBUG=None


def dbg(text):
    """Print debugging log if DEBUG=1"""
    if DEBUG is not None:
        print "DEBUG: %s" % text


class Airport(object):
    """Main SNMP Wrapper class for Apple Airport Base Station Devices"""

    def __init__(self, ipaddress='10.0.1.1', version=2, community='public'):
        """Constructor for Router class"""
        self._snmp = netsnmp.Session(DestHost = ipaddress, \
        Version = version, Community = community)
        
        self.Interface_List = None   
        self.DHCP_Clients = None
        self.Wireless_Clients = None
    
        self.DHCP_Clients = self.Get_NumDHCPClients()
        self.Wireless_Clients = self.Get_NumClients()
        self.WAN_Interface_Index = self.Get_Interface_Index('vlan1')

    def Airport_Query(self, SNMP_Oid):
        """Simple snmpget, will return single value as per the specified Oid"""
        return self._snmp.get(netsnmp.VarList(netsnmp.Varbind(SNMP_Oid)))[0]


    def Get_Hostname(self):
        """Method to get hostname using SNMP"""
        return self.Airport_Query('.1.3.6.1.2.1.1.5.0')


    def Get_Contact(self):
        """Method to get contact name using SNMP"""
        return self.Airport_Query('.1.3.6.1.2.1.1.4.0')

    def Get_NumClients(self):
        """Returns the number of wireless clients connected to the Airport.
        To reduce SNMP traffic, it will query the Airport router only 
        for the first time."""
        wirelessNumberOID = '.1.3.6.1.4.1.63.501.3.2.1.0'
        if self.Wireless_Clients is None:
            self.Wireless_Clients = int(self.Airport_Query(wirelessNumberOID))

        dbg("Get_NumClients: found %d clients" % self.Wireless_Clients)
        return self.Wireless_Clients


    def Get_NumDHCPClients(self):
        """Returns the number of DHCP clients with currently active leases. 
        To reduce SNMP traffic, it will query the Airport router only 
        for the first time."""
        dhcpNumberOID = '.1.3.6.1.4.1.63.501.3.3.1.0'
        if self.DHCP_Clients is None:
            self.DHCP_Clients = int(self.Airport_Query(dhcpNumberOID))

        dbg("Get_NumDHCPClients: found %d clients" % self.DHCP_Clients)
        return self.DHCP_Clients


    def Get_Interface_Index(self, intfc):
        """Returns the index of the particular interface of the Airport.
        Accepts Legal Interface Name (as reported by Airport Interface List).
        To reduce SNMP traffic, it will query the Airport router for 
        Interface List, only for the first time."""

        iFaceNames = '.1.3.6.1.2.1.2.2.1.2'
        Idx = 1 #Default Index to return
        if self.Interface_List is None:
            self.Interface_List = list(self._snmp.walk\
                                (netsnmp.VarList(netsnmp.Varbind(iFaceNames))))
            dbg("Get_Interface_Index: interfaces: %s" % self.Interface_List)
        try:
            Idx = self.Interface_List.index(intfc) + 1
        except ValueError:
            dbg("ERROR: Unable to find interface %s" % intfc)
            print "ERROR: Unable to find interface %s" % intfc
            print self.Interface_List
            sys.exit(-3)

        dbg("Get_Interface_Index: found %s at index: %d" % (intfc,Idx))
        return Idx


    def Get_InOctets(self, intf):
        """Returns the number of octets of inbound traffic on particular interface.
         Accepts Legal Interface Name (as reported by Airport Interface List)."""
        iFaceOctets = '.1.3.6.1.2.1.2.2.1.10.%s' % self.Get_Interface_Index(intf)
        return int(self.Airport_Query(iFaceOctets))


    def Get_OutOctets(self, intf):
        """Returns the number of octets of outbound traffic on particular interface.
        Accepts Legal Interface Name (as reported by Airport Interface List)."""
        iFaceOctets = '.1.3.6.1.2.1.2.2.1.16.%s' % self.Get_Interface_Index(intf)
        return int(self.Airport_Query(iFaceOctets))


    def Get_WanSpeed(self):
        """Returns the speed of the WAN interface"""
        ifSpeed = ".1.3.6.1.2.1.2.2.1.5.%s" % self.WAN_Interface_Index
        try:
            wanSpeed = int(self.Airport_Query(ifSpeed))
        except:
            dbg("Get_WanSpeed: Unable to probe for data, defaultint to 1000000000")
            wanSpeed = 1000000000
        return wanSpeed


    def Get_Data(self):
        """Returns a dictionary populated with all of the wireless clients and 
        their other parameters"""
        wirelessClientTableOID = '.1.3.6.1.4.1.63.501.3.2.2.1'

        numClients = self.Get_NumClients()

        if numClients == 0:
            dbg("Get_Data: 0 clients found!")
            sys.exit(0)

        dbg("Get_Data: polling SNMP for client table")
        clientTable = self._snmp.walk(netsnmp.VarList\
                                    (netsnmp.Varbind(wirelessClientTableOID)))
        clients = tableToDict(clientTable, numClients)
        return clients


def tableToDict(table, num):
    """The netsnmp snmpwalk gives all the data related to wireless clients,
    but it is not formatted well.This function converts the snmpwalk data into
    a structured dictionary, so that we can easily index/access different 
    parameters for each client. The associated value will be a dictionary 
    containing the information available
    about the client:
        * type        - 1 = sta, 2 = wds
        * rates       - Wi-Fi Datarate supported by client interface
        * time        - Client Up Time
        * lastrefresh - time since the client last refreshed
        * signal      - Wi-Fi signal strength reported by the client (or -1)
        * noise       - dB noise level reported by the client (or -1)
        * rate        - Mb/s Wi-Fi Datarate when client registered with Airport
        * rx          - number of octets received by the client
        * tx          - number of octets transmitted by the client
        * rxerr       - number of error packets received by the client
        * txerr       - number of error packets transmitted by the client
    """
    table = list(table)
    clients = []
    clientTable = {}

    # Get all MAC Addresses
    i = num
    while i > 0:
        data = table.pop(0)
        clients.append(data)
        clientTable[data] = {}
        dbg("tableToDict: found client '%s'" % data)
        i = i - 1

    CMDS=['type', 'rates', 'time', 'lastrefresh', 'signal', 'noise', 'rate',\
                                                'rx', 'tx', 'rxerr', 'txerr']

    # Use MAC Address as key, and fill up the dictionary
    for cmd in CMDS:
        i = 0
        while i < num:
            data = table.pop(0)
            clientTable[clients[i]][cmd] = data
            dbg("tableToDict: %s['%s'] = %s" % (clients[i], cmd, data))
            i = i + 1

    return clientTable

