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

        msg.match = of.ofp_match.from_packet(packet, event.port)

        # 🔥 TIMEOUT SETTINGS
        msg.idle_timeout = 10   # removed if idle for 10 sec
        msg.hard_timeout = 30   # removed after 30 sec anyway

        msg.actions.append(of.ofp_action_output(port=of.OFPP_FLOOD))

        # Send flow rule
        self.connection.send(msg)

        log.info("Flow installed with timeout")

class TimeoutController(object):
    def __init__(self):
        core.openflow.addListeners(self)

    def _handle_ConnectionUp(self, event):
        log.info("Switch connected")
        TimeoutManager(event.connection)

def launch():
    core.registerNew(TimeoutController)
