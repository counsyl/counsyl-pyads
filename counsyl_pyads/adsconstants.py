"""Collection of all documented ADS constants. Only a small subset of these
are used by code in this library.

Source: http://infosys.beckhoff.com/english.php?content=../content/1033/tcplclibsystem/html/tcplclibsys_constants.htm&id=  # nopep8
"""


"""Port numbers"""
# Port number of the standard loggers.
AMSPORT_LOGGER = 100
# Port number of the TwinCAT Eventloggers.
AMSPORT_EVENTLOG = 110
# Port number of the TwinCAT Realtime Servers.
AMSPORT_R0_RTIME = 200
# Port number of the TwinCAT I/O Servers.
AMSPORT_R0_IO = 300
# Port number of the TwinCAT NC Servers.
AMSPORT_R0_NC = 500
# Port number of the TwinCAT NC Servers (Task SAF).
AMSPORT_R0_NCSAF = 501
# Port number of the TwinCAT NC Servers (Task SVB).
AMSPORT_R0_NCSVB = 511
# internal
AMSPORT_R0_ISG = 550
# Port number of the TwinCAT NC I Servers.
AMSPORT_R0_CNC = 600
# internal
AMSPORT_R0_LINE = 700
# Port number of the TwinCAT PLC Servers (only at the Buscontroller).
AMSPORT_R0_PLC = 800
# Port number of the TwinCAT PLC Servers in the runtime 1.
AMSPORT_R0_PLC_RTS1 = 801
# Port number of the TwinCAT PLC Servers in the runtime 2.
AMSPORT_R0_PLC_RTS2 = 811
# Port number of the TwinCAT PLC Servers in the runtime 3.
AMSPORT_R0_PLC_RTS3 = 821
# Port number of the TwinCAT PLC Servers in the runtime 4.
AMSPORT_R0_PLC_RTS4 = 831
# Port number of the TwinCAT CAM Server.
AMSPORT_R0_CAM = 900
# Port number of the TwinCAT CAMTOOL Server.
AMSPORT_R0_CAMTOOL = 950
#   Port number of the TwinCAT  System Service.
AMSPORT_R3_SYSSERV = 10000
#   Port number of the TwinCAT Scope Servers (since Lib. V2.0.12)
AMSPORT_R3_SCOPESERVER = 27110


"""ADS States"""
ADSSTATE_INVALID = 0  # ADS Status: invalid
ADSSTATE_IDLE = 1  # ADS Status: idle
ADSSTATE_RESET = 2  # ADS Status: reset.
ADSSTATE_INIT = 3  # ADS Status: init
ADSSTATE_START = 4  # ADS Status: start
ADSSTATE_RUN = 5  # ADS Status: run
ADSSTATE_STOP = 6  # ADS Status: stop
ADSSTATE_SAVECFG = 7  # ADS Status: save configuration
ADSSTATE_LOADCFG = 8  # ADS Status: load configuration
ADSSTATE_POWERFAILURE = 9  # ADS Status: Power failure
ADSSTATE_POWERGOOD = 10  # ADS Status: Power good
ADSSTATE_ERROR = 11  # ADS Status: Error
ADSSTATE_SHUTDOWN = 12  # ADS Status: Shutdown
ADSSTATE_SUSPEND = 13  # ADS Status: Suspend
ADSSTATE_RESUME = 14  # ADS Status: Resume
ADSSTATE_CONFIG = 15  # ADS Status: Configuration
ADSSTATE_RECONFIG = 16  # ADS Status: Reconfiguration
ADSSTATE_MAXSTATES = 17


"""Reserved Index Groups"""
ADSIGRP_SYMTAB = 0xF000
ADSIGRP_SYMNAME = 0xF001
ADSIGRP_SYMVAL = 0xF002
ADSIGRP_SYM_HNDBYNAME = 0xF003
ADSIGRP_SYM_VALBYNAME = 0xF004
ADSIGRP_SYM_VALBYHND = 0xF005
ADSIGRP_SYM_RELEASEHND = 0xF006
ADSIGRP_SYM_INFOBYNAME = 0xF007
ADSIGRP_SYM_VERSION = 0xF008
ADSIGRP_SYM_INFOBYNAMEEX = 0xF009
ADSIGRP_SYM_DOWNLOAD = 0xF00A
ADSIGRP_SYM_UPLOAD = 0xF00B
ADSIGRP_SYM_UPLOADINFO = 0xF00C
ADSIGRP_SYMNOTE = 0xF010
ADSIGRP_IOIMAGE_RWIB = 0xF020
ADSIGRP_IOIMAGE_RWIX = 0xF021
ADSIGRP_IOIMAGE_RISIZE = 0xF025
ADSIGRP_IOIMAGE_RWOB = 0xF030
ADSIGRP_IOIMAGE_RWOX = 0xF031
ADSIGRP_IOIMAGE_RWOSIZE = 0xF035
ADSIGRP_IOIMAGE_CLEARI = 0xF040
ADSIGRP_IOIMAGE_CLEARO = 0xF050
ADSIGRP_IOIMAGE_RWIOB = 0xF060
ADSIGRP_DEVICE_DATA = 0xF100
ADSIOFFS_DEVDATA_ADSSTATE = 0x0000
ADSIOFFS_DEVDATA_DEVSTATE = 0x0002


