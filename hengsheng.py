# import scrapy
# #
# # class HsiSpider(scrapy.Spider):
# #     name = 'hsi'
# #     start_urls = ['https://www.hsi.com.hk/eng/indexes/all-indexes']
# #
# #     def parse(self, response):
# #         for tr in response.css('table#indexTable tr'):
# #             yield {
# #                 'date': tr.css('td:nth-child(1)::text').extract_first(),
# #                 'hsi': tr.css('td:nth-child(2)::text').extract_first(),
# #             }
import yfinance
hsi=yfinance.Ticker("IXIC")
# 获取恒生指数的历史数据
# hsi_history = hsi.get_historical_data(start="2022-01-01", end="2022-12-31")
hsi_history=hsi.history(period='max')
hsi_history.to_csv('纳斯达克指数.csv')
# 打印恒生指数的历史数据
print(hsi_history)