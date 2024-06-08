import random
import time
from typing import Any
import json
import re

import scrapy
from scrapy.http import Response
from scrapy.utils.response import open_in_browser

from ..items import AidserverItem


class ApartmentsSpider(scrapy.Spider):
    name = 'apartments'
    start_urls = {
        r'https://www.yad2.co.il/realestate/rent'
    }
    page_number = 2  # pagination
    descriptions = []
    pending_requests = 0
    items = None

    @staticmethod
    def load_config(cfg_file=r'scraping_cfg.json'):
        """
        loading the json config
        :param cfg_file:
        :return:
        """
        with open(cfg_file) as config_file:
            return json.load(config_file)

    @staticmethod
    def parse_rooms_floor_sqm(values):
        """
        parsing the rooms, floor and sqm from the html values
        :param values: list of html values
        :return: rooms, floor, sqm
        """
        rooms = []
        floor = []
        sqm = []
        for html in values:
            match = re.search(r'>([^<]+)<', html)
            if match:
                # Reverse the entire matched string and split by the dot symbol '•'
                parts = match.group(1)[::-1].split(' • ')

                # Reverse each word in the split parts
                reversed_parts = [' '.join(word[::-1] for word in part.split()) for part in parts]

                # Append the reversed parts to the respective lists
                if len(reversed_parts) == 3:
                    rooms.append(reversed_parts[2].strip().split(' ')[-1])
                    fl = reversed_parts[1].strip().split(' ')[0].strip('\u200e\u200f')
                    if fl == 'קרקע':
                        fl = 0
                    floor.append(int(fl))
                    sqm.append(reversed_parts[0].strip().split(' ')[-1])
                else:
                    rooms.append('-1')
                    floor.append('-1')
                    sqm.append('-1')
            else:
                rooms.append('-1')
                floor.append('-1')
                sqm.append('-1')

        return rooms, floor, sqm

    def parse(self, response: Response, **kwargs: Any) -> Any:
        """
        parsing the response from the website
        :param response: the response from the website
        :param kwargs: additional arguments
        :return:
        """
        open_in_browser(response)  # for debugging purposes

        if 'Shield' in str(response.body):  # or 'Secure' in str(response.certificate):
            raise Exception("Shield detected, exiting...")

        scraping_cfg = self.load_config()
        self.items = AidserverItem()

        # scraping all the relevant items
        price = response.xpath(scraping_cfg['xPaths']['price']).extract()
        price = [int(re.search(r'\d+,\d+', html).group().replace(',', '')) if re.search(r'\d+,\d+', html) else -1 for html in price]
        city = response.xpath(scraping_cfg['xPaths']['city']).extract()
        city = [re.search(r'>([^<]+)<', html).group(1).split(',')[-1] if re.search(r'>([^<]+)<', html) else '' for html in city]
        address = response.xpath(scraping_cfg['xPaths']['address']).extract()
        address = [re.search(r'>([^<]+)<', html).group(1) if re.search(r'>([^<]+)<', html) else '' for html in address]
        rooms_floor_sqm = response.xpath(scraping_cfg['xPaths']['rooms_floor_sqm']).extract()
        rooms, floor, sqm = self.parse_rooms_floor_sqm(rooms_floor_sqm)
        image = response.xpath(scraping_cfg['xPaths']['image']).extract()
        image = [re.search(r'src="([^"]+)"', html).group(1) if re.search(r'src="([^"]+)"', html) else '' for html in image]
        # paid_ad = response.xpath(scraping_cfg['xPaths']['paid_ad']).extract()
        # paid_ad = [True if re.search(r'>([^<]+)<', html).group(1) else False for html in paid_ad]
        apt_urls = response.xpath(scraping_cfg['xPaths']['apt_href']).extract()
        apt_urls = [re.search(r'href="([^"]+)"', html).group(1) if re.search(r'href="([^"]+)"', html) else '' for html in apt_urls]

        self.items['price'] = price
        self.items['city'] = city
        self.items['address'] = address
        self.items['rooms'] = rooms
        self.items['floor'] = floor
        self.items['sqm'] = sqm
        self.items['image'] = image
        # self.items['paid_ad'] = paid_ad
        self.items['url'] = [scraping_cfg['urls']['apt_start_url'] + apt for apt in apt_urls]
        self.descriptions = [''] * len(apt_urls)

        self.pending_requests = len(apt_urls)

        # following the specific apartments links to get the description + yielding items to the pipeline
        for i, apt_url in enumerate(apt_urls):
            time.sleep(random.uniform(1, 2))
            yield response.follow(apt_url, callback=self.parse_description, meta={'scraping_cfg': scraping_cfg, 'index': i})

    def parse_description(self, response: Response):
        """
        parsing the description of the apartment + yielding the items to the pipeline
        :param response: the response from the website
        :return:
        """
        cfg = response.meta['scraping_cfg']
        index = response.meta['index']
        description = response.xpath(cfg['xPaths']['description']).extract()
        if description:
            description = re.search(r'<p class="description_description__l3oun">(.*?)</p>', description[0], re.DOTALL)
            description = description.group(1).replace("\n", '') if description else ''
        else:
            description = ''
        self.descriptions[index] = description
        self.pending_requests -= 1

        if self.pending_requests == 0:
            self.items['description'] = self.descriptions
            yield self.items  # yield the items to the pipeline

            # pagination
            next_page = f'https://www.yad2.co.il/realestate/rent?page={str(ApartmentsSpider.page_number)}'
            # todo: change pages num
            if ApartmentsSpider.page_number <= 50:
                ApartmentsSpider.page_number += 1
                time.sleep(random.uniform(2, 6))
                yield response.follow(next_page, callback=self.parse)  # follow the next page

