"""
Changes Made To Code Are - 

1. _handle_PacketIn() : enable act_like_switch() and disable act_like_hub()
2. act_like_switch() :
    - TASK 3: Learning MAC addresses
    - TASK 4: Installing flow rules on switches using of.ofp_flow_mod()
    - TASK 5: Installing IP-matching rules on switch 1 (switch 7 as per professor's diagram)
"""

from pox.core import core
import pox.openflow.libopenflow_01 as of

log = core.getLogger()


class Tutorial (object):
    """
    A Tutorial object is created for each switch that connects.
    A Connection object for that switch is passed to the __init__ function.
    """

    def __init__(self, connection):
        # Keep track of the connection to the switch so that we can
        # send it messages!
        self.connection = connection

        # This binds our PacketIn event listener
        connection.addListeners(self)

        # Use this table to keep track of which ethernet address is on
        # which switch port (keys are MACs, values are ports).
        self.mac_to_port = {}

    def resend_packet(self, packet_in, out_port):
        """
        Instructs the switch to resend a packet that it had sent to us.
        "packet_in" is the ofp_packet_in object the switch had sent to the
        controller due to a table-miss.
        """
        msg = of.ofp_packet_out()
        msg.data = packet_in

        # Add an action to send to the specified port
        action = of.ofp_action_output(port=out_port)
        msg.actions.append(action)

        # Send message to switch
        self.connection.send(msg)

    def act_like_hub(self, packet, packet_in):
        """
        Implement hub-like behavior -- send all packets to all ports besides
        the input port.
        """

        # We want to output to all ports -- we do that using the special
        # OFPP_ALL port as the output port.  (We could have also used
        # OFPP_FLOOD.)
        self.resend_packet(packet_in, of.OFPP_ALL)

        # Note that if we didn't get a valid buffer_id, a slightly better
        # implementation would check that we got the full data before
        # sending it (len(packet_in.data) should be == packet_in.total_len)).

    def act_like_switch(self, packet, packet_in):
        # print("#### DPID OF SWITCH IS: #### " + str(self.connection.dpid))

        if self.connection.dpid == 1 and packet.type == packet.IP_TYPE:
            # Install IP-matching rule on switch 1
            fm = of.ofp_flow_mod()
            fm.match.dl_type = 0x0800
            fm.match.nw_dst = packet.next.dstip
            out_port = self.mac_to_port[packet.dst] if packet.dst in self.mac_to_port else of.OFPP_ALL
            action = of.ofp_action_output(port=out_port)
            fm.actions.append(action)
            self.connection.send(fm)

            # Log that the IP-matching rule was installed
            print("Installed IP-matching rule on switch {} for destination IP {}".format(
                self.connection.dpid, packet.next.dstip))

            # Resend the packet
            self.resend_packet(packet_in, out_port)

            # Log that the packet was resent
            print("Resent packet on switch {} with destination IP {}".format(
                self.connection.dpid, packet.next.dstip))

            return

        # Check if the source MAC is already learned; if not, learn it and log the learning
        if packet.src not in self.mac_to_port:
            print("Learning that " + str(packet.src) +
                  " is attached at port " + str(packet_in.in_port))
            self.mac_to_port[packet.src] = packet_in.in_port

        # If the port associated with the destination MAC of the packet is known:
        if packet.dst in self.mac_to_port:
            # Send packet out the associated port
            print(str(packet.dst) + " destination known. only send message to it")
            self.resend_packet(packet_in, self.mac_to_port[packet.dst])

            # Load the flow module
            fm = of.ofp_flow_mod()
            # Fill the match field (we match the flow with its destination address)
            fm.match.dl_dst = packet.dst
            # Add an action to send to the specified port
            out_port = self.mac_to_port[packet.dst]
            action = of.ofp_action_output(port=out_port)
            fm.actions.append(action)
            # Send message to switch
            self.connection.send(fm)

        else:
            # Flood the packet out everything but the input port
            print(str(packet.dst) + " not known, resend to everybody")
            self.resend_packet(packet_in, of.OFPP_ALL)

    def _handle_PacketIn(self, event):
        """
        Handles packet in messages from the switch.
        """

        packet = event.parsed  # This is the parsed packet data.
        if not packet.parsed:
            log.warning("Ignoring incomplete packet")
            return

        packet_in = event.ofp  # The actual ofp_packet_in message.

        # Comment out the following line and uncomment the one after
        # when starting the exercise.
        # self.act_like_hub(packet, packet_in)
        self.act_like_switch(packet, packet_in)


def launch():
    """
    Starts the component
    """
    def start_switch(event):
        log.debug("Controlling %s" % (event.connection,))
        Tutorial(event.connection)
    core.openflow.addListenerByName("ConnectionUp", start_switch)
