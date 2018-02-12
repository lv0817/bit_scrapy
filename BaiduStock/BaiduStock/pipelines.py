# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

'''
这里面每一个类都是对item处理的一个过程

'''
class BaidustockPipeline(object):
    def process_item(self, item, spider):
        return item
class BaidustockInfoPipeline(object):
    def open_spider(self,spider):
        #当一个爬虫被调用时，使用的pipeline
        self.f = open('BaiduStockInfo.txt','w')
        # 打开爬虫时，我们希望建立一个文件
    def close_spider(self,spider):
        self.f.close()

    def process_item(self,item,spider):
        #处理item时，要把信息写入到item中
        #这里将获得的股票信息的字典写入一个文件
        try:
            line = str(dict(item))+'\n'
            self.f.write(line)
        except:
            pass
        return item