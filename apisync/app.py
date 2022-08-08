import argparse

from apisync.read_config import read_config

logo = '''
   _         _  __                  
  /_\  _ __ (_)/ _\_   _ _ __   ___ 
 //_\\\\| '_ \| |\ \| | | | '_ \ / __|
/  _  \ |_) | |_\ \ |_| | | | | (__ 
\_/ \_/ .__/|_|\__/\__, |_| |_|\___|
      |_|          |___/            
'''
print(logo)

parser = argparse.ArgumentParser(description='Syn APIs')
parser.add_argument('config_files', metavar='config_file', type=str, nargs='+',
                    help='a config file')

args = parser.parse_args()

read_config(args.config_files)
