import socket, pickle, os, json, configparser, argparse
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


async def fresh_start_regie_instance(username, password):
    regie =  RegieBoard(username, password)
    regie.start()
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
    args = parser.parse_args()
    username = args.username
    password = args.password
    regie_boards = {}

    try:
        regie = await fresh_start_regie_instance(username, password)
        regie_boards.update({username: regie})
    except KeyboardInterrupt:
        await full_stop_regie_instance(username, regie_boards)


if __name__ == "__main__":
    main()
