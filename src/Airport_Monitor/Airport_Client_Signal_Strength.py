#!/usr/bin/python
#Author: Niket Shah
"""
Munin plugin to monitor signal quality of connected clients from an Apple Airport 
Express/Extreme or a Time Capsule.


To use this plugin:
place this python script (along with 'Airport_Monitor.py') to
/etc/munin/plugins folder.

this will create a virtual host in munin for the airport base station and 
produce graphs for:

* signal quality of connected clients (in dB)
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
        print "graph_args -l 0 --lower-limit -100 --upper-limit 0"
        print "graph_title Wireless Client's Signal Strength"
        print "graph_vlabel dBm Signal"
        print "graph_info This graph shows the wireless client's signal strength"
        print "graph_scale no"

        clients = R0.Get_Data()
        for client in clients:
            print "MAC_%s.label %s" % (client, client)
        sys.exit(0)
    else:
        """This function fetches metadata about wireless clients if needed, then
        displays whatever values have been requested"""
        clients = R0.Get_Data()
        for client in clients:
            print "MAC_%s.value %s" % (client, clients[client]['signal'])


if __name__ == '__main__':
    main()

