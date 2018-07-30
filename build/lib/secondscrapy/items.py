# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html
import json

import scrapy


class Event(scrapy.Item):
    name = scrapy.Field()
    venue = scrapy.Field()
    description = scrapy.Field()
    date = scrapy.Field()
    price = scrapy.Field()
    resident_advisor_link = scrapy.Field()
    minimum_age = scrapy.Field()
    artists = scrapy.Field()
    resident_advisor_members = scrapy.Field()
    flyer_URL = scrapy.Field()
    promoters = scrapy.Field()
    artists_links = scrapy.Field()

    def to_json(self):
        return dict(name=self['name'], venue=self['venue'], description=self['description'], date=self['date'],
                    price=self['price'], resident_advisor_link=self['resident_advisor_link'],
                    minimum_age=self['minimum_age'], artists=self['artists'],
                    resident_advisor_members=self['resident_advisor_members'], flyer_URL=self['flyer_URL'],
                    promoters=self['promoters'])


class Lineup(scrapy.Item):
    artists = scrapy.Field()


class Artist(scrapy.Item):
    name = scrapy.Field()
    label = scrapy.Field()
    link = scrapy.Field()

    def to_json(self):
        return dict(name=self['name'], label=self['label'], link=self['link'])


class Promoter(scrapy.Item):
    name = scrapy.Field()
    link = scrapy.Field()

    def to_json(self):
        return dict(name=self['name'], link=self['link'])


class EventEncoder(json.JSONEncoder):
    def default(self, obj):
        if hasattr(obj, 'to_json'):
            return obj.to_json()
        else:
            return json.JSONEncoder.default(self, obj)

