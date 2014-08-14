import time
import datetime
import urllib
import urllib.request

import ntplib

NTP_SERVER = "europe.pool.ntp.org"

class TimeSynchronization:

    def check_connectivity(self):
        try:
            urllib.request.urlopen(NTP_SERVER, timeout=1)
            return True
        except:
            #urllib.request.error
            return False

#TODO check connectivity for the ntp server
    def sync_clock_ntp(self):
        self.client = ntplib.NTPClient()
        self.response = self.client.request(NTP_SERVER, version = 3)
        self.date_and_time = time.strptime(time.ctime(self.response.tx_time),
                                "%a %b %d %H:%M:%S %Y")
        return self.date_and_time

    def sync_clock_local(self):
        return time.localtime()


res = TimeSynchronization();
print(res.sync_clock_ntp())