# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import openpyxl
import pymysql

class DbPipeline:
    def __init__(self):
        self.conn = pymysql.connect(host='xx', port='xx',
                                    user='xx', password='xx',
                                    database='xx', charset='xx')
        self.cursor = self.conn.cursor()
        self.data = []

    def close_spider(self, spider):
        if len(self.data) > 0:
            self._write_to_db()
        # self.conn.commit()
        self.conn.close()



    def process_item(self, item, spider):
        title = item.get('title', '')
        category = item.get('category', '')
        date = item.get('date', '')
        intro = item.get('intro', '')
        # self.cursor.execute('insert into top4399 (title, category, date, intro) values (%s, %s, %s, %s)',
        #                     (title, category, date, intro))

        self.data.append((title, category, date, intro))
        if len(self.data) == 100:
            self._write_to_db()
            self.data.clear()
        return item

    def _write_to_db(self):
        self.cursor.executemany(
            'insert into top4399 (title, category, date, intro) values (%s, %s, %s, %s)', self.data)
        self.conn.commit()


class ExcelPipeline:
    def __init__(self):
        self.wb = openpyxl.Workbook()
        self.ws = self.wb.active
        self.ws.title = '4399'
        self.ws.append(('标题', '类别', '日期', '简介'))

    def close_spider(self,spider):
        self.wb.save('4399小游戏.xlsx')


    def process_item(self, item, spider):
        title = item.get('title', '')
        category = item.get('category', '')
        date = item.get('date', '')
        intro = item.get('intro', '')
        self.ws.append((title, category, date, intro))
        return item
