import argparse
import os

import sys

MAIN_DIRECTORY = os.path.join(os.path.expanduser('~'), '.spellbook')
CONFIG_FILE = os.path.join(MAIN_DIRECTORY, 'config')
DATABASE_FILE = os.path.join(MAIN_DIRECTORY, 'database')

print("hejo")


def command_search(args):
    print('command search')


def command_add(args):
    print('command add')


def prepare_argparse():
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(dest='command_name')

    parser_search = subparsers.add_parser('search')
    parser_search.set_defaults(func=command_search)

    parser_add = subparsers.add_parser('add')
    parser_add.set_defaults(func=command_add)

    return parser


def main():
    parser = prepare_argparse()
    args = parser.parse_args()
    print(args.command_name)
    args.func(args)


if __name__ == '__main__':
    main()
