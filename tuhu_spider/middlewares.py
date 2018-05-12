# -*- coding: utf-8 -*-

# Define here the models for your spider middleware
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/spider-middleware.html

from scrapy import signals
from scrapy.exceptions import IgnoreRequest
import MySQLdb
import hashlib


class TuhuSpiderSpiderMiddleware(object):
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the spider middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_spider_input(self, response, spider):
        # Called for each response that goes through the spider
        # middleware and into the spider.

        # Should return None or raise an exception.
        return None

    def process_spider_output(self, response, result, spider):
        # Called with the results returned from the Spider, after
        # it has processed the response.

        # Must return an iterable of Request, dict or Item objects.
        for i in result:
            yield i

    def process_spider_exception(self, response, exception, spider):
        # Called when a spider or process_spider_input() method
        # (from other spider middleware) raises an exception.

        # Should return either None or an iterable of Response, dict
        # or Item objects.
        pass

    def process_start_requests(self, start_requests, spider):
        # Called with the start requests of the spider, and works
        # similarly to the process_spider_output() method, except
        # that it doesn’t have a response associated.

        # Must return only requests (not items).
        for r in start_requests:
            yield r

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)


class IgnoreDuplicatesDownloaderMiddleware(object):
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
            charset=settings['MYSQL_CHARSET'])
        cursor = conn.cursor()
        return cls(conn, cursor)

    def process_request(self, request, spider):
        return None

    def process_response(self, request, response, spider):
        page_uid = hashlib.sha1(request.url).hexdigest()
        data_uid = hashlib.sha1(response.body).hexdigest()
        start_url_uid = hashlib.sha1(spider.start_urls[0]).hexdigest()

        sql = "SELECT data_uid FROM base_tuhu_spider_logs WHERE page_uid = '%s' ORDER BY id DESC LIMIT 1 " % page_uid
        self.cursor.execute(sql)
        result = self.cursor.fetchone()
        if result and (str(data_uid) == str(result[0])):
            if page_uid == start_url_uid or ('check_data' in request.meta and request.meta['check_data']):
                response.headers['IGNORE-DATA'] = 1
                return response
            else:
                raise IgnoreRequest()

        sql = 'INSERT INTO base_tuhu_spider_logs (page_url, page_uid, data_uid) VALUES (%s, %s, %s)'
        params = (request.url, page_uid, data_uid)
        self.cursor.execute(sql, params)
        self.conn.commit()

        return response