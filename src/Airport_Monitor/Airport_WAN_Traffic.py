#!/usr/bin/python
#Author: Niket Shah
"""
Munin plugin to monitor WAN Traffic from an Apple Airport 
Express/Extreme or a Time Capsule.


To use this plugin:
place this python script (along with 'Airport_Monitor.py') to
/etc/munin/plugins folder.

this will create a virtual host in munin for the airport base station and 
produce graphs for:
* Internet Bandwidth Usage
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
    clients = None

    if len(sys.argv) > 1 and sys.argv[1] == 'config':
        """ Munin has requested configuration parameters for generating graphs
         from this script. Provide graph related configuration"""
        print "graph_category Network_Monitor:%s" % (R0.Get_Hostname())
        print "graph_args --base 1000"
        print "graph_title WAN traffic"
        print "graph_vlabel bits per second"
        print "graph_info This graph shows the incoming and outgoing traffic rate of WAN interface"
        print "in.label received"
        print "in.type DERIVE"
        print "in.draw AREA"
        print "in.min 0"
        print "in.cdef in,8,*"
        print "out.label sent"
        print "out.type DERIVE"
        print "out.draw LINE1"
        print "out.min 0"
        print "out.cdef out,8,*"
        sys.exit(0)
    else:
        """This function fetches metadata about wireless clients if needed, then
        displays whatever values have been requested"""
        print "in.value %s" % R0.Get_InOctets('vlan1')
        print "out.value %s" % R0.Get_OutOctets('vlan1')


if __name__ == '__main__':
    main()

