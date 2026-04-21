#!/usr/bin/bash

import argparse

from installer import installer
from remove import remove

def main():
    parser = argparse.ArgumentParser(
        description="VPN build."
    )

    parser.add_argument(
        '--install',"-I",
        action='store_true',
        help='Install and configure wireguard.'
    )

    parser.add_argument(
        '--remove', "-R",
        action='store_true',
        help='Remove wireguard and configurations.'
    )

    args  = parser.parse_args()

    if args.install:
        installer()

    elif args.remove:
        remove()

    else:
        pass

if __name__ == "__main__":
    main()