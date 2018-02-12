# -*- coding: utf-8 -*-
import scrapy
import re
'''
从东方财富爬取相关股票链接，并要产生对应百度的链接
'''


class StocksSpider(scrapy.Spider):
    name = 'stocks'
    #allowed_domains = ['baidu.com']
    start_urls = ['http://quote.eastmoney.com/stocklist.html']

    def parse(self, response):
        for href in response.css('a::attr(href)').extract():
            try:
                stock = re.findall(r'[s][hz]\d{6}',href)[0]
                url = 'https://gupiao.baidu.com/stock/'+stock+'.html'#百度股票对应的链接信息
                #这样的链接就可以重新作为一个request请求提交给scrapy框架
                yield scrapy.Request(url,callback=self.parse_stock)
                #这个callback给出了处理对应url的相应函数 
                #为了和已有的响应函数有所区分，我们为其更名为parse_stock
                #那么，需要在parse_stock函数中实现，单个股票的百度页面的爬取
            except:
                continue
        
        '''反馈信息最终提交给pipeline，所以生成一个字典'''
        def parse_stock(self,response):
            infoDict = {}
            #stockInfo = response.css('.stock-bets')
            stockInfo = response.css('div::attr(stock-bets)')
            name = stockInfo.css('.bets-name').extract()[0]
            keyList = stockInfo.css('dt').extract()
            valueList = stockInfo.css('dd').extract()
            #将提取的信息保存在字典中
            for i in range(len(keyList)):
                key = re.findall(r'>.*</dt>',keyList[i])[0][1:-5]#找到所有的，提取第0个，
                #上面可以试试用find
                try :
                    val = re.findall(r'\d+\.?*</dd>',valueList[i])[0][0:-5]
                except :
                    val = '找不到参数'
                infoDict[key] = val

            infoDict.update(
                {'股票名称':re.findall('\s.*\(',name)[0].split()[0] +\
                 re.findall(r'>.*<',name)[0][1:-1]})
            '''
            然后将得到的信息交给pipeline
            '''
            yield infoDict#生成器

