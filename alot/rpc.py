import os
from twisted.internet import protocol


def _expand_path(path):
    return os.path.expandvars(os.path.expanduser(path))


def create_rpc_server(reactor, ui, socket_path):

    class RPC(protocol.Protocol):
        def dataReceived(self, data):
            if data.strip() == 'refresh':
                ui.current_buffer.rebuild()
                ui.update()
                self.transport.write('refresh\n')
            else:
                self.transport.write('Unknown command\n')

    factory = protocol.ServerFactory()
    factory.protocol = RPC
    socket_path = _expand_path(socket_path)
    if os.path.exists(socket_path):
        os.remove(socket_path)
    reactor.listenUNIX(socket_path, factory)
