#!/usr/bin/python
#Author: Niket Shah
"""
Munin plugin to monitor wireless client's traffic stats from an Apple Airport 
Express/Extreme or a Time Capsule.


To use this plugin:
place this python script (along with 'Airport_Monitor.py') to
/etc/munin/plugins folder.

this will create a virtual host in munin for the airport base station and 
produce graphs for:
* wireless client's traffic stats
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
        print "graph_args --base 1000"
        print "graph_title Wirless Client's traffic"
        print "graph_vlabel bits per second"
        print "graph_info This graph shows traffic for the each Wireless Client Interface (Only if supported by client)"

        clients = R0.Get_Data()
        for client in clients:
            if int(clients[client]['rx']) > -1 and int(clients[client]['tx']) > -1:
                print "MAC_%s_send.label sent by %s" % (client, client)
                #print "MAC_%s_send.type DERIVE" % (client)
                #print "MAC_%s_send.draw LINE1" % (client)
                #print "MAC_%s_send.min 0" % (client)
                #print "MAC_%s_send.cdef MAC_%s_send,8,*" % (client, client)

                print "MAC_%s_recv.label received by %s" % (client, client)
                #print "MAC_%s_recv.type DERIVE" % (client)
                #print "MAC_%s_recv.draw AREA" % (client)
                #print "MAC_%s_recv.min 0" % (client)
                #print "MAC_%s_recv.cdef MAC_%s_recv,8,*" % (client, client)
        sys.exit(0)
    else:
        """This function fetches metadata about wireless clients if needed, then
        displays whatever values have been requested"""
        clients = R0.Get_Data()
        for client in clients:
            if int(clients[client]['rx']) > -1 and int(clients[client]['tx']) > -1:
                print "MAC_%s_send.value %s" % (client, int(clients[client]['tx']))
                print "MAC_%s_recv.value %s" % (client, int(clients[client]['rx']))
                


if __name__ == '__main__':
    main()

