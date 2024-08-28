from typing import Any
import re
import time
import os

import scrapy
from scrapy.http import Response
from scrapy.utils.response import open_in_browser

from ..items import AidserverItem
from utils.config import load_config
from utils.db_utils import get_apt_urls, remove_apt_by_url


class DescriptionsSpider(scrapy.Spider):
    name = 'descriptions'
    apt_urls = get_apt_urls()
    if apt_urls:
        start_urls = {
            apt_urls[0]
        }

    # get root project path
    project_root_path = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    scraping_cfg = load_config(fr"{project_root_path}/scraping_cfg.json")

    custom_settings = {
        'HTTPERROR_ALLOWED_CODES': [404, 500, 302],
    }
    items = None

    def parse(self, response: Response, **kwargs: Any) -> Any:
        """
        parsing the response from the website
        :param response: the response from the website
        :param kwargs: additional arguments
        :return:
        """
        if response.status in [404, 500]:  # page not found, internal server error
            self.logger.error(f'Received 404 or 500 at {response.url}')
            remove_apt_by_url(DescriptionsSpider.apt_urls.pop(0))
            yield response.follow(DescriptionsSpider.apt_urls[0], callback=self.parse)
        elif response.status == 302:  # redirect
            self.logger.error(f'Received 302 at {response.url}')
            yield response.follow(DescriptionsSpider.apt_urls[0], callback=self.parse)
        else:
            # open_in_browser(response)  # for debugging purposes

            if 'Shield' in str(response.body):
                # raise Exception("Shield detected, exiting...")
                time.sleep(2)

            self.items = AidserverItem()
            if not DescriptionsSpider.apt_urls:
                return
            apt_url = DescriptionsSpider.apt_urls.pop(0)

            # scraping the description
            self.items['url'] = apt_url

            description = response.xpath(DescriptionsSpider.scraping_cfg['xPaths']['description']).extract()
            if description:
                description = re.search(r'<p class="description_description__l3oun">(.*?)</p>', description[0], re.DOTALL)
                description = description.group(1).replace("\n", '') if description else 'empty'
            else:
                description = 'empty'
            if description == '':
                description = 'empty'
            self.items['description'] = description

            yield self.items  # yield the items to the pipeline

            yield response.follow(DescriptionsSpider.apt_urls[0], callback=self.parse)  # follow the next url
