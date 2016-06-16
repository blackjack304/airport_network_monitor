#!/usr/bin/python
#Author: Niket Shah
"""
Munin plugin to monitor number of connected wireless clients from an Apple Airport 
Express/Extreme or a Time Capsule.


To use this plugin:
place this python script (along with 'Airport_Monitor.py') to
/etc/munin/plugins folder.

this will create a virtual host in munin for the airport base station and 
produce graphs for:
* number of connected wireless clients
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
        print "graph_args -l 0 --lower-limit 0 --upper-limit 40"
        print "graph_title Wireless clients connected"
        print "graph_vlabel Number of clients"
        print "graph_info This graph shows the number of Wireless clients connected to %s" % (R0.Get_Hostname())
        print "graph_order clients"
        print "clients.warning 18"
        print "clients.critical 30"
        print "clients.label clients"
        sys.exit(0)
    else:
        """This function fetches metadata about wireless clients if needed, then
        displays whatever values have been requested"""
        print "clients.value %s" % R0.Get_NumClients()


if __name__ == '__main__':
    main()

