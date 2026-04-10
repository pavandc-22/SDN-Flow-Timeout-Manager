from pox.core import core
import pox.openflow.libopenflow_01 as of

log = core.getLogger()

class TimeoutManager(object):
    def __init__(self, connection):
        self.connection = connection
        connection.addListeners(self)

    def _handle_PacketIn(self, event):
        packet = event.parsed

        # Create flow rule
        msg = of.ofp_flow_mod()

        # Match incoming packet
        msg.match = of.ofp_match.from_packet(packet, event.port)

        # TIMEOUT SETTINGS
        msg.idle_timeout = 10   # removed if idle for 10 sec
        msg.hard_timeout = 30   # removed after 30 sec

        # Action: flood packet
        msg.actions.append(of.ofp_action_output(port=of.OFPP_FLOOD))

        # Send flow rule to switch
        self.connection.send(msg)

        # IMPORTANT: Send current packet immediately
        packet_out = of.ofp_packet_out()
        packet_out.data = event.ofp
        packet_out.actions.append(of.ofp_action_output(port=of.OFPP_FLOOD))
        self.connection.send(packet_out)

        log.info("Flow installed with idle_timeout=10, hard_timeout=30")


class TimeoutController(object):
    def __init__(self):
        core.openflow.addListeners(self)

    def _handle_ConnectionUp(self, event):
        log.info("Switch connected: %s", event.connection)
        TimeoutManager(event.connection)


def launch():
    log.info("Starting Flow Rule Timeout Manager Controller")
    core.registerNew(TimeoutController)
