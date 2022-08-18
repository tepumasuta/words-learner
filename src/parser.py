import argparse


_parser_test = argparse.ArgumentParser(prog='Words Learner Test', exit_on_error=False)
_parser_test.add_argument_group('Test')
_parser_test.add_argument('test', metavar='test', choices=['test'])
_parser_test.add_argument('db', nargs=1, type=str, metavar='<database-name>')

_parser_get = argparse.ArgumentParser(prog='Words Learner Get', exit_on_error=False)
_parser_get.add_argument_group('Get record from database')
_parser_get.add_argument('get', metavar='get', choices=['get'])
_parser_get.add_argument('db', nargs=1, type=str, metavar='<database-name>')
_parser_get.add_argument('key', nargs=1, type=str, metavar='<key>')

_parser_add = argparse.ArgumentParser(prog='Words Learner Add', exit_on_error=False)
_parser_add.add_argument_group('Add records to database')
_parser_add.add_argument('add', metavar='add', choices=['add'])
_parser_add.add_argument('db', nargs=1, type=str, metavar='<database-name>')
_parser_add.add_argument('key', nargs=1, type=str, metavar='<key>')
_parser_add.add_argument('values', nargs='+', type=str, metavar='<value>')

_parser_rm = argparse.ArgumentParser(prog='Words Learner Remove', exit_on_error=False)
_parser_rm.add_argument_group('Remove records from database')
_parser_rm.add_argument('rm', metavar='rm', choices=['rm'])
_parser_rm.add_argument('db', nargs=1, type=str, metavar='<database-name>')
_parser_rm.add_argument('key', nargs=1, type=str, metavar='<key>')
_parser_rm.add_argument('-V', '--values', nargs='*', type=str, metavar='<value>')

_parser_list = argparse.ArgumentParser(prog='Words Learner List', exit_on_error=False)
_parser_list.add_argument_group('List different things')
_parser_list.add_argument('list', metavar='list', choices=['list'])
_parser_list.add_argument('dbs', nargs='*', type=str, metavar='<database-name>')

_parser_create = argparse.ArgumentParser(prog='Words Learner Create', exit_on_error=False)
_parser_create.add_argument_group('Create databases')
_parser_create.add_argument('create', metavar='create', choices=['create'])
_parser_create.add_argument('db', nargs=1, type=str, metavar='<database-name>')
_parser_create.add_argument('db_path', nargs=1, type=str, metavar='<database-path>')
_parser_create.add_argument('db_alias', nargs='?', type=str, metavar='<alias>')

PARSERS = [_parser_test, _parser_get, _parser_add, _parser_rm, _parser_list, _parser_create]
