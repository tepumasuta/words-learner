#!/usr/bin/python3.11
import sys
import os

from app import Configuration, Application
from parser import get_help

def main():
    args = sys.argv[1:]
    
    if not args:
        print(get_help())
        return

    config: Configuration
    if args[0] == '-':
        if os.path.exists(Configuration.DEFAULT_PATH):
            config = Configuration.from_path(Configuration.DEFAULT_PATH)
        else:
            config = Configuration()
    else:
        # TODO: implement pretty error print
        config = Configuration.from_path(args[0])
    
    args = args[1:]

    app = Application.from_config(config, args)
    app.run()
    app.exit()


if __name__ == '__main__':
    main()        
