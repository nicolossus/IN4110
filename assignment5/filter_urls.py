#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import re

from requesting_urls import get_html


def find_urls(raw_html, base_url=None, output=None):
    """
    Find URL's in raw HTML.

    Find anchored hyperlink URL's, both absolute and relative, in raw HTML using
    regular expressions (regex). Fragments are excluded from URL, and base URL
    can be concatened to relative URL's by specifying the keyword argument.

    Arguments
    ---------
    raw_html : str
        HTML of webpage with anchored hyperlinks
    base_url : str, optional, default None
        Base URL which is concatened to relative URL's if specified
    output : str, optional, default None
        Optional output filename to store the found URL's. Filename can be
        specified without extension as .txt will be added regardless whether
        specified or not.

    Returns
    -------
    matches : list
        Found URL's

    Raises
    ------
    TypeError : if 'base_url' and/or 'output' is not str
    """
    # define regex pattern for anchored hyperlinks
    pattern = re.compile(r'<a\s+(?:[^>]*?\s+)?href="(.*?)(?:#.+)?"')
    # find matches and filter out empty hits
    matches = list(filter(None, pattern.findall(raw_html)))

    # some URL's might be relative and start with //, i.e. https: omitted. Fix:
    for i, match in enumerate(matches):
        if match.startswith('//'):
            matches[i] = "https:" + match

    if base_url is not None:
        if not isinstance(base_url, str):
            raise TypeError("'base_url' must be str")
        # concatenate base url to relative URL's
        for i, match in enumerate(matches):
            if match.startswith('/'):
                matches[i] = base_url + match

    # unique URL's only, i.e. no duplicates
    matches = list(set(matches))

    if output is not None:
        if not isinstance(output, str):
            raise TypeError("'output' must be str")

        filename, file_extension = os.path.splitext(output)
        if file_extension != ".txt":
            file_extension = ".txt"

        filename = filename + file_extension
        with open(filename, "w") as f:
            for line in matches:
                f.write(line + "\n")

    return matches


def find_articles(url, params=None, output=None, **kwargs):
    """
    Find wikipedia article URL's linked in Wikipedia webpage.

    Request to fetch data from Wikipedia website of choice, find all
    anchored hyperlinks and filter out wikipedia article URL's only.

    Arguments
    ---------
    url : str
        URL of (Wikipedia) webpage to get
    params : dict, optional, default None
        Data to send in the URL's query string
    output : str, optional, default None
        Optional output filename to store the found article URL's. Filename can
        be specified without extension as .txt will be added regardless whether
        specified or not.
    **kwargs
        Arbitrary keyword arguments are passed along to requests.get
        in get_html()

    Returns
    -------
    matches : list
        Found URL's

    Raises
    ------
    TypeError : if 'output' is not str
    """
    # response object
    r = get_html(url, params=params, **kwargs)

    # define regex pattern for base URL
    base_url_pattern = r'^.+?[^\/:](?=[?\/]|$)'
    # extract base URL from URL
    base_url = re.search(base_url_pattern, url).group(0)

    # find all anchored hyperlinks from raw HTML
    all_urls_list = find_urls(r.text, base_url=base_url)

    # define regex pattern for wikipedia articles only
    article_pattern = re.compile(r'^https?://(?!.*:[^_]).*wiki.*')
    # search for pattern match in list
    matches = list(filter(article_pattern.match, all_urls_list))

    if output is not None:
        if not isinstance(output, str):
            raise TypeError("'output' must be str")

        filename, file_extension = os.path.splitext(output)
        if file_extension != ".txt":
            file_extension = ".txt"

        filename = filename + file_extension
        with open(filename, "w") as f:
            for line in matches:
                f.write(line + "\n")

    return matches


if __name__ == "__main__":

    # test cases
    urls = ["https://en.wikipedia.org/wiki/Nobel_Prize", "https://en.wikipedia.org/wiki/Bundesliga",
            "https://en.wikipedia.org/wiki/2019–20_FIS_Alpine_Ski"]
    outputs = ["Nobel_Prize", "Bundesliga", "2019–20_FIS_Alpine_Ski"]

    path_all = "filter_urls/all_urls_"
    path_article = "filter_urls/articles_"
    base_url = "https://en.wikipedia.org"

    for url, output in zip(urls, outputs):
        r = get_html(url)
        m_all = find_urls(r.text, base_url=base_url, output=path_all + output)
        m_articles = find_articles(url, output=path_article + output)

    r = get_html("https://en.wikipedia.org/wiki/Studio_Ghibli")
    m = find_urls(r.text, base_url="https://en.wikipedia.org",
                  output="filter_urls/all_urls_Studio_Ghibli")

    m = find_articles("https://en.wikipedia.org/wiki/Studio_Ghibli",
                      output="filter_urls/articles_Studio_Ghibli")
