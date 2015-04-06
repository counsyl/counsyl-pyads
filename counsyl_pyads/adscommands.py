import ctypes
import struct

from .constants import PYADS_ENCODING
from .adsutils import HexBlock
from .amspacket import AmsPacket
from .adsexception import AdsException


class AdsCommand(object):
    def __init__(self):
        self.command_id = 0

    def CreateRequest(self):
        raise NotImplementedError()

    def CreateResponse(self, responsePacket):
        raise NotImplementedError()

    def to_ams_packet(self, adsConnection):
        packet = AmsPacket(adsConnection)
        packet.command_id = self.command_id
        packet.state_flags = 0x0004
        packet.data = self.CreateRequest()

        return packet


class AdsResponse(object):
    def __init__(self, responseAmsPacket):
        self.Error = struct.unpack_from('I', responseAmsPacket.data)[0]

        if (self.Error > 0):
            raise AdsException(self.Error)


class DeviceInfoCommand(AdsCommand):
    def __init__(self):
        super(DeviceInfoCommand, self).__init__()
        self.command_id = 0x0001

    def CreateRequest(self):
        return b''

    def CreateResponse(self, responsePacket):
        return DeviceInfoResponse(responsePacket)


class DeviceInfoResponse(AdsResponse):
    def __init__(self, responseAmsPacket):
        super(DeviceInfoResponse, self).__init__(responseAmsPacket)

        self.MajorVersion = struct.unpack_from(
            'B', responseAmsPacket.data, 4)[0]
        self.MinorVersion = struct.unpack_from(
            'B', responseAmsPacket.data, 5)[0]
        self.Build = struct.unpack_from(
            'H', responseAmsPacket.data, 6)[0]

        deviceNameEnd = 16
        for i in range(8, 24):
            if ord(responseAmsPacket.data[i]) == 0:
                deviceNameEnd = i
                break

        deviceNameRaw = responseAmsPacket.data[8:deviceNameEnd]
        self.DeviceName = deviceNameRaw.decode(
            PYADS_ENCODING).strip(' \t\n\r\0')

    @property
    def Version(self):
        return "%s.%s.%s" % (self.MajorVersion, self.MinorVersion, self.Build)

    def __str__(self):
        return unicode(self).encode('utf-8')

    def __unicode__(self):
        return u"%s (Version %s)" % (self.DeviceName, self.Version)


class ReadCommand(AdsCommand):
    def __init__(self, indexGroup, indexOffset, length):
        if not isinstance(indexOffset, int):
            raise TypeError('indexOffset argument must be integer')
        if not isinstance(length, int):
            raise TypeError('length argument must be integer')
        super(ReadCommand, self).__init__()
        self.command_id = 0x0002
        self.index_group = indexGroup
        self.index_offset = indexOffset
        self.length = length

    def CreateRequest(self):
        return struct.pack(
            '<III', self.index_group, self.index_offset, self.length)

    def CreateResponse(self, responsePacket):
        return ReadResponse(responsePacket)


class ReadResponse(AdsResponse):
    def __init__(self, responseAmsPacket):
        super(ReadResponse, self).__init__(responseAmsPacket)

        self.Length = struct.unpack_from('I', responseAmsPacket.data, 4)[0]
        self.data = responseAmsPacket.data[8:]

    def CreateBuffer(self):
        return ctypes.create_string_buffer(self.data, len(self.data))

    def __str__(self):
        return unicode(self).encode('utf-8')

    def __unicode__(self):
        return u"AdsReadResponse:\n%s" % HexBlock(self.data)


class ReadStateCommand(AdsCommand):
    def __init__(self):
        super(ReadStateCommand, self).__init__()
        self.command_id = 0x0004

    def CreateRequest(self):
        return ''

    def CreateResponse(self, responsePacket):
        return ReadStateResponse(responsePacket)


class ReadStateResponse(AdsResponse):
    def __init__(self, responseAmsPacket):
        super(ReadStateResponse, self).__init__(responseAmsPacket)

        self.AdsState = struct.unpack_from(
            'H', responseAmsPacket.data, 4)[0]
        self.DeviceState = struct.unpack_from(
            'H', responseAmsPacket.data, 6)[0]

    def __str__(self):
        return unicode(self).encode('utf-8')

    def __unicode__(self):
        return u"Ads/Device State: %s/%s" % (self.AdsState, self.DeviceState)


class ReadWriteCommand(AdsCommand):
    def __init__(self, indexGroup, indexOffset, readLen, dataToWrite=''):
        super(ReadWriteCommand, self).__init__()
        self.command_id = 0x0009
        self.index_group = indexGroup
        self.index_offset = indexOffset
        self.read_len = readLen
        self.data = dataToWrite

    def CreateRequest(self):
        result = struct.pack('<II', self.index_group, self.index_offset)
        result += struct.pack('<II', self.read_len, len(self.data))
        result += self.data
        return result

    def CreateResponse(self, responsePacket):
        return ReadWriteResponse(responsePacket)


class ReadWriteResponse(AdsResponse):
    def __init__(self, responseAmsPacket):
        super(ReadWriteResponse, self).__init__(responseAmsPacket)

        self.length = struct.unpack_from('I', responseAmsPacket.data, 4)[0]
        self.data = responseAmsPacket.data[8:]

    def __str__(self):
        return unicode(self).encode('utf-8')

    def __unicode__(self):
        return (
            u"AdsReadWriteResponse:\n%s" %
            AmsPacket.GetHexStringBlock(self.data))


class WriteCommand(AdsCommand):
    def __init__(self, indexGroup, indexOffset, data):
        super(WriteCommand, self).__init__()
        self.command_id = 0x0003
        self.index_group = indexGroup
        self.index_offset = indexOffset
        self.data = data

    def CreateRequest(self):
        result = struct.pack(
            '<III', self.index_group, self.index_offset, len(self.data))
        result += self.data
        return result

    def CreateResponse(self, responsePacket):
        return WriteResponse(responsePacket)


class WriteResponse(AdsResponse):
    def __init__(self, responseAmsPacket):
        super(WriteResponse, self).__init__(responseAmsPacket)


class WriteControlCommand(AdsCommand):
    def __init__(self, adsState, deviceState, data=''):
        super(WriteControlCommand, self).__init__()
        self.command_id = 0x0005
        self.AdsState = adsState
        self.DeviceState = deviceState
        self.data = data

    def CreateRequest(self):
        result = struct.pack(
            '<HHI', self.AdsState, self.DeviceState, len(self.data))
        result += self.data
        return result

    def CreateResponse(self, responsePacket):
        return WriteControlResponse(responsePacket)


class WriteControlResponse(AdsResponse):
    def __init__(self, responseAmsPacket):
        super(WriteControlResponse, self).__init__(responseAmsPacket)
