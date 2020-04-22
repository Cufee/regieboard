import argparse
import sys
import uuid
import asyncio
import socket
import select
from http.server import HTTPServer, BaseHTTPRequestHandler
from threading import Thread
from regie import RegieBoard


def logger(msg):
    print(f'[Lead] {msg}')


def fresh_start_regie_instance(username, password):
    print(f'Lead {username}:{password}')
    asyncio.set_event_loop(asyncio.new_event_loop())
    loop = asyncio.get_event_loop()
    regie = RegieBoard(username, password)
    asyncio.ensure_future(regie.start())
    loop.run_forever()
    del threads[username]


def main():
    parser = argparse.ArgumentParser(description='Regie Lead')
    parser.add_argument('--test-mode', action="store",
                        dest='test_mode', default=False)
    parser.add_argument('--instances', action="store",
                        dest='instances', default=1)
    parser.add_argument('--rm-ip', action="store",
                        dest='rm_ip', default='127.0.0.1')
    parser.add_argument('--rm-port', action="store",
                        dest='rm_port', default=6900)
    args = parser.parse_args()
    test_mode = args.test_mode
    instances = int(args.instances)
    username = 'IoNstish'
    password = 'JYss7x66h!NgxL&4'
    # IP and PORT for Regie Manager
    rm_ip = args.rm_ip
    rm_port = args.rm_port

    global threads
    threads = {}

    counter = 0
    while counter != instances:
        # Start one Regie instance
        thread_uuid = uuid.uuid1()
        threads.update({username: thread_uuid})
        regie_thread = Thread(target=fresh_start_regie_instance, args=(
            username, password,), name=thread_uuid)
        regie_thread.start()
        counter += 1


if __name__ == "__main__":
    main()
