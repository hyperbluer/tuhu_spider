本爬虫基于Scrapy框架完成对途虎网的车型库及车款保养周期表爬取，数据存储在mysql。

使用前请确认安装python2.7以及Scrapy模块
安装命令：`pip install scrapy`

使用步骤：
1. 建立mysql数据库，将根目录的sql文件导入
2. 修改**/tuhu_spider/settings.py**文件，配置mysql信息以及图片存储位置（IMAGES_STORE）
3. 根目录执行`scrapy crawl car`完成数据自动采集

友情提示：此爬虫涉及对第三方（途虎网）的数据采集，请勿作为商业使用！


