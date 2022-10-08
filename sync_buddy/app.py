import argparse

from sync_buddy.read_config import read_config

logo = '''
  ___              ___         _    _      
 / __|_  _ _ _  __| _ )_  _ __| |__| |_  _ 
 \__ \ || | ' \/ _| _ \ || / _` / _` | || |
 |___/\_, |_||_\__|___/\_,_\__,_\__,_|\_, |
      |__/                            |__/ 
===========================================
'''
print(logo)

parser = argparse.ArgumentParser(
    description='Synchronizes between different data sources base on config files and simple python scripts.')
parser.add_argument('config_files', metavar='config_file', type=str, nargs='+',
                    help='a config file')
parser.add_argument('--parse', '-p', action='store_true',
                    help='only parse the config, don\'t run')

args = parser.parse_args()

container = read_config(args.config_files)

if not args.parse:
    container.sql.create_tables()

    for e_name, count in container.run.items():
        for _ in range(int(count)):
            container.scripts[e_name].run()

container.save_variables()
