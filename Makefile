BASEPATH=output/nicar-2015-schedule
OUTPUTS=$(BASEPATH).json $(BASEPATH).csv
.PHONY: $(OUTPUTS)

schedules: $(OUTPUTS)

$(BASEPATH).json: scripts/scrape.py
	./scripts/scrape.py --format json > $@

$(BASEPATH).csv: scripts/scrape.py
	./scripts/scrape.py --format csv > $@
