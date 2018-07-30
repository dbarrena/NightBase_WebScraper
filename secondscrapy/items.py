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
    flyer_image = scrapy.Field()
    promoters = scrapy.Field()
    artists_links = scrapy.Field()

    def to_json(self):
        # API expects an array of promoters, if there is only one promoter create an array
        if not isinstance(self['promoters'], list):
            self['promoters'] = [self['promoters']]

        event_dict = dict(name=self['name'], venueTemp=self['venue'], description=self['description'],
                          date=self['date'],
                          price=self['price'], residentAdvisorLink=self['resident_advisor_link'],
                          minimumAge=self['minimum_age'], artistsTemp=self['artists'],
                          residentAdvisorMembers=self['resident_advisor_members'], flyerURL=self['flyer_URL'],
                          promotersTemp=self['promoters'], flyerImage=self['flyer_image'])

        # API cant take null values, if a value is null erase it
        filtered = {k: v for k, v in event_dict.items() if v is not None and v != ""}
        event_dict.clear()
        event_dict.update(filtered)

        return event_dict


class Lineup(scrapy.Item):
    artists = scrapy.Field()


class Artist(scrapy.Item):
    name = scrapy.Field()
    label = scrapy.Field()
    residentadvisor = scrapy.Field()

    def to_json(self):
        return dict(name=self['name'], label=self['label'], residentadvisor=self['residentadvisor'])


class Venue(scrapy.Item):
    name = scrapy.Field()
    residentadvisor = scrapy.Field()
    address = scrapy.Field()

    def to_json(self):
        return dict(name=self['name'], address=self['address'], residentadvisor=self['residentadvisor'])


class Promoter(scrapy.Item):
    name = scrapy.Field()
    residentadvisor = scrapy.Field()

    def to_json(self):
        return dict(name=self['name'], residentadvisor=self['residentadvisor'])


class EventEncoder(json.JSONEncoder):
    def default(self, obj):
        if hasattr(obj, 'to_json'):
            return obj.to_json()
        else:
            return json.JSONEncoder.default(self, obj)


def delete_none(json):
    for key, value in list(json.items()):
        if value is None:
            del json[key]
        elif isinstance(value, dict):
            delete_none(value)
    return json  # For convenience
