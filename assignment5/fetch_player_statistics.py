#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import re

import pandas as pd
from bs4 import BeautifulSoup
from requesting_urls import get_html


def extract_url(table, base_url):
    """
    Extract URLs from HTML table.

    First all URLs are found, and then links that occur more than once
    are found (in order to extract teams that goes to semifinal). A list
    with the (8) unique URLs is returned.

    Arguments
    ---------
    table : str
        HTML table
    base_url : str,
        Base URL which is concatened to relative URL's

    Returns
    -------
    links : list
        Found URLs of teams in semifinal
    """
    naive_links = []
    for link in table.find_all('a'):
        naive_links.append(link.get('href'))

    links = []
    for link in naive_links:
        if naive_links.count(link) > 1:
            links.append(link)

    # concatenate base url to relative URL's
    for i, link in enumerate(links):
        if link.startswith('/'):
            links[i] = base_url + link

    # unique URL's only, i.e. no duplicates
    links = list(set(links))

    return links


def find_team(url):
    """
    Extract team player URLs from HTML table.

    Arguments
    ---------
    url : str
        URL of webpage to get

    Returns
    -------
    links : list
        Found URLs of team players
    """
    r = get_html(url)
    soup = BeautifulSoup(r.text, 'lxml')
    base_url = "https://en.wikipedia.org"

    identifier = {"class": "toccolours"}
    outer_table = soup.find("table", identifier)

    table = outer_table.find("table")

    rows = table.find_all("tr")[1:]
    links = []
    for row in rows:
        cells = row.find_all("td")
        name = cells[2]
        # print(name)
        link = name.find('a')
        links.append(link.get('href'))

    # concatenate base url to relative URL's
    for i, link in enumerate(links):
        if link.startswith('/'):
            links[i] = base_url + link

    return links


def find_player(url):
    """
    Not finished
    """
    r = get_html(url)
    soup = BeautifulSoup(r.text, 'lxml')

    identifier = {"class": "wikitable sortable jquery-tablesorter"}
    table = soup.find("table", identifier)

    rows = table.find_all("tr")[1:]

    for row in rows:
        cells = row.find_all("td")
        if cells[0].text.strip() == "2019–20":
            print(True)


if __name__ == "__main__":
    url = "https://en.wikipedia.org/wiki/2020_NBA_playoffs"
    base_url = "https://en.wikipedia.org"
    r = get_html(url)
    soup = BeautifulSoup(r.text, 'lxml')

    start_loc = soup.find(id="Bracket")
    table = start_loc.find_next("table")

    links = extract_url(table, base_url)

    print("SEMINFINAL LINKS:")
    print("")
    for link in links:
        print(link)
    print("")
    print("TEAM PLAYERS:")
    print("")
    for link in links:
        print("Team:", link)
        links2 = find_team(link)
        for link2 in links2:
            print(link2)
        print("")
