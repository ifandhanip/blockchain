from argparse import ArgumentParser
# from blockchain_udp import *

import os
import sys
import pprint

# py server_udp.py -p 5000 -s backup -t pbft -c 5

parser = ArgumentParser()
parser.add_argument('-p', '--port', default=5000, type=int, help='port to listen on')
parser.add_argument('-s', '--status', default='backup', type=str, help='server status (primary/ backup)')
parser.add_argument('-t', '--type', default='pbft', type=str, help='consensus type')
parser.add_argument('-c', '--client', default=5, type=int, help='total client')

args = parser.parse_args()
# node_identifier = str(uuid4()).replace('-', '')
port = args.port
node_status = args.status
consensus_type = args.type
client_total = args.client
print(node_status, 'server', 'in', consensus_type,'consensus', 'running using port', port, '...')

consensus = ''
if consensus_type == 'pbft':
    from consensus_pbft import *
    consensus = PBFTConsensus()

    blockchain.node_status = node_status
    blockchain.initial_transaction(client_total)
    blockchain.set_database(port)
    blockchain.set_keys(port)

    def full_chain():
        response = {
            'chain': blockchain.chain,
            'length': len(blockchain.chain),
        }
        pprint.pprint(response)

    def request_determiner(data):
        if data['route'] == 'node/register':
            blockchain.register_node(data)
        elif data['route'] == 'transaction/request':
            consensus.request_phase(data)        
        elif data['route'] == 'transaction/preprepare':
            consensus.preprepare_phase(data)
        elif data['route'] == 'transaction/prepare':
            consensus.prepare_phase(data)
        elif data['route'] == 'transaction/commit':
            consensus.commit_phase(data)
        elif data['route'] == 'chain':
            full_chain()
        else:
            print('route does not exist')

    def request_handler(i):
        while True:
            data, addr = sock.recvfrom(1500) # buffer size is 1500 bytes
            data = data.decode()
            data = json.loads(data)
            threads.append(Thread(target=request_determiner(data), args=(len(threads),)))
            threads[len(threads)-1].daemon = True
            threads[len(threads)-1].start()

    def terminate_program(i):
        while True:
            isTerminated = input("")
            if isTerminated == '0':
                exit()

    import socket
    UDP_IP = "127.0.0.1"
    UDP_PORT = port
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind((UDP_IP, UDP_PORT))

    from threading import Thread
    threads = []
    threads.append(Thread(target=request_handler, args=(0,)))
    threads.append(Thread(target=terminate_program, args=(1,)))
    threads[0].daemon = True
    threads[1].daemon = False
    threads[0].start()
    threads[1].start()

elif consensus_type == 'sbft':
    from consensus_sbft import *
    consensus = SBFTConsensus()

    # consensus.set_tempfile(str(port))
    blockchain.node_status = node_status
    blockchain.initial_transaction(client_total)
    blockchain.set_database(port)
    blockchain.set_keys(port)

    def full_chain():
        response = {
            'chain': blockchain.chain,
            'length': len(blockchain.chain),
        }
        pprint.pprint(response)

    def request_determiner(data):
        if data['route'] == 'node/register':
            blockchain.register_node(data)
        elif data['route'] == 'transaction/request':
            consensus.request_phase(data)        
        elif data['route'] == 'transaction/preprepare':
            consensus.preprepare_phase(data)
        elif data['route'] == 'chain':
            full_chain()
        else:
            print('route does not exist')

    def request_handler(i):
        while True:
            data, addr = sock.recvfrom(1500) # buffer size is 1500 bytes
            data = data.decode()
            data = json.loads(data)
            threads.append(Thread(target=request_determiner(data), args=(len(threads),)))
            threads[len(threads)-1].daemon = True
            threads[len(threads)-1].start()

    def terminate_program(i):
        while True:
            isTerminated = input("")
            if isTerminated == '0':
                exit()

    import socket
    UDP_IP = "127.0.0.1"
    UDP_PORT = port
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind((UDP_IP, UDP_PORT))

    from threading import Thread
    threads = []
    threads.append(Thread(target=request_handler, args=(0,)))
    threads.append(Thread(target=terminate_program, args=(1,)))
    threads[0].daemon = True
    threads[1].daemon = False
    threads[0].start()
    threads[1].start()
