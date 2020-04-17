import socket, pickle, os, json, configparser, argparse, asyncio, threading
from regie import RegieBoard


async def import_config(section:str):
    config = configparser.ConfigParser()
    config.read('regie_lead.ini')
    config = config[section]
    return config


async def update_local_cache():
    pass


async def request_credentials():
    pass


async def request_2fa_code(username):
    pass


async def fresh_start_regie_instance(username=None, password=None):
    regie = RegieBoard(username, password)
    await regie.start()
    return regie


async def full_stop_regie_instance(username, regie_boards):
    regie = regie_boards.get(username)
    await regie.stop()


async def pause_regie_instance():
    pass


async def resume_regie_instance():
    pass


async def register_new_instance():
    pass


def main():
    parser = argparse.ArgumentParser(description='Regie Lead')
    parser.add_argument('--username', action="store", dest='username', default=None)
    parser.add_argument('--password', action="store", dest='password', default=None)
    parser.add_argument('--instances', action="store", dest='instances', default=None)
    parser.add_argument('--userdata', action="store", dest='userdata', default=None)
    args = parser.parse_args()
    username = args.username
    password = args.password
    instances = int(args.instances)
    userdata = args.userdata

    regie_boards = {}

    if instances == 1 or instances == None:
        try:
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            asyncio.ensure_future(fresh_start_regie_instance(username, password))
            loop.run_forever()
        except KeyboardInterrupt:
            loop.stop()
            exit()
    instance = 1
    if instances > 1:
        loops = []
        try:
            while instance <= instances:
                loop = asyncio.new_event_loop()
                asyncio.set_event_loop(loop)
                asyncio.ensure_future(fresh_start_regie_instance(instance))
                loops.append((loop, instance))
                instance += 1
        except KeyboardInterrupt:
            for l in loops:
                l[0].stop()
            exit()

if __name__ == "__main__":
    main()
