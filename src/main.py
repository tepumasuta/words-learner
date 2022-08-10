import sys

from app import Configuration, Application


def main():
    args = sys.argv[1:]
    
    # TODO: implement pretty error print
    if not args:
        print(...)
        return

    config: Configuration
    if args[0] == '-':
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
