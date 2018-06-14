import argparse
import logging
import pprint

from pgdumplib import toc


class Archive:

    def __init__(self, directory):
        self.directory = directory
        self.toc = toc.ToC('{}/toc.dat'.format(directory))

    @property
    def dbname(self):
        return self.toc.dbname

    @property
    def dump_version(self):
        return self.toc.dump_version

    @property
    def server_version(self):
        return self.toc.server_version

    @property
    def timestamp(self):
        return self.toc.timestamp


def parse_cli_args():
    parser = argparse.ArgumentParser(
        description='Convert PostgreSQL pg_dump -Fd backups to Avro')
    parser.add_argument(
        'directory', metavar='DIR', nargs=1,
        help='Path to the directory containing the backup')

    parser.add_argument('-d', '--debug', action='store_true')
    parser.add_argument('-v', '--verbose', action='store_true')
    return parser.parse_args()


def main():
    args = parse_cli_args()
    level = logging.WARNING
    if args.debug is True:
        level = logging.DEBUG
    elif args.verbose is True:
        level = logging.INFO
    logging.basicConfig(level=level)

    reader = Archive(args.directory[0])
    print('Header: {}'.format(reader.toc.header))
    print('Database: {}'.format(reader.toc.dbname))
    print('Archive Timestamp: {}'.format(reader.timestamp))
    print('Server Version: {}'.format(reader.server_version))
    print('Dump Version: {}'.format(reader.dump_version))
    for dump_id, entry in reader.toc.entries.items():
        if entry.section == 'Data' and entry.desc == 'TABLE DATA':
            pprint.pprint(entry)




if __name__ == '__main__':
    main()
