# open-ancestry

json \ python scripts - from wiki-ancestry and others

## getting started

download repository

```sh
 1513  pwd
 1514  cd Desktop
 1515  g clone git@github.com:david-wolgemuth/open-ancestry.git
 1516  cd open-ancestry
 1517  g status
```

create python virtual environment

```sh
 1518  python -m venv
 1519  python3 -m venv
 1520  python3 -m venv ./venv
 1521  ls
 1522  source venv/bin/activate
```

add a breakpoint

```py
# SET DEBUGGER BREAKPOINT
__import__("ipdb").set_trace()  # DO NOT COMMIT
```

## reading


> Fun With Scrapy Link Validation on CI
> https://www.mattlayman.com/blog/2024/fun-scrapy-validation-ci/
>
> The Spider
>
> As I mentioned earlier, we’re going to use Scrapy. Scrapy has a ton of great web scraping tool and pre-built spiders that we can use and extend.
>
> After installing Scrapy with pip install scrapy, you’ll get a scrapy command line tool to issue more commands. I needed a new project and a spider skeleton to start. Here’s how to get bootstrapped:
>
> $ scapy startproject checker .
> $ scrapy genspider -t crawl crawler http://localhost:8000
>
> That . at the end of the startproject command was important. By doing that, we can skip an extra directory layer that Scrapy wanted to add. Instead, we’ve got a scrapy.cfg file in the root as well as the checker directory that contains the Scrapy project code.
>
> Now I’m going to throw the spider code at you to digest. The important bits will be highlighted after the code.
>
> from scrapy.linkextractors import LinkExtractor
> from scrapy.spiders import CrawlSpider, Rule
>
>
> ```py
> class Spider(CrawlSpider):
>   name = "crawler"
>   allowed_domains = ["localhost"]
>   start_urls = ["http://localhost:8000"]
>
>   def parse(self, response):
>      if response.status == 404:
>           yield {"url": response.url}
>
> ```
