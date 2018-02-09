import argparse
from os import listdir
from os import path
from scapy.all import *
import random
from collections import deque
from difflib import SequenceMatcher

def sanitize(in_str):
    if in_str.startswith("b\'") or in_str.startswith("b\""):
        in_str = in_str[len("b\'"):]
    return in_str.replace('\\x', '').replace('\\', '').replace('\\', '')

def parse_payload(trace):
    payloads = deque()
    for packet in trace:
        cur_payload = sanitize(packet.split(",",7)[7].strip())
        if cur_payload == "-":
            continue
        payloads.append(cur_payload)
    return payloads

def table_packet(directory):
    ptraces = list()

    for trace in listdir(directory):
        ptraces.append(rdpcap(directory + "/" + trace))
        print trace
        
    packet_list = list()

    for packets in ptraces:
        container = deque()
        for pkt in packets:
            toprint = ""
            if TCP in pkt:
                toprint = str(packets).replace("<","").split(":")[0].strip() + ","
                toprint += str(pkt[Ether].src) + ","
                toprint += str(pkt[Ether].dst) + ","
                toprint += str(pkt[IP].src) + ","
                toprint += str(pkt[IP].dst) + ","
                toprint += str(pkt[TCP].sport) + ","
                toprint += str(pkt[TCP].dport) + ","
                if Raw in pkt:
                    toprint += sanitize(str(pkt[Raw].load))
                else:
                    toprint += "-"
            if toprint:
                container.append(toprint)
        packet_list.append(container)

    return packet_list
#
#    randomized_trace = list()
#
#    while packet_list:
#        cur = random.randint(0,len(packet_list) - 1)
#        randomized_trace.append(packet_list[cur].popleft())
#        if not packet_list[cur]:
#            packet_list.pop(cur)
#
#    return randomized_trace
#
def similar(str_a,str_b):
    seq = SequenceMatcher(None, str_a,str_b)
    return seq.ratio()

def get_connections(packets):  # dictionary of connections
    connections = dict()
    for packet in packets:
        data = packet.split(",",7)
        data[7] = data[7].strip()
        if data[7] == '-':
            continue # ignore empty payload
        if((data[3],data[4],data[5],data[6]) in connections): # src_ip,dst_ip,src_port,dst_port
            connections[(data[3],data[4],data[5],data[6])] += data[7]
        else:
            connections[(data[3],data[4],data[5],data[6])] = data[7]
    return connections

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('input', type=str, nargs='+', help="Input for the script.")
    parser.add_argument('-l','--logs', action='store_true', help="Print logs of packets. \
                                                                  Input: directory of traces")
    args = parser.parse_args()

    cur_input = args.input[0]

    if(args.logs): # python pcap_extractor.py <dir_name> -l
        logs = table_packet(cur_input)
        for log in logs:
            print(log)
    else:
        print("No processing found")
# endif
