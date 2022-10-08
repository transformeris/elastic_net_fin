#!/usr/bin/env python
# -*- encoding=utf8 -*-

import time
import requests
import json

from datetime import datetime

from .jd_logger import logger
from .config import global_config


class Timer(object):
    def __init__(self, sleep_interval=0.5):
        # '2018-09-28 22:45:50.000'
        self.buy_time = None
        try:
            self.buy_time = datetime.strptime(global_config.getRaw('config', 'buy_time'), "%Y-%m-%d %H:%M:%S.%f")
        except Exception as e:
            # 如果没有配置购买时间，就使用当天的时间，2021-01-13 09:59:59.800
            self.buy_time = datetime.strptime((time.strftime("%Y-%m-%d", time.localtime()) + " 09:59:59.800")
                                              , "%Y-%m-%d %H:%M:%S.%f")
        logger.info('配置的抢购时间为: %s', self.buy_time)
        self.buy_time_ms = int(time.mktime(self.buy_time.timetuple()) * 1000.0 + self.buy_time.microsecond / 1000)
        self.sleep_interval = sleep_interval

        self.diff_time = self.local_jd_time_diff()

    def jd_time(self):
        """
        从京东服务器获取时间毫秒
        :return:
        """
        # url = 'https://a.jd.com//ajax/queryServerData.html'
        # ret = requests.get(url).text
        # js = json.loads(ret)
        url = 'https://api.m.jd.com/client.action?functionId=queryMaterialProducts&client=wh5'
        header = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"}

        ret = requests.get(url,headers=header).text
        js = json.loads(ret)
        return int(js["currentTime2"])

    def local_time(self):
        """
        获取本地毫秒时间
        :return:
        """
        return int(round(time.time() * 1000))

    def local_jd_time_diff(self):
        """
        计算本地与京东服务器时间差
        :return:
        """
        return self.local_time() - self.jd_time()

    def start(self):
        logger.info('正在等待到达设定时间:{}，检测本地时间与京东服务器时间误差为【{}】毫秒'.format(self.buy_time, self.diff_time))
        while True:
            # 本地时间减去与京东的时间差，能够将时间误差提升到0.1秒附近
            # 具体精度依赖获取京东服务器时间的网络时间损耗
            if self.local_time() - self.diff_time >= self.buy_time_ms:
                logger.info('时间到达，开始执行……')
                break
            else:
                time.sleep(self.sleep_interval)

    def buytime_get(self):
        """获取开始抢购的时间"""
        return self.buy_time