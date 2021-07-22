import os
import time
import logging
import requests


logger = logging.getLogger("abstractapi")


class AbstractAPI(object):

    HOLIDAYS_API_KEY = os.environ.get("HOLIDAYS_API_KEY")
    IP_GEOLOCATION_API_KEY = os.environ.get("IP_GEOLOCATION_API_KEY")

    def _get(self, url, max_tries=5, **params):
        tries = 0
        while tries < max_tries:
            tries += 1
            try:
                response = requests.get(url, params=params)
                if response.ok:
                    return response.json()
            except Exception as e:
                logger.error("Failed getting response(%s): %s", url, e)
                time.sleep(5)
        return None

    def get_holiday_details(self, country_code, year, month, day):
        url = "https://holidays.abstractapi.com/v1/"
        return self._get(
            url=url,
            day=day,
            year=year,
            month=month,
            country=country_code,
            api_key=self.HOLIDAYS_API_KEY,
        )

    def get_geolocation_details(self, ip_address):
        url = "https://ipgeolocation.abstractapi.com/v1/"
        return self._get(
            url=url,
            ip_address=ip_address,
            api_key=self.IP_GEOLOCATION_API_KEY,
        )
