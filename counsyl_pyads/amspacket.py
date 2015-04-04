from .adsconnection import AdsConnection
from .binaryparser import BinaryParser
from .adsutils import HexBlock


class AmsPacket(object):
    """An incoming or outgoing communications packet in the Ams protocol"""

    def __init__(self, connection):
        """Constructor for packet. Because the header information is specific
        to an connection, the connection argument must be an instance of
        AdsConnection.
        """
        assert(isinstance(connection, AdsConnection))
        # the ams-net-id of the destination device (6 bytes)
        self.target_ams_id = connection.target_ams_id
        # the ams-port to use (2 bytes, UInt16)
        self.target_ams_port = connection.target_ams_port
        # the ams-net-id of the sender device (6 bytes)
        self.source_ams_id = connection.source_ams_id
        # the ams-port of the sender (2 bytes, UInt16)
        self.source_ams_port = connection.source_ams_port

        # command-id (2 bytes, UInt16)
        self.command_id = 0
        # state flags, i.e. 0x0004 for request. (2 bytes, UInt16)
        self.state_flags = 0
        # length of data (4 bytes, UInt32)
        self.Length = 0
        # error code of ads-response (4 bytes, UInt32)
        self.error_code = 0
        # arbitrary number to identify request<->response (4 bytes, UInt32)
        self.invoke_id = 0
        # the ADS-data to transmit as payload of the AMS packet
        self.data = b''

    @staticmethod
    def ams_id_to_bytes(dotted_decimal):
        return map(int, dotted_decimal.split('.'))

    @staticmethod
    def ams_id_from_bytes(byteList):
        words = []

        for bt in byteList:
            words.append("%s" % ord(bt))

        return ".".join(words)

    def GetBinaryData(self):
        binary = BinaryParser()

        # ams-target id & port
        binary.WriteBytes(AmsPacket.ams_id_to_bytes(self.target_ams_id))
        binary.WriteUInt16(self.target_ams_port)

        # ams-source id & port
        binary.WriteBytes(AmsPacket.ams_id_to_bytes(self.source_ams_id))
        binary.WriteUInt16(self.source_ams_port)

        # command id, state flags & data length
        binary.WriteUInt16(self.command_id)
        binary.WriteUInt16(self.state_flags)
        binary.WriteUInt32(len(self.data))

        # error code & invoke id
        binary.WriteUInt32(self.error_code)
        binary.WriteUInt32(self.invoke_id)

        # last but not least - the data
        binary.WriteBytes(self.data)

        # return byte buffer
        return binary.ByteData

    @staticmethod
    def from_binary_data(data=''):
        binary = BinaryParser(data)

        # ams target & source
        target_ams_id = AmsPacket.ams_id_from_bytes(binary.ReadBytes(6))
        target_ams_port = binary.ReadUInt16()
        source_ams_id = AmsPacket.ams_id_from_bytes(binary.ReadBytes(6))
        source_ams_port = binary.ReadUInt16()

        ads_conn = AdsConnection(
            target_ams="%s:%s" % (target_ams_id, target_ams_port),
            source_ams="%s:%s" % (source_ams_id, source_ams_port),
        )

        packet = AmsPacket(ads_conn)

        packet.command_id = binary.ReadUInt16()
        packet.state_flags = binary.ReadUInt16()
        packet.Length = binary.ReadUInt32()
        packet.error_code = binary.ReadUInt32()
        packet.invoke_id = binary.ReadUInt32()
        packet.data = binary.ByteData[32:]

        return packet

    def __str__(self):
        result = "%s:%s --> " % (self.source_ams_id, self.source_ams_port)
        result += "%s:%s\n" % (self.target_ams_id, self.target_ams_port)
        result += "Command ID:  %s\n" % self.command_id
        result += "Invoke ID:   %s\n" % self.invoke_id
        result += "State Flags: %s\n" % self.state_flags
        result += "Data Length: %s\n" % self.Length
        result += "Error:       %s\n" % self.error_code

        if (len(self.data) == 0):
            result += "Packet contains no data.\n"
        else:
            result += "Data:\n%s\n" % HexBlock(self.data)

        return result
