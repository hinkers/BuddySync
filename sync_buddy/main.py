import argparse
from sys import argv
from sync_buddy.logger import get_logger
from sync_buddy.read_config import read_config

def main():
    logo = '''
    ___              ___         _    _      
    / __|_  _ _ _  __| _ )_  _ __| |__| |_  _ 
    \__ \ || | ' \/ _| _ \ || / _` / _` | || |
    |___/\_, |_||_\__|___/\_,_\__,_\__,_|\_, |
        |__/                            |__/ 
    ===========================================
    '''
    print(logo)

    logger = get_logger('app')
    logger.info('App startup')

    parser = argparse.ArgumentParser(
        description='Synchronizes between different data sources base on config files and simple python scripts.')
    parser.add_argument('config_files', metavar='config_file', type=str, nargs='+',
                        help='a config file')
    parser.add_argument('--parse', '-p', action='store_true',
                        help='only parse the config, don\'t run')

    logger.debug(f'Receieved args: {argv[1:]}')
    parsed_args = parser.parse_args()
    logger.debug(f'Args passed successfully')

    container = read_config('.env', parsed_args.config_files)

    if not parsed_args.parse:
        container.create_all_tables()

        for script in container.scripts:
            script.run()

    container.save_variables()
    logger.info('App shutdown')


if __name__ == '__main__':
    main()
