# coding: utf-8

import toml
import logging
import argparse

from laputa.watch import Watcher
from laputa.record import Recorder
from laputa.notify import IFTTTNotifier


def read_config(file_name):
    with open(file_name) as config_file:
        config = toml.loads(config_file.read())
    return config


def parse():
    parser = argparse.ArgumentParser(description='Laputa, flying in the sky')
    parser.add_argument('-c', metavar='CONFIG_FILE',
                        required=True, help='config file')
    return parser.parse_args()


def main():
    args = parse()
    config = read_config(args.c)

    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger()
    handler = logging.FileHandler(config['run']['log_file'])
    handler.setLevel(logging.INFO)
    logging_format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    formatter = logging.Formatter(logging_format)
    handler.setFormatter(formatter)
    logger.addHandler(handler)

    watcher = Watcher(config['laputa']['weibo_uid'],
                      Recorder(config['run']['record_file']),
                      IFTTTNotifier(config['laputa']['ifttt_key'],
                                    config['laputa']['ifttt_event']))
    watcher.watch()
