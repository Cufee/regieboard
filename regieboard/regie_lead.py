import socket, pickle, os, json, configparser


def import_config(section:str):
    config = configparser.ConfigParser()
    config.read('regie_lead.ini')
    config = config[section]
    return config


async def update_local_cache():
    pass


async def request_credentials(number):
    pass


async def request_2fa_code(number, username):
    pass


async def fresh_start_regie_instance(number, username, password):
    username_id = ''
    return username_id


async def full_stop_regie_instance(username_id):
    pass


async def pause_regie_instance(username_id):
    pass


async def resume_regie_instance(username_id):
    pass


async def register_new_instance(username_id):
    pass


def main():
    pass


if __name__ == "__main__":
    pass
