#!/usr/bin/env python

import argparse
import json
import os

MAIN_DIRECTORY = os.path.join(os.path.expanduser('~'), '.spellbook')
if not os.path.exists(MAIN_DIRECTORY):
    os.makedirs(MAIN_DIRECTORY)
CONFIG_FILE = os.path.join(MAIN_DIRECTORY, 'config')
DATABASE_FILE = os.path.join(MAIN_DIRECTORY, 'database')


def collect_str(what):
    result = input("provide %s>> " % what)
    return result


def load_config(config_file):
    with open(config_file, 'rU') as fin:
        conf = json.load(fin)
    return conf


def list_spell(database_path):
    with open(database_path, 'rU') as fin:
        for line in fin:
            obj = json.loads(line)
            print(obj['cmd'], obj['desc'], sep='\t::>>\t')


def search_spell(database_path, what):
    with open(database_path, 'rU') as fin:
        for line in fin:
            obj = json.loads(line)
            for word in what:
                if word in obj['cmd'] or word in obj['desc']:
                    print(obj['cmd'])
                    break


def save_spell(database_path, cmd, desc):
    val = {
        'cmd': cmd,
        'desc': desc
    }
    with open(database_path, 'aU') as fout:
        fout.write(json.dumps(val))
        fout.write('\n')


def command_search(args):
    search_spell(DATABASE_FILE, args.data)


def command_add(args):
    data = args.data

    if len(data) == 2:
        cmd = data[0]
        desc = data[1]
    elif len(data) == 1:
        cmd = data[0]
        desc = collect_str('description')
    elif len(data) == 0:
        cmd = collect_str('command')
        desc = collect_str('description')
    else:
        print("ERR: got too much arguments (2 is max, got: %d)" % len(data))
        return

    print("%s::%s" % (cmd, desc))
    save_spell(DATABASE_FILE, cmd, desc)


def command_list(args):
    list_spell(DATABASE_FILE)


def prepare_parser():
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(dest='command_name')

    parser_search = subparsers.add_parser('search', aliases=['s'])
    parser_search.set_defaults(func=command_search)
    parser_search.add_argument('data', nargs='*')

    parser_add = subparsers.add_parser('add', aliases=['a'])
    parser_add.set_defaults(func=command_add)
    parser_add.add_argument('data', nargs='*')

    parser_search = subparsers.add_parser('list', aliases=['l'])
    parser_search.set_defaults(func=command_list)

    return parser


def main():
    parser = prepare_parser()
    args = parser.parse_args()

    if hasattr(args, 'func'):
        args.func(args)
    else:
        parser.print_help()

if __name__ == '__main__':
    main()
