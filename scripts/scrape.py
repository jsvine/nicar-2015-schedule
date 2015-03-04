#!/usr/bin/env python
import requests
import lxml.html
import unicodecsv
import itertools
import argparse
import json
import sys
import re

SCHEDULE_URL = "http://www.ire.org/events-and-training/event/1494/"
DATES = [ "2015-03-04", "2015-03-05", "2015-03-06", "2015-03-07", "2015-03-08" ]

def fix_encoding(string):
    """
    Fix embedded utf-8 bytestrings.
    Solution via http://bit.ly/1DEpdmQ
    """
    pat = ur"[\xc2-\xf4][\x80-\xbf]+"
    fix = lambda m: m.group(0).decode("utf-8")
    return re.sub(pat, fix, string)

def flatten(nested_list):
    """
    Given a nested list, return a flat version.
    e.g., [ [1, 2, 3], [4, 5, 6] ] -> [ 1, 2, 3, 4, 5, 6 ]
    """
    return list(itertools.chain.from_iterable(nested_list))

def extract_speakers(description):
    """
    If speakers are listed in the first paragraph of the description,
    extract them.
    """
    speaker_pat = re.compile(r"^(Speakers?: ([^\n]+))?(.*)$", re.DOTALL)
    match = re.match(speaker_pat, description)
    graf, names, rest = match.groups()
    return names, rest.strip()

def parse_session(el, date):
    """
    Given an HTML element containing one session and the date of the session,
    extract the key information.
    """
    s_type = el.cssselect(".col-10")[0].text_content().strip()
    s_title = el.cssselect(".title3")[0].text_content().strip()
    grafs = el.cssselect(".col-60 p")
    s_desc = "\n\n".join(p.text_content().strip() for p in grafs).strip()
    s_desc_compact = re.sub(r"\n\n+", "\n\n", s_desc)
    s_speakers, s_description = extract_speakers(s_desc_compact)
    details = el.cssselect(".meta p")
    s_room, s_time = (p.text_content().strip() for p in details)
    return {
        "type": s_type,
        "title": s_title,
        "description": s_description,
        "speakers": s_speakers,
        "room": s_room,
        "time": s_time,
        "date": date,
    }
    
def parse_day(el, date):
    """
    Given an HTML element containing a day's worth of sessions,
    pass each session element to the parser and return the results.
    """
    session_els = list(el)
    sessions_data = [ parse_session(s, date) for s in session_els ]
    return sessions_data

def get_sessions():
    """
    Fetch and parse the schedule HTML from the NICAR webpage.
    """
    html = fix_encoding(requests.get(SCHEDULE_URL).content)
    dom = lxml.html.fromstring(html)
    day_els = dom.cssselect("ul.listview.pane")
    days_zipped = zip(day_els, DATES)
    sessions_nested = [ parse_day(el, date) for el, date in days_zipped ]
    sessions = flatten(sessions_nested)
    return sessions

def print_sessions(sessions, fmt):
    """
    Print the schedule data to stdout, as either JSON or CSV.
    """
    if fmt == "json":
        json.dump(sessions, sys.stdout, indent=4)
    elif fmt == "csv":
        fields = [ "date", "time", "type", "title", "description", "speakers", "room" ]
        writer = unicodecsv.DictWriter(sys.stdout, fields, encoding="utf-8")
        writer.writeheader()
        writer.writerows(sessions)
    else:
        raise ValueError("'{0}' is not a supported format".format(fmt))

def main():
    """
    Get the data and print it.
    """
    parser = argparse.ArgumentParser()
    parser.add_argument("--format", default="json")
    fmt = parser.parse_args().format
    sessions = get_sessions()
    print_sessions(sessions, fmt)

if __name__ == "__main__":
    main()
