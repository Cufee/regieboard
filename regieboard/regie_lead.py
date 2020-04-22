import argparse, sys, uuid, asyncio, socket
from threading import Thread
from regie import RegieBoard


def fresh_start_regie_instance(regie_uuid, username, password):
    asyncio.set_event_loop(asyncio.new_event_loop())
    loop = asyncio.get_event_loop()
    regie = RegieBoard(regie_uuid, username, password)
    asyncio.ensure_future(regie.start())
    print(f'Lead started Regie {regie_uuid}')
    loop.run_forever()


def full_stop_regie_instance(username, regie_boards):
    regie = regie_boards.get(username)
    regie.stop()


def connect_to_manager(rm_ip, rm_port, test_mode,):
    asyncio.set_event_loop(asyncio.new_event_loop())
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((rm_ip, rm_port))
    client_socket.setblocking(False)


def main():
    parser = argparse.ArgumentParser(description='Regie Lead')
    parser.add_argument('--test-mode', action="store", dest='test_mode', default=False)
    parser.add_argument('--username', action="store", dest='username', default=None)
    parser.add_argument('--password', action="store", dest='password', default=None)
    parser.add_argument('--instances', action="store", dest='instances', default=1)
    parser.add_argument('--data-path', action="store", dest='data_path', default=None)
    parser.add_argument('--rm-ip', action="store", dest='rm_ip', default='127.0.0.1')
    parser.add_argument('--rm-port', action="store", dest='rm_port', default=6900)
    args = parser.parse_args()
    test_mode = args.test_mode
    username = args.username
    password = args.password
    instances = int(args.instances)
    #Path to login/password dictionary
    data_path = args.data_path
    #IP and PORT for Regie Manager
    rm_ip = args.rm_ip
    rm_port = args.rm_port

    #Connect to Regie Manager
    Thread(target=connect_to_manager, args=(rm_ip, rm_port, test_mode,), name='lead_thread')
    
    threads = {}

    if username and password or instances <= 1:
        #Start one Regie instance
        regie_uuid = uuid.uuid1()
        regie_thread = Thread(target=fresh_start_regie_instance, args=(regie_uuid, username, password,), name=regie_uuid)

        regie_thread.start()
        threads.update({username: regie_uuid})
        print('\n\nRegie thread started, moving on\n\n')

    if data_path:
        #Check the dict and start a Regie per username in dict
        #Keep the local dict updated
        pass

    counter = 1
    while counter != instances:
        #Start one Regie instance
        thread_uuid = uuid.uuid1()
        threads.update({username: thread_uuid})
        regie_thread = Thread(target=fresh_start_regie_instance, args=(thread_uuid, username, password,), name=regie_uuid)

        regie_thread.start()

        print('\n\nRegie thread started, moving on\n\n')
        counter += 1

    print(threads)




if __name__ == "__main__":
    main()
