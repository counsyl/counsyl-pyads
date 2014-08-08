import re


class AdsConnection(object):
    """Container for parameters necessary to establish an Ads connection."""
    def __init__(
            self, target_ams, source_ams, target_ip=None, target_port=None):
        """
        target_ams, source_ams must be of format 0.0.0.0.0.0:0
        target_ip, target_port are derived from target_ams if not provided
        """
        target_ams_info = self.parse_ams(target_ams)

        self.target_ams_id = target_ams_info[0]
        self.target_ip = target_ip or target_ams_info[1]
        self.target_ams_port = target_port or target_ams_info[2]

        source_ams_info = self.parse_ams(source_ams)
        self.source_ams_id = source_ams_info[0]
        self.source_ams_port = source_ams_info[2]

    def parse_ams(self, amsconnection):
        pattern = '([0-9\.]+):([0-9]+){1}'
        match = re.match(pattern, amsconnection)
        if (match is None):
            raise Exception(
                "AmsId port format not valid. Expected format is "
                "'192.168.1.17.1.1:801'.")

        amsID = str(match.group(1))
        tcpIP = '.'.join(x for x in amsID.split('.')[:4])
        amsPort = int(match.group(2))

        return (amsID, tcpIP, amsPort)

    def __str__(self):
        return "%s:%s --> %s:%s" % (
            self.source_ams_id,
            self.target_ams_id,
            self.target_ams_port,
        )
