from .packet import Packet


class ProbePacket(Packet):
    def __init__(self):
        super().__init__()
        self.data.update({
            'action': 'probe'
        })
