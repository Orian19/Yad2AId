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
        # open_in_browser(response)  # for debugging purposes

        scraping_cfg = self.load_config()
        items = AidserverItem()

        # scraping all the relevant items
        price = response.xpath(scraping_cfg['xPaths']['price']).extract()
        # -1 if "לא צוין מחיר"
        price = [int(re.search(r'\d+,\d+', html).group().replace(',', '')) if re.search(r'\d+,\d+', html) else -1 for html in price]
        city = response.xpath(scraping_cfg['xPaths']['city']).extract()
        city = [re.search(r'>([^<]+)<', html).group(1).split(',')[-1] if re.search(r'>([^<]+)<', html) else '' for html in city]
        address = response.xpath(scraping_cfg['xPaths']['address']).extract()
        address = [re.search(r'>([^<]+)<', html).group(1) if re.search(r'>([^<]+)<', html) else '' for html in address]
        rooms_floor_sqm = response.xpath(scraping_cfg['xPaths']['rooms_floor_sqm']).extract()
        rooms, floor, sqm = self.parse_rooms_floor_sqm(rooms_floor_sqm)
        image = response.xpath(scraping_cfg['xPaths']['image']).extract()
        image = [re.search(r'src="([^"]+)"', html).group(1) if re.search(r'src="([^"]+)"', html) else '' for html in image]
        items['price'] = price
        items['city'] = city
        items['address'] = address
        items['rooms'] = rooms
        items['floor'] = floor
        items['sqm'] = sqm
        items['image'] = image

        # user = class ="user-drop-container_profileBoxText__deZ0a user-drop-container_wideDesktop__wuusc" > Orian < /span >

        # sends item to pipline
        yield items

        # next_page = response.css('<a data-testid="nextButton" class="link_link__vOomn" aria-label="עמוד הבא" aria-disabled="false" data-nagish="pagination-item-link" href="/realestate/rent?page=2"><svg width="1em" height="1em" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg" class="link_icon__qM0QO"><path d="M15.014 17.884a.75.75 0 01-.98 1.13l-.084-.073-6.137-6.18a.75.75 0 01-.069-.977l.073-.083 6.145-6.103a.75.75 0 011.13.98l-.073.085-5.613 5.573 5.608 5.648z" fill="currentColor"></path></svg></a>')
        next_page = f'https://www.yad2.co.il/realestate/rent?page={str(ApartmentsSpider.page_number)}'

        # # todo: decide if to scrape all 1000+ pages or limit
        if ApartmentsSpider.page_number <= 3:
            ApartmentsSpider.page_number += 1
            yield response.follow(next_page, callback=self.parse)
