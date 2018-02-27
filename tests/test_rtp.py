from unittest import TestCase

from aiortc import rtp

from .utils import load


class RtpTest(TestCase):
    def test_no_ssrc(self):
        data = load('rtp.bin')
        packet = rtp.Packet.parse(data)
        self.assertEqual(packet.version, 2)
        self.assertEqual(packet.extension, 0)
        self.assertEqual(packet.marker, 0)
        self.assertEqual(packet.payload_type, 0)
        self.assertEqual(packet.sequence_number, 15743)
        self.assertEqual(packet.timestamp, 3937035252)
        self.assertEqual(packet.csrc, [])
        self.assertEqual(len(packet.payload), 160)
        self.assertEqual(bytes(packet), data)

    def test_with_csrc(self):
        data = load('rtp_with_csrc.bin')
        packet = rtp.Packet.parse(data)
        self.assertEqual(packet.version, 2)
        self.assertEqual(packet.extension, 0)
        self.assertEqual(packet.marker, 0)
        self.assertEqual(packet.payload_type, 0)
        self.assertEqual(packet.sequence_number, 16082)
        self.assertEqual(packet.timestamp, 144)
        self.assertEqual(packet.csrc, [2882400001, 3735928559])
        self.assertEqual(len(packet.payload), 160)
        self.assertEqual(bytes(packet), data)

    def test_truncated(self):
        data = load('rtp.bin')[0:11]
        with self.assertRaises(ValueError) as cm:
            rtp.Packet.parse(data)
        self.assertEqual(str(cm.exception), 'RTP packet length is less than 12 bytes')

    def test_bad_version(self):
        data = b'\xc0' + load('rtp.bin')[1:]
        with self.assertRaises(ValueError) as cm:
            rtp.Packet.parse(data)
        self.assertEqual(str(cm.exception), 'RTP packet has invalid version')
