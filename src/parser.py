import argparse


_parser_test = argparse.ArgumentParser(prog='Test: words-learner', exit_on_error=False)
_parser_test.add_argument_group('Test')
_parser_test.add_argument('test', metavar='test', choices=['test'], help='Test words from database <database-name>')
_parser_test.add_argument('db', nargs=1, type=str, metavar='<database-name>', help='Name of database to be tested')

_parser_get = argparse.ArgumentParser(prog='Get: words-learner', exit_on_error=False)
_parser_get.add_argument_group('Get record from database')
_parser_get.add_argument('get', metavar='get', choices=['get'])
_parser_get.add_argument('db', nargs=1, type=str, metavar='<database-name>')
_parser_get.add_argument('key', nargs=1, type=str, metavar='<key>')

_parser_add = argparse.ArgumentParser(prog='Add: words-learner', exit_on_error=False)
_parser_add.add_argument_group('Add records to database')
_parser_add.add_argument('add', metavar='add', choices=['add'])
_parser_add.add_argument('db', nargs=1, type=str, metavar='<database-name>')
_parser_add.add_argument('key', nargs=1, type=str, metavar='<key>')
_parser_add.add_argument('values', nargs='+', type=str, metavar='<value>')

_parser_rm = argparse.ArgumentParser(prog='Remove: words-learner', exit_on_error=False)
_parser_rm.add_argument_group('Remove records from database')
_parser_rm.add_argument('rm', metavar='rm', choices=['rm'])
_parser_rm.add_argument('db', nargs=1, type=str, metavar='<database-name>')
_parser_rm.add_argument('key', nargs=1, type=str, metavar='<key>')
_parser_rm.add_argument('-V', '--values', nargs='*', type=str, metavar='<value>')

_parser_list = argparse.ArgumentParser(prog='List: words-learner', exit_on_error=False)
_parser_list.add_argument_group('List different things')
_parser_list.add_argument('list', metavar='list', choices=['list'])
_parser_list.add_argument('dbs', nargs='*', type=str, metavar='<database-name>')

_parser_create = argparse.ArgumentParser(prog='Create: words-learner', exit_on_error=False)
_parser_create.add_argument_group('Create databases')
_parser_create.add_argument('create', metavar='create', choices=['create'])
_parser_create.add_argument('db', nargs=1, type=str, metavar='<database-name>')
_parser_create.add_argument('db_path', nargs=1, type=str, metavar='<database-path>')
_parser_create.add_argument('db_alias', nargs='?', type=str, metavar='<alias>')

_parser_print = argparse.ArgumentParser(prog='Print: words-learner', exit_on_error=False)
_parser_print.add_argument_group('Print databases')
_parser_print.add_argument('print', metavar='print', choices=['print'])
_parser_print.add_argument('db', nargs=1, type=str, metavar='<database-name>')

_parser_attach = argparse.ArgumentParser(prog='Attach: words-learner', exit_on_error=False)
_parser_attach.add_argument_group('Attach databases')
_parser_attach.add_argument('attach', metavar='attach', choices=['attach'])
_parser_attach.add_argument('db_alias', nargs=1, type=str, metavar='<alias>')
_parser_attach.add_argument('db_path', nargs=1, type=str, metavar='<database-path>')

_parser_detach = argparse.ArgumentParser(prog='Detach: words-learner', exit_on_error=False)
_parser_detach.add_argument_group('Detach databases')
_parser_detach.add_argument('detach', metavar='detach', choices=['detach'])
_parser_detach.add_argument('db', nargs=1, type=str, metavar='<database-name>')

PARSERS = [_parser_test, _parser_get, _parser_add, _parser_rm, _parser_list, _parser_create,
           _parser_print, _parser_attach, _parser_detach]

def get_help() -> str:
    text = ''
    usages = []
    helps = []
    options = []
    for parser in PARSERS:
        usages.append(parser.format_usage())
        format_help = parser.format_help()
        # print(format_help)
        helps.append(format_help[format_help.find('positional arguments'):format_help.find('options')][len('positional arguments: \n'):-1].rstrip())

    usage = 'usage:\n' + '\n'.join((f"-{u[len('usage:'):-1]}\n {h}\n" for u, h in zip(usages, helps)))
    return usage
