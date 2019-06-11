import datetime
import ipaddress
import unittest
import uuid

import arrow
import faker

from pgdumplib import constants, converters


class TestCase(unittest.TestCase):

    def test_data_converter(self):
        data = []
        for row in range(0, 10):
            data.append([
                str(row),
                str(uuid.uuid4()),
                str(datetime.datetime.utcnow()),
                str(uuid.uuid4()),
                str(uuid.uuid4()),
                None
            ])

        converter = converters.DataConverter()
        for offset, expectation in enumerate(data):
            line = '\t'.join(['\\N' if e is None else e for e in expectation])
            self.assertListEqual(list(converter.convert(line)), expectation)

    def test_smart_data_converter(self):
        fake = faker.Faker()
        data = []
        for row in range(0, 10):
            data.append([
                row,
                None,
                fake.pydecimal(positive=True, left_digits=5, right_digits=3),
                uuid.uuid4(),
                ipaddress.IPv4Network(fake.ipv4(True)),
                ipaddress.IPv4Address(fake.ipv4()),
                ipaddress.IPv6Address(fake.ipv6()),
                arrow.get(arrow.now().to('America/Los_Angeles').strftime(
                    constants.PGDUMP_STRFTIME_FMT)).datetime
            ])

        def convert(value):
            """Convert the value to the proper string type"""
            if value is None:
                return '\\N'
            elif isinstance(value, datetime.datetime):
                return value.strftime(constants.PGDUMP_STRFTIME_FMT)
            return str(value)

        converter = converters.SmartDataConverter()
        for offset, expectation in enumerate(data):
            line = '\t'.join([convert(e) for e in expectation])
            row = list(converter.convert(line))
            self.assertListEqual(row, expectation)
