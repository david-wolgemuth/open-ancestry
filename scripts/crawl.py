

from scrapy.spiders import CrawlSpider, Spider
#from scrapy.spiders import Rule

# from scrapy.linkextractors import LinkExtractor


class Crawl(Spider):
    """
    Thin wrapper around scrapy crawler

    ---

    Scrapy CLI usage (convenience copied from `scrapy runspider --help`):

    (venv) (venv) [main*][modifieduntracked]scrapy runspider --help

        Usage
        =====
        scrapy runspider [options] <spider_file>

        Run the spider defined in the given file

        Options
        =======
        -h, --help            show this help message and exit
        -a NAME=VALUE         set spider argument (may be repeated)
        -o FILE, --output FILE
                                append scraped items to the end of FILE (use - for stdout), to define format set a colon at the end of the output URI (i.e.
                                -o FILE:FORMAT)
        -O FILE, --overwrite-output FILE
                                dump scraped items into FILE, overwriting any existing file, to define format set a colon at the end of the output URI
                                (i.e. -O FILE:FORMAT)
        -t FORMAT, --output-format FORMAT
                                format to use for dumping items

        Global Options
        --------------
        --logfile FILE        log file. if omitted stderr will be used
        -L LEVEL, --loglevel LEVEL
                                log level (default: DEBUG)
        --nolog               disable logging completely
        --profile FILE        write python cProfile stats to FILE
        --pidfile FILE        write process ID to FILE
        -s NAME=VALUE, --set NAME=VALUE
                                set/override setting (may be repeated)
        --pdb                 enable pdb on failure
    """
    pass
