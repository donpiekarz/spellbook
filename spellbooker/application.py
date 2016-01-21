#!/usr/bin/env python
from __future__ import print_function

import argparse
import json
import os

MAIN_DIRECTORY = os.path.join(os.path.expanduser('~'), '.spellbook')
if not os.path.exists(MAIN_DIRECTORY):
    os.makedirs(MAIN_DIRECTORY)
CONFIG_FILE = os.path.join(MAIN_DIRECTORY, 'config')
DATABASE_FILE = os.path.join(MAIN_DIRECTORY, 'database')

VERSION = '1.0.2'


def collect_str(what):
    result = input("provide %s>> " % what)
    return result


def load_config(config_file):
    with open(config_file, 'rU') as fin:
        conf = json.load(fin)
    return conf


def list_spell(database_path, _):
    with open(database_path, 'rU') as fin:
        for line in fin:
            obj = json.loads(line)
            print(obj['cmd'], obj['desc'], sep='\t::>>\t')


def search_spell(database_path, args):
    what = args.data
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
    with open(database_path, 'a') as fout:
        fout.write(json.dumps(val))
        fout.write('\n')


def wrap_optional_spellbook(func, args):
    if args.spellbook_name is not None:
        database_path = os.path.join(MAIN_DIRECTORY, args.spellbook_name)
        if not os.path.isfile(database_path):
            print("ERR: no such spellbook: %s" % args.spellbook_name)
            return
        func(database_path, args)
    else:
        for p in filter(lambda f: os.path.isfile(os.path.join(MAIN_DIRECTORY, f)), os.listdir(MAIN_DIRECTORY)):
            func(os.path.join(MAIN_DIRECTORY, p), args)


def command_search(args):
    wrap_optional_spellbook(search_spell, args)


def command_add(args):
    data = args.data
    database_path = os.path.join(MAIN_DIRECTORY, args.spellbook_name)
    if not os.path.isfile(database_path):
        print("ERR: no such spellbook: %s" % args.spellbook_name)
        return

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
    save_spell(database_path, cmd, desc)


def command_list(args):
    wrap_optional_spellbook(list_spell, args)


def command_create(args):
    if args.spellbook_name is None:
        print("ERR: please set new spellbook name")
        return
    database_path = os.path.join(MAIN_DIRECTORY, args.spellbook_name)
    if os.path.isfile(database_path):
        print("ERR: such spellbook already exist")
        return

    # create empty file
    open(database_path, 'a').close()


def prepare_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument('--version', action='version', version='%(prog)s ' + VERSION)
    parser.add_argument('spellbook_name', help='name of spellbook')
    subparsers = parser.add_subparsers(dest='command_name')

    parser_search = subparsers.add_parser('search', help='search for spells')
    parser_search.set_defaults(func=command_search)
    parser_search.add_argument('data', nargs='*')

    parser_add = subparsers.add_parser('add', help='add spell')
    parser_add.set_defaults(func=command_add)
    parser_add.add_argument('data', nargs='*')

    parser_list = subparsers.add_parser('list', help='list all spells')
    parser_list.set_defaults(func=command_list)

    parser_create = subparsers.add_parser('create', help='create new spellbook')
    parser_create.set_defaults(func=command_create)

    # hacks for lack of aliases for python 2
    parser_s = subparsers.add_parser('s', help='shortcut for search')
    parser_s.set_defaults(func=command_search)
    parser_s.add_argument('data', nargs='*')

    parser_a = subparsers.add_parser('a', help='shortcut for add')
    parser_a.set_defaults(func=command_add)
    parser_a.add_argument('data', nargs='*')

    parser_l = subparsers.add_parser('l', help='shortcut for list')
    parser_l.set_defaults(func=command_list)

    return parser


def validate_parser(parser):
    args = parser.parse_args()

    if args.spellbook_name == '-':
        args.spellbook_name = None

    return args


def main():
    parser = prepare_parser()
    args = validate_parser(parser)

    if hasattr(args, 'func'):
        args.func(args)
    else:
        parser.print_help()


if __name__ == '__main__':
    main()
