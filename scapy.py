
from scapy.all import sendp, send, get_if_list, get_if_hwaddr
from scapy.all import Packet
from scapy.all import Ether, IP, UDP, TCP

import socket
import time
import psutil
# from memory_profiler import profile
# @profile
def main():
	#source_IP = socket.gethostbyname(sys.argv[1])
	#target_IP = socket.gethostbyname(sys.argv[2])
	#source_port = int(input("Enter Source Port Number:"))

			pkt=Ether(src='94:16:3e:3b:41:cf', dst='00:00:00:00:00:00',type=0x0800)/IP(src='0.0.0.0',dst='10.0.1.2',proto=6 ,tos= '2')/TCP(dport=443,sport=0, flags="A")
			myString = "z"*(67 - 40)
			pkt = pkt/myString
			pkt.show2()
			sendp(pkt, verbose=False)
			time.sleep(0.5)
if __name__ == '__main__':
	main()

