from typing import Any

import scrapy
from scrapy.http import Response
from scrapy.utils.response import open_in_browser

from ..items import AidserverItem


class ApartmentsSpider(scrapy.Spider):
    name = 'apartments'
    start_urls = {
        r'https://www.yad2.co.il/realestate/rent'
    }

    def parse(self, response: Response, **kwargs: Any) -> Any:
        # open_in_browser(response)  # for debugging purposes

        items = AidserverItem()

        title = response.css("title::text").extract()
        items['title'] = title

        # sends item to pipline
        yield items

        # next_page = response.css('<a data-testid="nextButton" class="link_link__vOomn" aria-label="עמוד הבא" aria-disabled="false" data-nagish="pagination-item-link" href="/realestate/rent?page=2"><svg width="1em" height="1em" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg" class="link_icon__qM0QO"><path d="M15.014 17.884a.75.75 0 01-.98 1.13l-.084-.073-6.137-6.18a.75.75 0 01-.069-.977l.073-.083 6.145-6.103a.75.75 0 011.13.98l-.073.085-5.613 5.573 5.608 5.648z" fill="currentColor"></path></svg></a>')

        # # todo: decide if to scrape all 1000+ pages or limit
        # if next_page:
        #     yield response.follow(next_page, callback=self.parse)
