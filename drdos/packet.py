class Packet:
    payload: str    

class ARDPacket(Packet):
    def __init__(self):        
        self.payload = b"\x00\x14\x00\x00"        

class SteamRPPacket(Packet):
    def __init__(self):
        self.payload = b"\xff\xff\xff\xff\x21\x4c\x5f\xa0\x04\x00\x00\x00\x08\x01\x10\x00"   

class MemcachedPacket(Packet):
    def __init__(self):
        self.payload = b"\x00\x00\x00\x00\x00\x01\x00\x00"
    
    def command(self, cmd):
        self.payload += cmd.encode('ascii')+b"\x0d\x0a"
