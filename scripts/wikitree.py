import logging
import os

from typing import Any, Optional
from scrapy import Request
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import Rule, Spider
from crawl import Crawl


EXCLUDE = [
    "wikitree.com/wiki/Help:",
    "wikitree.com/wiki/Special:",
]


START_URL = os.environ.get("START_URL", "https://www.wikitree.com/wiki/Wolgemuth-10")
MAX_URLS = int(os.environ.get("MAX_URLS", 10))


class WikiAncestryLinkExtractor(LinkExtractor):
    def extract_links(self, response):
        for link in super().extract_links(response):
            # Link(
            #   url='https://www.wikitree.com/wiki/Help:About_WikiTree',
            #   text='ABOUT',
            #   ...
            # )
            logging.debug(f"extract_links.link: {link}")

            if any(exclude in link.url for exclude in EXCLUDE):
                logging.debug(f"extract_links.exclude: {link}")
                continue

            if "wikitree.com/wiki/" in link.url:

                logging.debug(f"extract_links.match: {link}")
                yield link


class WikiAncestryCrawl(Crawl):
    """
     $ scrapy genspider -t crawl crawler http://localhost:8000


    :param CrawlSpider:
    :yield:

    """
    output_dir = "data/wikitree"

    max_urls = MAX_URLS
    name = "crawler"
    allowed_domains = ["wikitree.com"]
    start_urls = [START_URL]

    rules = [
        # Rule(WikiAncestryLinkExtractor(), callback="parse")
        Rule(LinkExtractor(allow=r".*"), callback="parse")

        # Rule(LinkExtractor(allow="/wiki/"), callback="parse"),
    ]

    def __init__(self, name=None, **kwargs):
        super().__init__(name, **kwargs)
        self.urls_seen = []
        self.queue = []

    def parse(self, response):
        """
        """
        self.urls_seen.append(response.url)

        logging.debug(f"parse: {response.url}")
        parent_urls = response.css(".VITALS [itemprop=parent] a::attr(href)").getall()
        sibling_urls = response.css(".VITALS [itemprop=sibling] a::attr(href)").getall()
        spouse_urls = response.css(".VITALS [itemprop=spouse] a::attr(href)").getall()
        children_urls = response.css(".VITALS [itemprop=children] a::attr(href)").getall()

        if response.status != 200:
            logging.warning(f"parse.status: {response.status}")
            return

        yield {
            "url": response.url,
            "id": response.url.split("/")[-1],
            "name": response.css(".VITALS [itemprop=name] ::text").get(),
            "birth_date": response.css(".VITALS [itemprop=birthDate]::attr(datetime)").get(),
            "birth_place": response.css(".VITALS [itemprop=birthPlace] ::text").get(),
            "death_date": response.css(".VITALS [itemprop=deathDate]::attr(datetime)").get(),
            "life_span": response.css(".VITALS span[title]::attr(title)").get(),
            "status": response.status,
            "title": response.xpath("//title/text()").get(),
            "h1": response.xpath("//h1/text()").getall(),
            "h2": response.xpath("//h2/text()").getall(),
            "h3": response.xpath("//h3/text()").getall(),

            "vitals": response.css(".VITALS").getall(),
            "vitals_html": response.css(".VITALS").getall(),

            "gender": response.css(".VITALS  [itemprop=gender] ::text").get(),
            "gender_hmtl": response.css(".VITALS  [itemprop=gender]").get(),

            "parents": response.css(".VITALS  [itemprop=parent] ::text").getall(),
            "parents_html": response.css(".VITALS  [itemprop=parent]").getall(),
            "parent_urls": parent_urls,

            "siblings": response.css(".VITALS  [itemprop=sibling] ::text").getall(),
            "siblings_html": response.css(".VITALS  [itemprop=sibling]").getall(),
            "sibling_urls": sibling_urls,

            "spouses": response.css(".VITALS  [itemprop=spouse] ::text").getall(),
            "spouses_html": response.css(".VITALS  [itemprop=spouse]").getall(),
            "spouse_urls": spouse_urls,

            "children": response.css(".VITALS  [itemprop=children] ::text").getall(),
            "children_html": response.css(".VITALS  [itemprop=children]").getall(),
            "children_urls": children_urls,
        }

        # breadth-first search
        for url in parent_urls + sibling_urls + spouse_urls + children_urls:
            if len(self.urls_seen) <= self.max_urls:
                self.queue.append(url)

        logging.debug(f"parse.urls_seen: {len(self.urls_seen)}")
        if len(self.urls_seen) >= self.max_urls:
            logging.info(f"parse.urls_seen hit limit: {len(self.urls_seen)}")
            return

        # # yield Request(response.urljoin(href), self.parse)
        # yield response.follow(href, callback=self.parse)

        while self.queue:
            next_href = self.queue.pop(0)
            if next_href in self.urls_seen:
                # (this filtered out by default)
                logging.debug(f"parse.follow: {next_href} already seen")
                continue

            logging.info(f"parse.follow: {next_href}")
            if len(self.urls_seen) >= self.max_urls:
                logging.info(f"parse.urls_seen hit limit: {len(self.urls_seen)}")
                return

            yield response.follow(next_href, callback=self.parse)
