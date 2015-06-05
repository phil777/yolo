#! /usr/bin/env python

import subprocess
import argparse
import random

excuses = [
    "Testing is doubting.",
    "Do. Or do not. There is no try.",
]

commands = {}

def register(x):
    commands[x._cmd_] = x
    return x

class Command(object):
    _cmd_ = "N/A"
    def __init__(self, options):
        self.options = options
    def readjust_philisophy(self, args):
        return args
    def run(self, args):
        args.insert(0, self._cmd_)
        args = self.readjust_philisophy(args)
        if self.options.verbose:
            print " ".join(args)
        subprocess.call(args)

@register
class Mercurial(Command):
    _cmd_ = "hg"
    def readjust_philisophy(self, args):
        if len(args) > 1 and args[1] in ["pull", "push", "fetch", "clone"]:
            args = args[0:2]+["--insecure"]+args[2:]
        return args

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--verbose","-v", action="store_true")
    parser.add_argument("--dry-run","-n", action="store_true")
    sub = parser.add_subparsers(dest="command")
    
    for cmdname in commands:
        p = sub.add_parser(cmdname)
        p.add_argument("args", nargs="*", default=[])

    options = parser.parse_args()

    if options.dry_run:
        raise Exception(random.choice(excuses))

    cmd = commands[options.command](options)
    cmd.run(options.args)


if __name__ == "__main__":
    main()
