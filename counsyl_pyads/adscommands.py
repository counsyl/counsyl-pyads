import ctypes
import struct

from . import PYADS_ENCODING
from .adsutils import HexBlock
from .amspacket import AmsPacket
from .adsexception import AdsException


class AdsCommand(object):
    def __init__(self):
        pass

    CommandID = 0

    def CreateRequest(self):
        raise NotImplementedError()

    def CreateResponse(self, responsePacket):
        raise NotImplementedError()

    def to_ams_packet(self, adsConnection):
        packet = AmsPacket(adsConnection)
        packet.CommandID = self.CommandID
        packet.StateFlags = 0x0004
        packet.Data = self.CreateRequest()

        return packet


class AdsResponse(object):
    def __init__(self, responseAmsPacket):
        self.Error = struct.unpack_from('I', responseAmsPacket.Data)[0]

        if (self.Error > 0):
            raise AdsException(self.Error)


class DeviceInfoCommand(AdsCommand):
    def __init__(self):
        self.CommandID = 0x0001

    def CreateRequest(self):
        return b''

    def CreateResponse(self, responsePacket):
        return DeviceInfoResponse(responsePacket)


class DeviceInfoResponse(AdsResponse):
    def __init__(self, responseAmsPacket):
        super(DeviceInfoResponse, self).__init__(responseAmsPacket)

        self.MajorVersion = struct.unpack_from(
            'B', responseAmsPacket.Data, 4)[0]
        self.MinorVersion = struct.unpack_from(
            'B', responseAmsPacket.Data, 5)[0]
        self.Build = struct.unpack_from(
            'H', responseAmsPacket.Data, 6)[0]

        deviceNameEnd = 16
        for i in range(8, 24):
            if ord(responseAmsPacket.Data[i]) == 0:
                deviceNameEnd = i
                break

        deviceNameRaw = responseAmsPacket.Data[8:deviceNameEnd]
        self.DeviceName = deviceNameRaw.decode(PYADS_ENCODING).strip(' \t\n\r')

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
        self.CommandID = 0x0002
        self.IndexGroup = indexGroup
        self.IndexOffset = indexOffset
        self.Length = length

    def CreateRequest(self):
        return struct.pack(
            '<III', self.IndexGroup, self.IndexOffset, self.Length)

    def CreateResponse(self, responsePacket):
        return ReadResponse(responsePacket)


class ReadResponse(AdsResponse):
    def __init__(self, responseAmsPacket):
        super(ReadResponse, self).__init__(responseAmsPacket)

        self.Length = struct.unpack_from('I', responseAmsPacket.Data, 4)[0]
        self.Data = responseAmsPacket.Data[8:]

    def CreateBuffer(self):
        return ctypes.create_string_buffer(self.Data, len(self.Data))

    def __str__(self):
        return unicode(self).encode('utf-8')

    def __unicode__(self):
        return u"AdsReadResponse:\n%s" % HexBlock(self.Data)


class ReadStateCommand(AdsCommand):
    def __init__(self):
        self.CommandID = 0x0004

    def CreateRequest(self):
        return ''

    def CreateResponse(self, responsePacket):
        return ReadStateResponse(responsePacket)


class ReadStateResponse(AdsResponse):
    def __init__(self, responseAmsPacket):
        super(ReadStateResponse, self).__init__(responseAmsPacket)

        self.AdsState = struct.unpack_from(
            'H', responseAmsPacket.Data, 4)[0]
        self.DeviceState = struct.unpack_from(
            'H', responseAmsPacket.Data, 6)[0]

    def __str__(self):
        return unicode(self).encode('utf-8')

    def __unicode__(self):
        return u"Ads/Device State: %s/%s" % (self.AdsState, self.DeviceState)


class ReadWriteCommand(AdsCommand):
    def __init__(self, indexGroup, indexOffset, readLen, dataToWrite=''):
        self.CommandID = 0x0009
        self.IndexGroup = indexGroup
        self.IndexOffset = indexOffset
        self.ReadLen = readLen
        self.Data = dataToWrite

    def CreateRequest(self):
        result = struct.pack('<II', self.IndexGroup, self.IndexOffset)
        result += struct.pack('<II', self.ReadLen, len(self.Data))
        result += self.Data
        return result

    def CreateResponse(self, responsePacket):
        return ReadWriteResponse(responsePacket)


class ReadWriteResponse(AdsResponse):
    def __init__(self, responseAmsPacket):
        super(ReadWriteResponse, self).__init__(responseAmsPacket)

        self.Length = struct.unpack_from('I', responseAmsPacket.Data, 4)[0]
        self.Data = responseAmsPacket.Data[8:]

    def __str__(self):
        return unicode(self).encode('utf-8')

    def __unicode__(self):
        return (
            u"AdsReadWriteResponse:\n%s" %
            AmsPacket.GetHexStringBlock(self.Data))


class WriteCommand(AdsCommand):
    def __init__(self, indexGroup, indexOffset, data):
        self.CommandID = 0x0003
        self.IndexGroup = indexGroup
        self.IndexOffset = indexOffset
        self.Data = data

    def CreateRequest(self):
        result = struct.pack(
            '<III', self.IndexGroup, self.IndexOffset, len(self.Data))
        result += self.Data
        return result

    def CreateResponse(self, responsePacket):
        return WriteResponse(responsePacket)


class WriteResponse(AdsResponse):
    def __init__(self, responseAmsPacket):
        super(WriteResponse, self).__init__(responseAmsPacket)


class WriteControlCommand(AdsCommand):
    def __init__(self, adsState, deviceState, data=''):
        self.CommandID = 0x0005
        self.AdsState = adsState
        self.DeviceState = deviceState
        self.Data = data

    def CreateRequest(self):
        result = struct.pack(
            '<HHI', self.AdsState, self.DeviceState, len(self.Data))
        result += self.Data
        return result

    def CreateResponse(self, responsePacket):
        return WriteControlResponse(responsePacket)


class WriteControlResponse(AdsResponse):
    def __init__(self, responseAmsPacket):
        super(WriteControlResponse, self).__init__(responseAmsPacket)
