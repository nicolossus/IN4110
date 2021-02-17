#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os

import requests as req


def get_html(url, params=None, output=None, **kwargs):
    """
    Request to fetch data from website of choice.

    Arguments
    ---------
    url : str
        URL of webpage to get
    params : dict, optional, default None
        Data to send in the URL's query string
    output : str, optional, default None
        Optional output filename to store webpage data, in form of the HTML
        body, in. Filename can be specified without extension as .txt will be
        added regardless whether specified or not.
    **kwargs
        Arbitrary keyword arguments are passed along to requests.get

    Returns
    -------
    r : object
        Response object

    Raises
    ------
    TypeError : if 'url' and/or 'output' is not str
    """

    if not isinstance(url, str):
        raise TypeError("'url' must be website address as str")

    r = req.get(url, params=params, **kwargs)

    if output is not None:
        if not isinstance(output, str):
            raise TypeError("'output' must be str")

        filename, file_extension = os.path.splitext(output)
        if file_extension != ".txt":
            file_extension = ".txt"

        filename = filename + file_extension
        with open(filename, "w") as f:
            f.write(r.text)

    return r


if __name__ == "__main__":
    path = "requesting_urls/"

    r = get_html("https://en.wikipedia.org/wiki/Studio_Ghibli",
                 output=path + "Studio_Ghibli")

    r = get_html("https://en.wikipedia.org/wiki/Star_Wars",
                 output=path + "Star_Wars")

    r = get_html("https://en.wikipedia.org/wiki/Dungeons_%26_Dragons",
                 output=path + "Dungeons_Dragons")

    r = get_html("https://en.wikipedia.org/w/index.php",
                 params={"title": "Main_Page", "action": "info"},
                 output=path + "Main_Page")

    r = get_html("https://en.wikipedia.org/w/index.php",
                 params={"title": "Hurricane_Gonzalo", "oldid": "983056166"},
                 output=path + "Hurricane_Gonzalo")
