# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import json

from pip._vendor import requests

from secondscrapy.items import Event, Artist, EventEncoder

base_url = "www.residentadvisor.net"


class LineupPipeline(object):

    def open_spider(self, spider):
        self.file = open('events.json', 'w')
        self.file.write('{ "events": [')

    def close_spider(self, spider):
        self.file.write("]}")
        self.file.close()

    def process_item(self, item, spider):
        if not isinstance(item, Event):
            return item

        lineup = clean_lineup(item['artists'])

        links = item['artists_links']

        item['artists'] = process_lineup(lineup, links)
        item['artists'] = clean_artists(item['artists'])
        item['promoters'] = clean_promoters(item['promoters'])
        item['date'] = clean_date(item['date'])

        data_json = json.dumps(item.to_json(), cls=EventEncoder)
        # print('JSON', data_json)

        headers = {
            "content-type": "application/json"
        }

        response = requests.post(
            url="http://localhost:8080/event/add",
            headers=headers,
            data=data_json
        )
        print(response)

        return item


def clean_artists(artists):
    clean_artists_list = []
    for artist in artists:
        temp = {k: v for k, v in artist.items() if v != ''}
        clean_artists_list.append(temp)
    return clean_artists_list


def clean_promoters(promoters):
    clean_promoters_list = []
    temp = {k: v for k, v in promoters.items() if v != ''}
    clean_promoters_list.append(temp)

    for promoter in clean_promoters_list:
        if not promoter:
            clean_promoters_list.remove(promoter)

    return clean_promoters_list


def clean_date(date):
    final_date = ""
    for line in date:
        if line == "Date /":
            continue
        else:
            final_date += line + ' '
    return final_date


def clean_lineup(lineup):
    strip_list = ["/", "*", "-", "b2b", "live", "b2b2b", ",", "\n", "LIVE"]

    clean_lineup = []

    # Remove any character that exists in strip_list from each line
    for line in lineup:
        for strip_item in strip_list:
            line = line.replace(strip_item, "")
            line = line.strip()
        clean_lineup.append(line)
    return clean_lineup


def process_lineup(lineup, links):
    artists = []

    avoid_list = ["upstairs", "downstairs", "garden", "r1", "r2",
                  "afterhour", "line up", "lineup", "artwork",
                  "flyer", "mainfloor", "mainroom", "main floor",
                  "hip hop", "hip-hop", "reggae", "livingroom", "rummel",
                  "bunker floor", "house floor", "r_1", "r_2", "artists",
                  "all night", "more tba", "more t.b.a", "and more", ":",
                  "AND MORE", "ALL NIGHT"]

    # Sometimes the artists has the label inside parenthesis after the name,
    # if the label contains any link then it is divided in more than one line
    # if there is no link in the label then its one single line, so here it detects
    # a label and assign it to the last artists in the array

    temp_label = None
    for artist in lineup:

        artist_item = Artist()
        artist_item['label'] = ''

        if any(avoid in artist for avoid in avoid_list):
            continue

        if not artist or artist.isspace():
            continue

        # Label without a link
        if "(" in artist and ")" in artist:
            if artist.startswith('('):
                last_key = artists[-1]
                last_key['label'] = artist
                continue
            else:
                artist_with_link = artist.split('(')
                artist_item['name'] = artist_with_link[0]
                artist_item['label'] = artist_with_link[1].replace(')', '')
                artists.append(artist_item)
                continue

        # Label is being processed
        if temp_label:
            if ")" in artist:
                temp_label += artist
                last_key = artists[-1]
                last_key['label'] = temp_label
                temp_label = None
                continue
            else:
                temp_label += artist
                continue
        else:
            if "(" in artist:
                temp_label = artist
                continue

        artist_item['name'] = artist
        artists.append(artist_item)

    # If the artist contains a link assign it to artist item
    for artist in artists:
        artist['residentadvisor'] = ''
        name = artist['name'].replace(" ", "").lower()
        for link in links:
            if name in link:
                artist['residentadvisor'] = base_url + link

    return artists
