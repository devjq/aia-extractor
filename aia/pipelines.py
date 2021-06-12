# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
import csv

csv_columns = ["Title", "Location", "Email", "Website", "Url"]

class TutorialPipeline(object):
    def process_item(self, item, spider):
        return item

    def close_spider(self, spider):
        md = spider.all_archs
        print(len(md.keys()))
        write_to_csv(md)


def write_to_csv(my_dict):
    try:
        with open("AIA.csv", 'w') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=csv_columns)
            writer.writeheader()
            for key, data in my_dict.items():
                writer.writerow(data)
    except IOError:
        print("I/O ERROR")