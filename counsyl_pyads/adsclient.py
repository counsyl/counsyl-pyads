import logging
import select
import socket
import struct
import threading
import time

from .amspacket import AmsPacket
from .adsdatatypes import AdsDatatype
from .adsexception import AdsException
from .adssymbol import AdsSymbol

from .adscommands import DeviceInfoCommand
from .adscommands import ReadCommand
from .adscommands import ReadStateCommand
from .adscommands import ReadWriteCommand
from .adscommands import WriteCommand
from .adscommands import WriteControlCommand


ADS_CHUNK_SIZE_DEFAULT = 1024
ADS_PORT_DEFAULT = 0xBF02


logger = logging.getLogger(__name__)


class AdsClient(object):
    def __init__(self, ads_connection, debug=False):
        self.ads_connection = ads_connection
        # default values
        self.debug = debug
        self.ads_index_group_in = 0xF020
        self.ads_index_group_out = 0xF030
        self.socket = None
        self._current_invoke_id = 0x8000
        self._current_packet = None
        # event to signal shutdown to async reader thread
        self._stop_reading = threading.Event()

    # BEGIN Connection Management Functions

    @property
    def is_connected(self):
        return self.socket is not None

    def close(self):
        if (self.socket is not None):
            # stop async reading thread
            self._stop_reading.set()
            try:
                self._async_read_thread.join()
            except RuntimeError:
                # ignore Runtime error raised if thread doesn't exist
                pass
            # close socket
            self.socket.close()
            self.socket = None

    def connect(self):
        self.close()
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.settimeout(2)
        try:
            self.socket.connect(
                (self.ads_connection.target_ip, ADS_PORT_DEFAULT))
        except Exception as ex:
            raise Exception("Could not connect to device: {ex}".format(ex=ex))

        try:
            # start reading thread
            self._stop_reading.clear()
            self._async_read_thread = threading.Thread(
                target=self._async_read_fn)
            self._async_read_thread.daemon = True
            self._async_read_thread.start()
        except Exception as ex:
            raise Exception("Could not start read thread: {ex}".format(ex=ex))

    def _async_read_fn(self):
        while not self._stop_reading.is_set():
            ready = select.select([self.socket], [], [], 0.1)
            if ready[0] and self.is_connected:
                try:
                    newPacket = self.read_ams_packet_from_socket()
                    if (newPacket.InvokeID == self._current_invoke_id):
                        self._current_packet = newPacket
                    else:
                        logger.debug("Packet dropped: %s" % newPacket)
                except socket.error:
                    self.close()
                    break

    def __enter__(self):
        return self

    def __exit__(self, ex_type, ex_value, traceback):
        if (ex_type is not None):
            logger.warning(
                "AdsClient exiting with exception: {ex_type}, {ex_value}. "
                "{traceback}".format(
                    ex_type=ex_type,
                    ex_value=ex_value or '',
                    traceback=traceback or ''))
        try:
            self.close()
        except:
            pass

    # END Connection Management Methods

    # BEGIN Read/Write Methods

    def execute(self, command):
        # create packet
        packet = command.to_ams_packet(self.ads_connection)
        # send to client
        responsePacket = self.send_and_recv(packet)
        # check for error
        if (responsePacket.ErrorCode > 0):
            raise AdsException(responsePacket.ErrorCode)
        # return response object
        result = command.CreateResponse(responsePacket)
        if (result.Error > 0):
            raise AdsException(result.Error)
        return result

    def read_device_info(self):
        cmd = DeviceInfoCommand()
        resp = self.execute(cmd)
        return {
            'major_version': unicode(resp.MajorVersion),
            'minor_version': unicode(resp.MinorVersion),
            'build': unicode(resp.Build),
            'device_name': unicode(resp.DeviceName),
        }

    def read(self, indexGroup, indexOffset, length):
        cmd = ReadCommand(indexGroup, indexOffset, length)
        return self.execute(cmd)

    def write(self, indexGroup, indexOffset, data):
        cmd = WriteCommand(indexGroup, indexOffset, data)
        return self.execute(cmd)

    def read_state(self):
        cmd = ReadStateCommand().execute(self)
        return self.execute(cmd)

    def write_control(self, adsState, deviceState, data=''):
        cmd = WriteControlCommand(adsState, deviceState, data)
        return self.execute(cmd)

    def read_write(self, indexGroup, indexOffset, readLen, dataToWrite=''):
        cmd = ReadWriteCommand(indexGroup, indexOffset, readLen, dataToWrite)
        return self.execute(cmd)

    # END Read/Write Methods

    # BEGIN variable access methods

    def get_symbol_handle(self, var_name):
        """Retrieves the internal handle of a symbol identified by symbol name.

        var_name: is of type unicode (or str if only ASCII characters are used)
            Both fully qualified PLC symbol names (e.g. including leading "."
            for global variables) or PLC variable names (the name used in the
            PLC program) are accepted. Names are NoT case-sensitive because the
            PLC converts all variables to all-uppercase internally.
        """
        # convert unicode or ascii input to the Windows-1252 encoding used by
        # the plc
        var_name_enc = var_name.encode('windows-1252')
        symbol = self.read_write(
            indexGroup=0xF003,
            indexOffset=0x0000,
            readLen=4,
            dataToWrite=var_name_enc + '\x00')
        return struct.unpack("I", symbol.Data)[0]

    def read_by_handle(self, symbolHandle, ads_data_type):
        """Retrieves the current value of a symbol identified by its handle.

        ads_data_type: The data type of the symbol must be specified as
            AdsDatatype object.
        """
        assert(isinstance(ads_data_type, AdsDatatype))
        response = self.read(
            indexGroup=0xF005,
            indexOffset=symbolHandle,
            length=ads_data_type.byte_count)
        data = response.Data
        return ads_data_type.unpack(data)

    def read_by_name(self, var_name, ads_data_type):
        """Retrieves the current value of a symbol identified by symbol name.

        This simply calls get_symbol_handle() first and then uses the handle to
        call read_by_handle().

        var_name: must meet the same requirements as in get_symbol_handle, i.e.
            be unicode or an ASCII-only str.
        ads_data_type: must meet the same requirements as in read_by_handle.
        """
        symbol_handle = self.get_symbol_handle(var_name)
        return self.read_by_handle(symbol_handle, ads_data_type)

    def write_by_handle(self, symbolHandle, ads_data_type, value):
        """Retrieves the current value of a symbol identified by its handle.

        ads_data_type: The data type of the symbol must be specified as
            AdsDatatype object.
        value: must meet the requirements of the ads_data_type. For example,
            integer datatypes will require a number to be passed, etc.
        """
        assert(isinstance(ads_data_type, AdsDatatype))
        value_raw = ads_data_type.pack(value)
        self.write(
            indexGroup=0xF005,
            indexOffset=symbolHandle,
            data=value_raw)

    def write_by_name(self, var_name, ads_data_type, value):
        """Sets the current value of a symbol identified by symbol name.

        This simply calls get_symbol_handle() first and then uses the handle to
        call write_by_handle().

        var_name: must meet the same requirements as in get_symbol_handle, i.e.
            be unicode or an ASCII-only str.
        ads_data_type: must meet the same requirements as in write_by_handle.
        value: must meet the requirements of the ads_data_type. For example,
            integer datatypes will require a number to be passed, etc.
        """
        symbol_handle = self.get_symbol_handle(var_name)
        self.write_by_handle(symbol_handle, ads_data_type, value)

    def get_symbols(self):
        # Figure out the length of the symbol table first
        resp1 = self.read(
            indexGroup=0xF00F,
            indexOffset=0x0000,
            length=24)
        sym_count = struct.unpack("I", resp1.Data[0:4])[0]
        sym_list_length = struct.unpack("I", resp1.Data[4:8])[0]

        # Get the symbol table
        resp2 = self.read(
            indexGroup=0x0000F00B,
            indexOffset=0x00000000,
            length=sym_list_length)

        ptr = 0
        symbols = []
        for idx in xrange(sym_count):
            read_length = struct.unpack("I", resp2.Data[ptr+0:ptr+4])[0]
            index_group = struct.unpack("I", resp2.Data[ptr+4:ptr+8])[0]
            index_offset = struct.unpack("I", resp2.Data[ptr+8:ptr+12])[0]
            name_length = struct.unpack("H", resp2.Data[ptr+24:ptr+26])[0]
            type_length = struct.unpack("H", resp2.Data[ptr+26:ptr+28])[0]
            comment_length = struct.unpack("H", resp2.Data[ptr+28:ptr+30])[0]

            name_start_ptr = ptr + 30
            name_end_ptr = name_start_ptr + name_length
            type_start_ptr = name_end_ptr + 1
            type_end_ptr = type_start_ptr + type_length
            comment_start_ptr = type_end_ptr + 1
            comment_end_ptr = comment_start_ptr + comment_length

            name = resp2.Data[name_start_ptr:name_end_ptr]
            symtype = resp2.Data[type_start_ptr:type_end_ptr]
            comment = resp2.Data[comment_start_ptr:comment_end_ptr]

            ptr = comment_end_ptr + 1

            symbol = AdsSymbol(
                read_length, index_group, index_offset, name, symtype, comment)

            symbols.append(symbol)

        return symbols

    # END variable access methods

    def read_ams_packet_from_socket(self):
        # read default buffer
        response = self.socket.recv(ADS_CHUNK_SIZE_DEFAULT)
        # ensure correct beckhoff tcp header
        if(len(response) < 6):
            return None
        # first two bits must be 0
        if (response[0:2] != b'\x00\x00'):
            return None
        # read whole data length
        dataLen = struct.unpack('I', response[2:6])[0] + 6
        # read rest of data, if any
        while (len(response) < dataLen):
            nextReadLen = min(ADS_CHUNK_SIZE_DEFAULT, dataLen - len(response))
            response += self.socket.recv(nextReadLen)
        # cut off tcp-header and return response amspacket
        return AmsPacket.from_binary_data(response[6:])

    def get_tcp_header(self, amsData):
        # pack 2 bytes (reserved) and 4 bytes (length)
        # format _must_ be little endian!
        return struct.pack('<HI', 0, len(amsData))

    def get_tcp_packet(self, amspacket):
        # get ams-data and generate tcp-header
        amsData = amspacket.GetBinaryData()
        tcpHeader = self.get_tcp_header(amsData)
        return tcpHeader + amsData

    def send_and_recv(self, amspacket):
        if not self.is_connected:
            self.connect()
        # prepare packet with invoke id
        self.prepare_command_invoke(amspacket)
        # send tcp-header and ams-data
        self.socket.send(self.get_tcp_packet(amspacket))
        # here's your packet
        return self.await_command_invoke()

    def prepare_command_invoke(self, amspacket):
        if(self._current_invoke_id < 0xFFFF):
            self._current_invoke_id += 1
        else:
            self._current_invoke_id = 0x8000
        self._current_packet = None
        amspacket.InvokeID = self._current_invoke_id
        if self.debug:
            logger.debug(">>> sending ams-packet:")
            logger.debug(amspacket)

    def await_command_invoke(self):
        # unfortunately threading.event is slower than this oldschool poll :-(
        timeout = 0
        while (self._current_packet is None):
            timeout += 0.001
            time.sleep(0.001)
            if (timeout > 10):
                raise AdsException("Timout: Did not receive ADS Answer!")
        if self.debug:
            logger.debug("<<< received ams-packet:")
            logger.debug(self._current_packet)
        return self._current_packet
