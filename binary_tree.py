#!/usr/bin/env python

from mininet.topo import Topo
from mininet.net import Mininet
from mininet.log import setLogLevel
from mininet.util import dumpNodeConnections
from mininet.cli import CLI


class BinaryTreeTopo(Topo):
    def build(self, depth=3):
        # Create a list to store all the switches in the network
        switches = []

        # Add the root switch to the list of switches
        root_switch = self.addSwitch('s1')
        switches.append(root_switch)

        # Create the rest of the switches and links, based on the depth of the tree
        for i in range(2, 2**depth):
            switch = self.addSwitch('s' + str(i))
            switches.append(switch)

            parent_index = i // 2 - 1
            parent_switch = switches[parent_index]
            self.addLink(switch, parent_switch)

        # Add hosts to the leaves of the tree
        j = len(switches) - 1
        # Add hosts to the leaves of the tree
        for i in range(2**(depth - 1) + 1, 2**depth + 1):
            host1 = self.addHost('h' + str(i - 2**(depth - 1)))
            host2 = self.addHost(
                'h' + str(i - 2**(depth - 1) + 2**(depth - 1)))
            self.addLink(host1, switches[j])
            self.addLink(host2, switches[j])
            j -= 1


topos = {'binary_tree': BinaryTreeTopo}


def simpleTest():
    "Create and test a simple network"
    topo = BinaryTreeTopo(depth=4)
    net = Mininet(topo)
    net.start()
    print("Dumping host connections")
    dumpNodeConnections(net.hosts)
    print("Testing network connectivity")
    # net.pingAll()
    CLI(net)
    net.stop()


if __name__ == '__main__':
    # Tell mininet to print useful information
    setLogLevel('info')
    simpleTest()
