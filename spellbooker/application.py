#!/usr/bin/env python
from __future__ import (absolute_import, division,
                        print_function, unicode_literals)

import argparse
import imp
import json
import os
from builtins import *

from spellbooker import VERSION

MAIN_DIRECTORY = os.path.join(os.path.expanduser('~'), '.spellbook')
CONFIG_DIRECTORY = os.path.join(MAIN_DIRECTORY, 'config')
if not os.path.exists(CONFIG_DIRECTORY):
    os.makedirs(CONFIG_DIRECTORY)

try:
    imp.find_module('dropbox')
    dropbox_available = True

    DROPBOX_TOKEN_PATH = os.path.join(CONFIG_DIRECTORY, 'dropbox_token')
    DROPBOX_REPO_PATH = os.path.join(MAIN_DIRECTORY, 'dropbox_repo')
    if not os.path.exists(DROPBOX_REPO_PATH):
        os.makedirs(DROPBOX_REPO_PATH)
except ImportError as e:
    dropbox_available = False
    pass


def collect_str(what):
    result = input("provide %s>> " % what).strip()
    return result


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
        fout.write(str(json.dumps(val)))
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


def command_dropbox_connect(args):
    import dropbox

    if args.spellbook_name is not None:
        print('ERR: sync is only for all books')
        return

    app_key = 'ow3gosk8pb9bhkr'
    app_secret = 'w3eqoqx5scb64pd'
    flow = dropbox.DropboxOAuth2FlowNoRedirect(app_key, app_secret)
    # Have the user sign in and authorize this token
    authorize_url = flow.start()
    print('1. Go to: ' + authorize_url)
    print('2. Click "Allow" (you might have to log in first)')
    print('3. Copy the authorization code.')
    code = collect_str("the authorization code here")

    # This will fail if the user enters an invalid authorization code
    access_token, user_id = flow.finish(code)

    client = dropbox.Dropbox(access_token)
    print('successfully linked account: ', client.users_get_current_account().name.display_name)
    with open(DROPBOX_TOKEN_PATH, 'w') as fout:
        fout.write(access_token)


def db_repo_load():
    repo = {}
    for file_name in os.listdir(DROPBOX_REPO_PATH):
        with open(os.path.join(DROPBOX_REPO_PATH, file_name), 'rU') as fin:
            repo[file_name] = fin.read()

    for file_name in os.listdir(MAIN_DIRECTORY):
        if os.path.isfile(os.path.join(MAIN_DIRECTORY, file_name)) and file_name not in repo:
            repo[file_name] = None

    return repo


def db_repo_update(spellbook_name, rev):
    spellbook_path = os.path.join(DROPBOX_REPO_PATH, spellbook_name)
    with open(spellbook_path, 'w') as fout:
        fout.write(rev)


def db_repo_removed_list():
    removed = []
    for file_name in os.listdir(DROPBOX_REPO_PATH):
        if not os.path.isfile(os.path.join(MAIN_DIRECTORY, file_name)):
            removed.append(file_name)

    return removed


def db_repo_remove(spellbook_name):
    spellbook_path = os.path.join(DROPBOX_REPO_PATH, spellbook_name)
    os.remove(spellbook_path)


def db_load_token():
    return open(DROPBOX_TOKEN_PATH, 'rU').read()


def db_sync():
    import dropbox
    dbx = dropbox.Dropbox(db_load_token())
    repo = db_repo_load()
    for book in dbx.files_list_folder('').entries:
        if book.name not in repo:
            db_download(dbx, book.name)
        elif repo[book.name] != book.rev:
            db_merge(dbx, book.name, book.rev)
            db_update(dbx, book.name, book.rev)
            repo.pop(book.name)
        elif repo[book.name] == book.rev:
            # TODO: prevent uploading unchanged files
            db_update(dbx, book.name, book.rev)
            repo.pop(book.name)
        else:
            print('dead end: %s' % book.name)

    for spellbook_name in repo:
        if repo[spellbook_name] is None:
            db_upload(dbx, spellbook_name)

    for spellbook_name in db_repo_removed_list():
        db_remove(dbx, spellbook_name)


def db_upload(dbx, spellbook_name):
    import dropbox
    spellbook_path = os.path.join(MAIN_DIRECTORY, spellbook_name)
    with open(spellbook_path, 'rU') as fout:
        response = dbx.files_upload(fout, os.path.join('/', spellbook_name), mode=dropbox.files.WriteMode.add)

    db_repo_update(spellbook_name, response.rev)


def db_update(dbx, spellbook_name, rev):
    import dropbox
    spellbook_path = os.path.join(MAIN_DIRECTORY, spellbook_name)
    with open(spellbook_path, 'rU') as fout:
        response = dbx.files_upload(fout, os.path.join('/', spellbook_name), mode=dropbox.files.WriteMode.update(rev))

    db_repo_update(spellbook_name, response.rev)


def db_remove(dbx, spellbook_name):
    dbx.files_delete(os.path.join('/', spellbook_name))
    db_repo_remove(spellbook_name)


def db_merge(dbx, spellbook_name, rev):
    spellbook_path = os.path.join(MAIN_DIRECTORY, spellbook_name)
    with open(spellbook_path, 'rU') as fin:
        local_spells = [json.loads(line) for line in fin]

    metadata, http_resp = dbx.files_download('rev:%s' % rev)
    local_spells.extend(json.loads(line.decode('utf-8')) for line in http_resp.iter_lines() if
                        json.loads(line.decode('utf-8')) not in local_spells)

    with open(spellbook_path, 'w') as fout:
        for val in local_spells:
            fout.write(str(json.dumps(val)))
            fout.write('\n')

    db_repo_update(spellbook_name, metadata.rev)


def db_download(dbx, spellbook_name):
    spellbook_path = os.path.join(MAIN_DIRECTORY, spellbook_name)
    response = dbx.files_download_to_file(spellbook_path, os.path.join('/', spellbook_name))
    db_repo_update(spellbook_name, response.rev)


def command_dropbox_sync(args):
    if args.spellbook_name is not None:
        print('ERR: sync is only for all books')
        return
    db_sync()


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

    if dropbox_available:
        parser_db_connect = subparsers.add_parser('connectdb', help='connect to dropbox storage')
        parser_db_connect.set_defaults(func=command_dropbox_connect)

        parser_db_sync = subparsers.add_parser('sync', help='sync to dropbox storage')
        parser_db_sync.set_defaults(func=command_dropbox_sync)

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
