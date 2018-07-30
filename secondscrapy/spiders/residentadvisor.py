# -*- coding: utf-8 -*-
import scrapy
import requests
import base64

from secondscrapy.items import Event, Promoter, Venue

# Main list of events

events_list_selector = "#items > li"
event_selector = "article > div > h1 > a ::text"
venue_selector = "article > div > h1 > span > a ::text"
venue_link_selector = "article > div > h1 > span > a ::attr(href)"
link_selector = "article > div > h1 > a ::attr(href)"

# Individual event

description_selector = "#event-item > div.left > p:nth-child(3) ::text"
members_selector = "#MembersFavouriteCount ::text"
flyer_selector = "#event-item > div.flyer > a > img ::attr(src)"
date_selector = "#detail > ul > li:nth-child(1) ::text"
artists_selector = "//*[@id='event-item']/div[3]/p[1]//text()"
artists_links_selector = "//*[@id='event-item']/div[3]/p[1]//a/@href"
price_selector = "//div[text()='Cost /']/parent::li[1]/text()"
promoters_selector = "//div[text()='Promoters /']/parent::li[1]/text()"
age_selector = "//div[text()='Minimum age /']/parent::li[1]/text()"
venue_address_selector = "//*[@id='detail']/ul/li[2]/text()"


class ResidentadvisorSpider(scrapy.Spider):

    base_url = "www.residentadvisor.net"
    name = "residentadvisor"
    allowed_domains = ["www.residentadvisor.net"]
    start_urls = ["https://www.residentadvisor.net/events/de/berlin"]

    def parse(self, response):

        events_list = response.css(events_list_selector)

        for eventItem in events_list:
            event = Event()
            event["name"] = eventItem.css(event_selector).extract_first()

            venue = Venue()
            venue["name"] = eventItem.css(venue_selector).extract_first()
            venue["residentadvisor"] = eventItem.css(venue_link_selector).extract_first()
            venue["address"] = eventItem.xpath(venue_address_selector).extract_first()

            event["venue"] = venue
            event["resident_advisor_link"] = response.urljoin(eventItem.css(link_selector).extract_first())

            # It"s a date header instead of event item so exit loop iteration
            if not event["name"]:
                continue

            request = scrapy.Request(event["resident_advisor_link"], callback=self.parse_event)
            request.meta["event"] = event

            yield request

    def parse_event(self, response):

        event = response.meta["event"]
        event["description"] = u"".join(response.css(description_selector).extract())
        event["resident_advisor_members"] = response.css(members_selector).extract_first().strip()
        event["flyer_URL"] = response.urljoin(response.css(flyer_selector).extract_first())
        event["date"] = response.css(date_selector).extract()
        event["price"] = response.xpath(price_selector).extract_first()
        event["minimum_age"] = response.xpath(age_selector).extract_first()
        event["artists"] = response.xpath(artists_selector).extract()
        event["artists_links"] = response.xpath(artists_links_selector).extract()
        event['promoters'] = process_promoter(response)
        event["flyer_image"] = base64.b64encode(requests.get(event["flyer_URL"]).content)

        venue = event["venue"]
        venue["address"] = response.xpath(venue_address_selector).extract_first()

        yield event


def process_promoter(response):
    promoter_item = Promoter()
    promoter = response.xpath(promoters_selector).extract_first()
    if promoter:
        promoter_item['name'] = promoter
        promoter_item['residentadvisor'] = ''

    if not promoter:
        promoter_with_link = response.xpath("//div[text()='Promoters /']/parent::li/a/text()").extract_first()

        if promoter_with_link:
            promoter_item['name'] = promoter_with_link
            promoter_item['residentadvisor'] = response.urljoin(
                response.xpath("//div[text()='Promoters /']/parent::li/a/@href").extract_first())
        else:
            promoter_item['name'] = ''
            promoter_item['residentadvisor'] = ''

    return promoter_item
