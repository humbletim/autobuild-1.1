#!/usr/bin/env python
# $LicenseInfo:firstyear=2010&license=mit$
# Copyright (c) 2010, Linden Research, Inc.
# $/LicenseInfo$


import os

import autobuild_base
from common import get_current_platform, AutobuildError
import configfile


class autobuild_tool(autobuild_base.autobuild_base):
    def get_details(self):
        return dict(name=self.name_from_file(__file__),
            description="Manipulate manifest entries to the autobuild configuration.")
     
    def register(self, parser):
        parser.add_argument('--config-file',
            dest='config_file',
            default=configfile.AUTOBUILD_CONFIG_FILE,
            help="")
        parser.add_argument('--platform','-p', default=get_current_platform(),
            help="the platform manifest to manipulate")
        parser.add_argument('command', nargs='?', default='print',
            help="manifest command: add, remove, clear, or print")
        parser.add_argument('pattern', nargs='*', help='a file pattern')

    def run(self, args):
        config = configfile.ConfigurationDescription(args.config_file)
        if args.command == 'add':
            [add(config, args.platform, p) for p in args.pattern]
        elif args.command == 'remove':
            [remove(config, args.platform, p) for p in args.pattern]
        elif args.command == 'clear':
            clear(config, args.platform)
        elif args.command == 'print':
            print_manifest(config, args.platform)
        else:
            raise ManifestError('unknown command %s' % args.command)
        if args.dry_run is not None and not args.dry_run:
            config.save()


class ManifestError(AutobuildError):
	pass


def add(config, platform_name, pattern):
    """
    Adds a pattern to the giving platform's manifest.
    """
    platform_description = config.get_platform(platform_name)
    platform_description.manifest.append(pattern)


def remove(config, platform_name, pattern):
    """
    Removes first occurance of a pattern in the manifest which is equivalent to the given pattern.
    """
    platform_description = config.get_platform(platform_name)
    try:
        platform_description.manifest.remove(pattern)
    except:
        pass


def clear(config, platform_name):
    """
    Clears all entries from the manifest list.
    """
    config.get_platform(platform_name).manifest = []


def print_manifest(config, platform_name):
    """
    Prints the platform's manifest.
    """
    for pattern in config.get_platform(platform_name).manifest:
        print pattern


if __name__ == "__main__":
    sys.exit( autobuild_tool().main( sys.argv[1:] ) )
