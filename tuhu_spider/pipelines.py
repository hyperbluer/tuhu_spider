# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import MySQLdb
from tuhu_spider import items


class TuhuSpiderPipeline(object):
    def __init__(self, conn, cursor):
        self.conn = conn
        self.cursor = cursor

    @classmethod
    def from_settings(cls, settings):
        conn = MySQLdb.connect(
            host=settings['MYSQL_HOST'],
            db=settings['MYSQL_DBNAME'],
            user=settings['MYSQL_USER'],
            passwd=settings['MYSQL_PASSWD'],
            port=settings['MYSQL_PORT'],
            charset=settings['MYSQL_CHARSET']
        )
        cursor = conn.cursor()
        return cls(conn, cursor)

    def process_item(self, item, spider):
        try:
            if isinstance(item, items.BrandItem):
                sql = 'INSERT INTO base_tuhu_car_brand(`name`, remote_logo) VALUES (%s, %s)'
                params = (item['name'], item['remote_logo'])
                self.cursor.execute(sql, params)
                self.conn.commit()
            elif isinstance(item, items.CarItem):
                sql = 'INSERT INTO base_tuhu_car(`name`, product_id, remote_logo, brand_name, factory_name, is_baoyang) VALUES (%s, %s, %s, %s, %s, %s)'
                params = (item['name'], item['product_id'], item['remote_logo'], item['brand_name'], item['factory_name'], item['is_baoyang'])
                self.cursor.execute(sql, params)
                self.conn.commit()
            elif isinstance(item, items.CarVersionItem):
                sql = 'INSERT INTO base_tuhu_car_version(`name`, t_id, product_id, displacement, `year`) VALUES (%s, %s, %s, %s, %s)'
                params = (item['name'], item['t_id'], item['product_id'], item['displacement'], item['year'])
                self.cursor.execute(sql, params)
                self.conn.commit()
            elif isinstance(item, items.CarDisplacementItem):
                sql = 'INSERT INTO base_tuhu_car_displacement(product_id, displacement) VALUES (%s, %s)'
                params = (item['product_id'], item['displacement'])
                self.cursor.execute(sql, params)
                self.conn.commit()
            elif isinstance(item, items.CarDisplacement2YearItem):
                sql = 'INSERT INTO base_tuhu_car_displacement2year(product_id, displacement, `year`) VALUES (%s, %s, %s)'
                params = (item['product_id'], item['displacement'], item['year'])
                self.cursor.execute(sql, params)
                self.conn.commit()
            else:
                pass
        except MySQLdb.Error, e:
            if e.args[0] == 1062:
                print 'PASS'
            else:
                print "Error %d: %s" % (e.args[0], e.args[1])

        return item
