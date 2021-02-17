#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import re

import pandas as pd
from bs4 import BeautifulSoup
from collect_dates import find_dates
from requesting_urls import get_html


def extract_events(raw_html, identifier={}, output="betting_slip_empty.md"):
    """
    Make betting slip for FIS Alpine Ski World Cup Events.

    Extract events from Wikipedia table and make a betting slip in markdown
    for handing out to friends.

    Arguments
    ---------
    raw_html : str
        HTML of webpage
    identifier : dict, optional, default empty
        Table identifiers
    output : str, optional, default 'betting_slip_empty.md'
        Optional output filename for markdown (.md) betting slip

    Returns
    -------
    None
    """
    soup = BeautifulSoup(r.text, 'lxml')
    table = soup.find("table", identifier)
    headers = [th.text.strip() for th in table.find_all('th')]

    rows = table.find_all("tr")[1:]
    found_event = None
    found_venue = None
    found_type = None
    prev_venue = None
    events = []

    for row in rows:
        cells = row.find_all("td")
        if len(cells) > 3:
            event = cells[headers.index('Event')]
            if re.match(r"\d{1,3}$", event.text.strip()):
                found_event = event.text.strip()
            else:
                found_event = None

            if not event.find("span"):
                if found_event is not None:
                    date = cells[headers.index('Date')]
                    found_date = find_dates(str(date))[1]

                if found_event is None:
                    venue = cells[headers.index('Venue') - 1]
                else:
                    venue = cells[headers.index('Venue')]

                if venue.find("span"):
                    found_venue = venue.text.strip()

                if found_venue == prev_venue and prev_venue is not None:
                    type = cells[headers.index('Type') - 1]
                else:
                    type = cells[headers.index('Type')]

                found_type = type.text.strip()

                prev_venue = found_venue

                print(f"{found_event}, {found_date}, {found_venue}")
                if found_event is not None:
                    discipline = m = re.match(r'[A-Z]{2}', found_type).group(0)
                    events.append((found_date, found_venue, discipline))

        df = pd.DataFrame(events, columns=['DATE', 'VENUE', 'DISCIPLINE'])
        df["Who Wins?"] = ""

        markdown = df.to_markdown()

        with open(output, 'w') as f:
            f.write("## Betting Slip\n\n**Name:**\n\n")
            f.write(markdown)


if __name__ == "__main__":
    # 2019-2020 season
    url = "https://en.wikipedia.org/wiki/2019–20_FIS_Alpine_Ski_World_Cup"
    r = get_html(url)
    identifier = {"class": "wikitable plainrowheaders"}
    extract_events(r.text, identifier=identifier,
                   output="datetime_filter/2019_2020_betting_slip_empty.md")

    # 2020-2021 season
    url = "https://en.wikipedia.org/wiki/2020%E2%80%9321_FIS_Alpine_Ski_World_Cup"
    r = get_html(url)
    identifier = {"class": "wikitable plainrowheaders"}
    extract_events(r.text, identifier=identifier,
                   output="datetime_filter/2020_2021_betting_slip_empty.md")
