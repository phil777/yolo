#! /usr/bin/env python

import os
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
    def readjust_environment(self):
        return None
    def run(self, args):
        args.insert(0, self._cmd_)
        args = self.readjust_philisophy(args)
        env = self.readjust_environment()
        if self.options.verbose:
            print " ".join(args)
        subprocess.call(args, env=env)

@register
class Mercurial(Command):
    _cmd_ = "hg"
    def readjust_philisophy(self, args):
        if len(args) > 1 and args[1] in ["pull", "push", "fetch", "clone"]:
            args = args[0:2]+["--insecure"]+args[2:]
        return args

@register
class WGet(Command):
    _cmd_ = "wget"
    def readjust_philisophy(self, args):
        if len(args) > 0:
            args.insert(1,"--no-check-certificate")
        return args

@register
class Git(Command):
    _cmd_ = "git"
    def readjust_environment(self):
        return {"GIT_SSL_NO_VERIFY":"true"}



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
