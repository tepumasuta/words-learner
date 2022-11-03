#!/usr/bin/python3.11
import sys

from app import Configuration, Application
from parser import get_help

def main():
    args = sys.argv[1:]
    
    if not args:
        print(get_help())
        return
    
    config: Configuration
    try:
        config = Configuration.from_path(Configuration.PATH)
    except OSError as e:
        # TODO: print error message via application
        # -> implement event queue for stacking events up before Application 
        config = Configuration()

    app = Application.from_config(config, args)
    app.run()
    app.exit()


if __name__ == '__main__':
    main()        
