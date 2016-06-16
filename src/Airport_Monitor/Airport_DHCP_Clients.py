#!/usr/bin/python
"""
Munin plugin to monitor active DHCP leases from an Apple Airport 
Express/Extreme or a Time Capsule.


To use this plugin:
place this python script (along with 'Airport_Monitor.py') to
/etc/munin/plugins folder.

this will create a virtual host in munin for the airport base station and 
produce graphs for:
* number of active DHCP leases
"""
import sys
import os
try:
    import Airport_Monitor
except ImportError:
    print """ERROR: Unable to import Airport_Monitor.py.
Please make sure that file 'Airport_Monitor.py' is in the same directory.'"""
    sys.exit(-3)


def main():
    R0 = Airport_Monitor.Airport('10.0.1.1', 2, 'public')

    if len(sys.argv) > 1 and sys.argv[1] == 'config':
        """ Munin has requested configuration parameters for generating graphs
         from this script. Provide graph related configuration"""
        print "graph_category Network_Monitor:%s" % (R0.Get_Hostname())
        print "graph_args --base 1000 -l 0 -r --lower-limit 0"
        print "graph_title DHCP leases"
        print "graph_vlabel number"
        print "graph_info This graph shows the number of active leases for %s"%\
                                                             (R0.Get_Hostname())
        print "graph_scale no"
        print "dhcpclients.label leases"
        sys.exit(0)
    else:
        """This function fetches metadata about wireless clients if needed, then
        displays whatever values have been requested"""
        print "dhcpclients.value %s" % R0.Get_NumDHCPClients()


if __name__ == '__main__':
    main()

