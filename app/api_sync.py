import argparse

from read_config import read_config

parser = argparse.ArgumentParser(description='Syn APIs')
parser.add_argument('config_files', metavar='config_file', type=str, nargs='+',
                    help='a config file')

args = parser.parse_args()

read_config(args.config_files)
