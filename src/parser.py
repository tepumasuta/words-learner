import argparse


_parser = argparse.ArgumentParser(prog='Words Learner')

_parser.add_argument_group('Test')
_parser.add_argument('test', metavar='test')
_parser.add_argument('db', nargs=1, type=str, metavar='<database-name>')

_parser.add_argument_group('Databases')
# _parser.add_argument('')

PARSER = _parser
