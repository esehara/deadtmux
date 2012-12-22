# -*- coding: utf-8 -*-
import argparse
import writer
import os
import yaml


def write(args):

    yamlfile = open(args.input)
    conf = yaml.load(yamlfile.read())
    manager = writer.PaneManager(conf)
    build_string = manager.output()

    if args.debug:
        print build_string
    else:
        f = open(args.output, "w")
        f.write(build_string)
        f.close()

def input_filepath(string):
    if not os.path.isfile(string):
        raise argparse.ArgumentTypeError(
            'file "%s" is not exist.' % string)
    return string


def parser():
    parser = argparse.ArgumentParser(
        description="deadtmux")

    parser.add_argument(
        'input',
        type=input_filepath,
        help="configure yaml file.")

    parser.add_argument(
        'output',
        type=str,
        help="output shell script.")

    parser.add_argument('--debug', action='store_true')

    return parser.parse_args()


def main():
    args = parser()
    write(args)

if __name__ == "__main__":
    main()
