# -*- coding: utf-8 -*-
import scrapy
import json
from tuhu_spider import items


class CarSpider(scrapy.Spider):
    name = 'car'
    allowed_domains = ['tuhu.cn']
    start_urls = ['https://item.tuhu.cn/Car/GetCarBrands']
    external_urls = {
        'car_list': 'https://item.tuhu.cn/Car/SelOneBrand?Brand=%s',
        'car_displacement_list': 'https://item.tuhu.cn/Car/SelectVehicle?VehicleID=%s&PaiLiang=%s',
        'car_version_list': 'https://item.tuhu.cn/Car/SelectVehicleSalesName?VehicleID=%s&PaiLiang=%s&Nian=%s',
    }

    def parse(self, response):
        priority = 10000
        ignore_data = int(response.headers['IGNORE-DATA']) if 'IGNORE-DATA' in response.headers else 0
        dict_data = json.loads(response.body, strict=False)['Brand']

        for data in dict_data:
            name = data['Brand']

            if not ignore_data:
                item = items.BrandItem()
                item['name'] = name
                item['remote_logo'] = data['ImageUrl']
                yield item

            print u'[品牌] ' + ('' if ignore_data else '+ ') + name

            priority -= 1
            url = self.external_urls['car_list'] % name
            yield scrapy.Request(url, callback=self.parse_car_data, meta={'brand_name': name, 'check_data': 1}, priority=priority)

    def parse_car_data(self, response):
        priority = 10000
        ignore_data = int(response.headers['IGNORE-DATA']) if 'IGNORE-DATA' in response.headers else 0
        dict_data = json.loads(response.body, strict=False)['OneBrand']

        for data in dict_data:
            name = data['CarName']
            if not ignore_data:
                item = items.CarItem()
                item['name'] = data['CarName']
                item['product_id'] = data['ProductID']
                item['remote_logo'] = data['Image']
                item['brand_name'] = data['Brand']
                item['factory_name'] = data['BrandType']
                item['is_baoyang'] = 1 if data['IsBaoYang'] == 'True' else 0
                #print item
                yield item

            print u'[车型] ' + ('' if ignore_data else '+ ') + response.meta['brand_name'] + ' ' + name

            priority -= 1
            url = self.external_urls['car_displacement_list'] % (data['ProductID'], '')
            yield scrapy.Request(url, callback=self.parse_car_displacement_data, meta={'brand_name': data['Brand'], 'car_name': name, 'check_data': 1}, priority=priority)

    def parse_car_displacement_data(self, response):
        priority = 10000
        ignore_data = int(response.headers['IGNORE-DATA']) if 'IGNORE-DATA' in response.headers else 0
        dict_data = json.loads(response.body, strict=False)['PaiLiang']

        for data in dict_data:
            if not ignore_data:
                item = items.CarDisplacementItem()
                item['product_id'] = data['Key']
                item['displacement'] = data['Value']
                # print item
                yield item

            car_full_name = response.meta['brand_name'] + ' ' + response.meta['car_name'] + ' '
            print u'[排量] ' + ('' if ignore_data else '+ ') + car_full_name + ' ' + data['Value']

            priority -= 1
            url = self.external_urls['car_displacement_list'] % (data['Key'], data['Value'])
            yield scrapy.Request(url, callback=self.parse_car_displacement2year_data, meta={'car_full_name': car_full_name, 'displacement': data['Value'], 'check_data': 1}, priority=priority)

    def parse_car_displacement2year_data(self, response):
        priority = 10000
        ignore_data = int(response.headers['IGNORE-DATA']) if 'IGNORE-DATA' in response.headers else 0
        dict_data = json.loads(response.body, strict=False)['Nian']

        for data in dict_data:
            if not ignore_data:
                item = items.CarDisplacement2YearItem()
                item['product_id'] = data['Key']
                item['displacement'] = response.meta['displacement']
                item['year'] = data['Value']
                # print item
                yield item

            print u'[排量+年份] ' + ('' if ignore_data else '+ ') + response.meta['car_full_name'] + ' ' + response.meta['displacement'] + ' ' + data['Value']

            priority -= 1
            url = self.external_urls['car_version_list'] % (data['Key'], response.meta['displacement'], data['Value'])
            yield scrapy.Request(url, callback=self.parse_car_version_data, meta={'car_full_name': response.meta['car_full_name'], 'product_id': data['Key'], 'displacement': response.meta['displacement'], 'year': data['Value'], 'check_data': 1}, priority=priority)

    def parse_car_version_data(self, response):
        ignore_data = int(response.headers['IGNORE-DATA']) if 'IGNORE-DATA' in response.headers else 0
        dict_data = json.loads(response.body, strict=False)['SalesName']

        for data in dict_data:
            if not ignore_data:
                item = items.CarVersionItem()
                item['name'] = data['Name']
                item['t_id'] = data['TID']
                item['product_id'] = response.meta['product_id']
                item['displacement'] = response.meta['displacement']
                item['year'] = response.meta['year']
                # print item
                yield item

            print u'[车款] ' + ('' if ignore_data else '+ ') + response.meta['car_full_name'] + ' ' + data['Name']
