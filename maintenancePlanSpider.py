# -*- coding:utf-8 -*-
from __future__ import division
import sys
import MySQLdb
import urllib2
import time
import json

reload(sys)
sys.setdefaultencoding('utf-8')

# 本地
MYSQL_CONFIG = {
    'host': 'localhost',
    'dbname': 'car',
    'user': 'root',
    'passwd': '123456',
    'port': 3306,
    'charset': 'utf8',
}


class CarLevelSpider(object):
    custom_settings = {
        "DEFAULT_REQUEST_HEADERS": {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'accept-language': 'zh-CN,zh;q=0.8',
            'referer': 'https://www.baidu.com/',
            'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3251.0 Safari/537.36',
        }
    }
    parse_start_url = 'https://by.tuhu.cn/apinew/GetBaoYangManualTable.html?Vehicle={"Distance":"","OnRoadTime":"","Nian":"%s","PaiLiang":"%s","VehicleId":"%s"}'
    page_size = 1000
    time_sleep = 0.1

    def __init__(self):
        self.conn = MySQLdb.connect(
            host=MYSQL_CONFIG['host'],
            db=MYSQL_CONFIG['dbname'],
            user=MYSQL_CONFIG['user'],
            passwd=MYSQL_CONFIG['passwd'],
            port=MYSQL_CONFIG['port'],
            charset=MYSQL_CONFIG['charset'])
        self.cursor = self.conn.cursor()

    def parse(self):
        i = 0
        current_page = 1
        while True:
            car_version_list = self.get_car_version_list(current_page)
            if isinstance(car_version_list, tuple) and len(car_version_list) > 0:
                current_page += 1
                for version in car_version_list:
                    self.parse_car_version(version)
                    i += 1
                    if self.time_sleep:
                        time.sleep(self.time_sleep)
            else:
                break

        print '总记录数：' + str(i)

    def parse_car_version(self, version):
        start_url = self.parse_start_url % (version[3], (version[2]).strip(), version[1])
        print start_url

        try:
            request = urllib2.Request(start_url)
            request.add_header('user-agent', self.custom_settings['DEFAULT_REQUEST_HEADERS']['user-agent'])
            response = urllib2.urlopen(request)
            html = response.read()

            if not html:
                return None

            result = json.loads(html)
            if not result['Code']:
                return None

            accessory_data = MySQLdb.escape_string(json.dumps(result['Data']['AccessoryData']))
            maintenance_plan_data = MySQLdb.escape_string(json.dumps(result['Data']['SuggestData']))

            try:
                sql = "UPDATE base_tuhu_car_version SET accessory_data = '%s', maintenance_plan_data = '%s' WHERE id = %d" % (
                accessory_data, maintenance_plan_data, version[0])
                self.cursor.execute(sql)
                self.conn.commit()
            except MySQLdb.Error, e:
                if e.args[0] == 1062:
                    print 'PASS'
                else:
                    print "Error %d: %s" % (e.args[0], e.args[1])
        except urllib2.HTTPError:
            print '异常'
            pass

    def get_car_version_list(self, current_page):
        sql = 'SELECT id, product_id, displacement, `year` FROM base_tuhu_car_version WHERE accessory_data IS NULL ORDER BY id ASC LIMIT %s, %s'
        # offset = (current_page-1)*self.page_size
        #params = (offset, self.page_size)
        params = (0, self.page_size)
        self.cursor.execute(sql, params)
        result = self.cursor.fetchall()
        return result


if __name__ == '__main__':
    spider = CarLevelSpider()
    spider.parse()
