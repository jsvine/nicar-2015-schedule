# NICAR 2015 Schedule CSV & JSON

This repository contains the [NICAR 2015 conference schedule](http://www.ire.org/events-and-training/event/1494/) as structured data, plus the underlying Python scraper.

## Get the data

*Last updated March 3, 2015, 3:30 p.m.  Eastern*

- [CSV schedule](output/nicar-2015-schedule.csv?raw=true)
- [JSON schedule](output/nicar-2015-schedule.json?raw=true)

## Run the scraper yourself

To download the script and install the necessary Python libraries, execute the following commands in your terminal:

```bash
mkvirtualenv nicar-2015 # Optional, recommended
git clone https://github.com/jsvine/nicar-2015-schedule.git
cd nicar-2015-schedule
pip install -r requirements.txt
```

To run the scraper, execute this command:

```bash
make schedules
```

*Or*, more verbosely:

```bash
python scripts/scrape.py --json > output/nicar-2015-schedule.json
python scripts/scrape.py --csv > output/nicar-2015-schedule.csv
```

## Look beneath the hood

You can find the Python script that extracts and formats the schedule [here](scripts/scrape.py).

## Fix/improve things

Pull requests are welcome.
