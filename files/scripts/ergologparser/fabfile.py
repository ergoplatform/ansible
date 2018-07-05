#!/usr/bin/env python3

from fabric.api import *

env.use_ssh_config = True
env.hosts = [
    'testnet1-ubuntu-s-2vcpu-4gb-lon1-01',
    '209.97.134.210'
]
env.user = "root"
env.key_filename = '/home/andyceo/.ssh/id_ed25519'


def hello(name="my world"):
    print("Hello {}!".format(name))


def test():
    run('uname -a')


def copy_script():
    put('ergologparser.py', '~')
