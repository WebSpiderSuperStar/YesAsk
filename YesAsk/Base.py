# File: Base.py
# User: Payne-Wu
# Date: 2022/6/24 15:01
# Desc:


import json
import time
import random
import requests
from loguru import logger
from fake_headers import Headers
from retrying import retry, RetryError
from YesAsk.configs import GET_TIMEOUT, MinSleepTime, MaxSleepTime

requests.packages.urllib3.disable_warnings()


# from fake_useragent import UserAgent
# for _ in range(1, 2 << 12):
#     print(UserAgent(verify_ssl=False).random)


class BaseCrawler:

    @staticmethod
    @retry(stop_max_attempt_number=3, retry_on_result=lambda x: x is None, wait_fixed=2000)
    def fetch(method, url, **kwargs):
        try:
            logger.info(f"scraping url: {url}")
            if "proxies" in kwargs.keys():
                logger.info(f"Use proxy {kwargs.values()}")
            kwargs.setdefault("timeout", GET_TIMEOUT)
            kwargs.setdefault("verify", False)
            kwargs.setdefault("headers", Headers(headers=True).generate())
            response = requests.request(method, url, **kwargs)
            if response.status_code == 200:
                return response
            logger.error(
                f"Fetch status code is not as expected，status code: {response.status_code}"
            )
        except (requests.ConnectionError, requests.ReadTimeout, RetryError):
            return
        finally:
            time.sleep(random.uniform(MinSleepTime, MaxSleepTime))

    @staticmethod
    def cloud_proxy():
        url = "http://hlfjump.sh.nint.com/api/getproxyyun"
        params = {"user": "test", "proxycount": 1}
        resp_json = BaseCrawler.fetch(method="GET", url=url, params=params).json()
        if resp_json.get('code') == 200:
            proxy = json.loads(resp_json["data"])[0]
            return {
                "http": f"http://liner0123:a123456@{proxy}",
                "https": f"http://liner0123:a123456@{proxy}",
            }

if __name__ == '__main__':
    print(BaseCrawler.cloud_proxy())
