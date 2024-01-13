START_ID?=
START_URL?=https://www.wikitree.com/wiki/$(START_ID)
MAX_URLS?=10


venv: venv_install
	# activate virtual environment
	source venv/bin/activate

venv_install:
	# create virtual environment
	# python3 -m venv venv	(overwrites existing venv)
	# (todo - create virtual environment if not exists)

install: venv
	# install requirements
	pip install -r requirements.txt

# crawl scripts

wikitree:
	# run wikitree.py
	@scrapy runspider scripts/wikitree.py\
		-s NAME=wikiancestry\
		--loglevel=DEBUG\
		--output=./output/wikitree/${START_ID}.${MAX_URLS}.json:json\
		&& echo "# make wikitree complete"

wikitree_shell:
	# run debug shell for url
	# ex:
	# 	response.css("title::text")[0].get()
	#
	scrapy shell https://www.wikitree.com/wiki/Wolgemuth-10
