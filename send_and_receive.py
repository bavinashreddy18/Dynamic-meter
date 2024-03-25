import argparse
import sys
import socket
import random
import struct

from scapy.all import sendp, send, get_if_list, get_if_hwaddr
from scapy.all import Packet
from scapy.all import Ether, IP, UDP, TCP


def get_if():
    ifs=get_if_list()
    iface=None # "h1-eth0"
    for i in get_if_list():
        if "eth0" in i:
            iface=i
            break;
    if not iface:
        print "Cannot find eth0 interface"
        exit(1)
    return iface

def main():

    if len(sys.argv)<3:
        print 'pass 2 arguments: <destination> "<tos>"'
        exit(1)

    addr = socket.gethostbyname(sys.argv[1])
    iface = get_if()
    #srcport=[4070, 4071, 8000, 16119, 53, 554, 8554, 19531, 80, 81, 443, 8008, 8009, 8000, 16119, 53, 21, 22, 23, 81, 554, 631, 943, 3910, 3911, 4070, 4071, 4520, 5001, 5002, 5080, 5555, 6668, 7888, 8008, 8009, 8554,9000, 9001, 8008, 8009, 8000, 16119, 53, 21, 22, 23, 81, 554, 631, 943, 3910, 3911, 4070, 4071, 4520, 5001, 5002, 5080, 5555, 6668, 7888, 8008, 8009, 8554,9000, 9001, 4070, 4071, 8000, 16119, 53, 554, 8554, 19531, 80, 81, 443, 8008, 8009, 8000, 16119, 53, 21, 22, 23, 81, 554, 631, 943, 3910, 3911, 4070, 4071, 4520, 5001, 5002, 5080, 5555, 6668, 7888, 8008, 8009, 8554,9000, 9001, 8008, 8009, 8000, 16119, 53, 21, 22, 23, 81, 554, 631, 943, 3910, 3911, 4070, 4071, 4520, 5001, 5002, 5080, 5555, 6668, 7888, 8008, 8009, 8554,9000, 9001, 4070, 4071, 8000, 16119, 53, 554, 8554, 19531, 80, 81, 443, 8008, 8009, 8000, 16119, 53, 21, 22, 23, 81, 554, 631, 943, 3910, 3911, 4070, 4071, 4520, 5001, 5002, 5080, 5555, 6668, 7888, 8008, 8009, 8554,9000, 9001, 8008, 8009, 8000, 16119, 53, 21, 22, 23, 81, 554, 631, 943, 3910, 3911, 4070, 4071, 4520, 5001, 5002, 5080, 5555, 6668, 7888, 8008, 8009, 8554,9000, 9001, 4070, 4071, 8000, 16119, 53, 554, 8554, 19531, 80, 81, 443, 8008, 8009, 8000, 16119, 53, 21, 22, 23, 81, 554, 631, 943, 3910, 3911, 4070, 4071, 4520, 5001, 5002, 5080, 5555, 6668, 7888, 8008, 8009, 8554,9000, 9001, 8008, 8009, 8000, 16119, 53, 21, 22, 23, 81, 554, 631, 943, 3910, 3911, 4070, 4071, 4520, 5001, 5002, 5080, 5555, 6668, 7888, 8008, 8009, 8554,9000, 9001]
    sno=0
    for i in range (0,1000):
        srcport = random.randint(150,450)
        dstport = random.randint(150,450)
        n = random.randint(100, 300)
        
        print "sending on interface %s to %s" % (iface, str(addr))
        pkt =  Ether(src=get_if_hwaddr(iface),dst = "00:00:0a:00:01:09")
        pkt = pkt /IP(dst=addr, tos=int(sys.argv[2]), flags=1, proto=17)
        pkt = pkt /TCP(sport = srcport, dport= dstport)
        myString = "z"*(n - 40)
        pkt = pkt/myString
        #pkt = pkt/"https://amazonecho.com/amazonecho"
        pkt.show2()
        sendp(pkt, iface=iface, verbose=False)
        time.sleep(0.1)
    for i in range (1001,2500):
        srcport = random.randint(150,450)
        dstport = random.randint(150,450)
        n = random.randint(100, 300)
        
        print "sending on interface %s to %s" % (iface, str(addr))
        pkt =  Ether(src=get_if_hwaddr(iface),dst = "00:00:0a:00:01:09")
        pkt = pkt /IP(dst=addr, tos=int(sys.argv[2]), flags=1, proto=1)
        pkt = pkt /TCP(sport = srcport, dport= dstport)
        myString = "z"*(n - 40)
        pkt = pkt/myString
        #pkt = pkt/"https://amazonecho.com/amazonecho"
        pkt.show2()
        sendp(pkt, iface=iface, verbose=False)
        time.sleep(0.1)
    for i in range (2501,7001):
        srcport = random.randint(150,450)
        dstport = random.randint(150,450)
        n = random.randint(100, 300)
        if (i%2)==0:
            sno=sno+1
        if (i%2)==0:
            if i==7000:
                print "sending on interface %s to %s" % (iface, str(addr))
                pkt =  Ether(src=get_if_hwaddr(iface),dst = "00:00:0a:00:01:09")
                pkt = pkt /IP(dst=addr, tos=int(sys.argv[2]), flags=0, proto=6)
                pkt = pkt /TCP(sport = srcport, dport= dstport, flags="F")
                myString = "z"*(n - 40)
                pkt = pkt/myString
                #pkt = pkt/"https://amazonecho.com/amazonecho"
                pkt.show2()
                sendp(pkt, iface=iface, verbose=False)
                time.sleep(0.1)
            else:
                print "sending on interface %s to %s" % (iface, str(addr))
                pkt =  Ether(src=get_if_hwaddr(iface),dst = "00:00:0a:00:01:09")
                pkt = pkt /IP(dst=addr, tos=int(sys.argv[2]), flags=1, proto=6)
                pkt = pkt /TCP(sport = srcport, dport= dstport, flags="S", seq=sno)
                myString = "z"*(n - 40)
                pkt = pkt/myString
            #pkt = pkt/"https://amazonecho.com/amazonecho"
                pkt.show2()
                sendp(pkt, iface=iface, verbose=False)
                time.sleep(0.1)
        else:
            print "sending on interface %s to %s" % (iface, str(addr))
            pkt =  Ether(src=get_if_hwaddr(iface),dst = "00:00:0a:00:01:09")
            pkt = pkt /IP(src="10.0.1.9",dst="10.0.1.4", tos=int(sys.argv[2]), flags=1, proto=6)
            pkt = pkt /TCP(sport = srcport, dport= dstport, flags="A", ack=sno)
            myString = "z"*(n - 40)
            pkt = pkt/myString
        #pkt = pkt/"https://amazonecho.com/amazonecho"
            pkt.show2()
            sendp(pkt, iface=iface, verbose=False)
            time.sleep(0.1)
    


if __name__ == '__main__':
    main()

