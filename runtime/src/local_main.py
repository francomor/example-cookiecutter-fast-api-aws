import argparse
import inspect
import os
import sys

import uvicorn


def main():
    arg_parse = create_arg_parser()
    args = arg_parse.parse_args(sys.argv[1:])
    current_dir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
    parent_dir = os.path.dirname(current_dir)
    sys.path.insert(0, parent_dir)
    uvicorn.run("src.main:app", host=args.host, port=args.port, reload=True)


def create_arg_parser():
    default_host = '127.0.0.1'
    default_port = 8000
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--host", help=f"API host. Default is {default_host}", nargs='?', const=default_host,
        type=str, default=default_host
    )
    parser.add_argument(
        "-p", "--port", help=f"API port. Default is {default_port}", nargs='?', const=default_port,
        type=int, default=default_port
    )
    return parser


if __name__ == "__main__":
    main()