"""System Service Index Groups"""
SYSTEMSERVICE_OPENCREATE = 100
SYSTEMSERVICE_OPENREAD = 101
SYSTEMSERVICE_OPENWRITE = 102
SYSTEMSERVICE_CREATEFILE = 110
SYSTEMSERVICE_CLOSEHANDLE = 111
SYSTEMSERVICE_FOPEN = 120
SYSTEMSERVICE_FCLOSE = 121
SYSTEMSERVICE_FREAD = 122
SYSTEMSERVICE_FWRITE = 123
SYSTEMSERVICE_FSEEK = 124
SYSTEMSERVICE_FTELL = 125
SYSTEMSERVICE_FGETS = 126
SYSTEMSERVICE_FPUTS = 127
SYSTEMSERVICE_FSCANF = 128
SYSTEMSERVICE_FPRINTF = 129
SYSTEMSERVICE_FEOF = 130
SYSTEMSERVICE_FDELETE = 131
SYSTEMSERVICE_FRENAME = 132
SYSTEMSERVICE_REG_HKEYLOCALMACHINE = 200
SYSTEMSERVICE_SENDEMAIL = 300
SYSTEMSERVICE_TIMESERVICES = 400
SYSTEMSERVICE_STARTPROCESS = 500
SYSTEMSERVICE_CHANGENETID = 600


"""System Service Index Offsets (Timeservices)"""
TIMESERVICE_DATEANDTIME = 1
TIMESERVICE_SYSTEMTIMES = 2
TIMESERVICE_RTCTIMEDIFF = 3
TIMESERVICE_ADJUSTTIMETORTC = 4


"""Masks for Log output"""
ADSLOG_MSGTYPE_HINT = 0x01
ADSLOG_MSGTYPE_WARN = 0x02
ADSLOG_MSGTYPE_ERROR = 0x04
ADSLOG_MSGTYPE_LOG = 0x10
ADSLOG_MSGTYPE_MSGBOX = 0x20
ADSLOG_MSGTYPE_RESOURCE = 0x40
ADSLOG_MSGTYPE_STRING = 0x80


"""Masks for Bootdata-Flagsx"""
BOOTDATAFLAGS_RETAIN_LOADED = 0x01
BOOTDATAFLAGS_RETAIN_INVALID = 0x02
BOOTDATAFLAGS_RETAIN_REQUESTED = 0x04
BOOTDATAFLAGS_PERSISTENT_LOADED = 0x10
BOOTDATAFLAGS_PERSISTENT_INVALID = 0x20


"""Masks for BSOD-Flags"""
SYSTEMSTATEFLAGS_BSOD = 0x01  # BSOD: Blue Screen of Death
SYSTEMSTATEFLAGS_RTVIOLATION = 0x02  # Realtime violation, latency time overrun


"""Masks for File output"""
# 'r': Opens file for reading
FOPEN_MODEREAD = 0x0001
# 'w': Opens file for writing, (possible) existing files were overwritten.
FOPEN_MODEWRITE = 0x0002
# 'a': Opens file for writing, is attached to (possible) exisiting files. If no
# file exists, it will be created.
FOPEN_MODEAPPEND = 0x0004
# '+': Opens a file for reading and writing.
FOPEN_MODEPLUS = 0x0008
# 'b': Opens a file for binary reading and writing.
FOPEN_MODEBINARY = 0x0010
# 't': Opens a file for textual reading and writing.
FOPEN_MODETEXT = 0x0020


"""Masks for Eventlogger Flags"""
# Class and priority are defined by the formatter.
TCEVENTFLAG_PRIOCLASS = 0x0010
# The formatting information comes with the event
TCEVENTFLAG_FMTSELF = 0x0020
# Logg.
TCEVENTFLAG_LOG = 0x0040
# Show message box .
TCEVENTFLAG_MSGBOX = 0x0080
# Use Source-Id instead of Source name.
TCEVENTFLAG_SRCID = 0x0100


"""TwinCAT Eventlogger Status messages"""
# Not valid, occurs also if the event was not reported.
TCEVENTSTATE_INVALID = 0x0000
# Event is reported, but neither signed off nor acknowledged.
TCEVENTSTATE_SIGNALED = 0x0001
# Event is signed off ('gone').
TCEVENTSTATE_RESET = 0x0002
# Event is acknowledged.
TCEVENTSTATE_CONFIRMED = 0x0010
# Event is signed off  and acknowledged.
TCEVENTSTATE_RESETCON = 0x0012


"""TwinCAT Eventlogger Status messages"""
TCEVENT_SRCNAMESIZE = 15  # Max. Length for the Source name.
TCEVENT_FMTPRGSIZE = 31  # Max. Length for the name of the formatters.


"""Other"""
PI = 3.1415926535897932384626433832795  # Pi number
DEFAULT_ADS_TIMEOUT = 5  # (seconds) Default ADS timeout
MAX_STRING_LENGTH = 255  # The max. string length of T_MaxString data type
