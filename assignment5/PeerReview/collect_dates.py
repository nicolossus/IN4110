#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import re
from calendar import month_abbr, month_name
from requesting_urls import get_html


def find_dates(raw_html, output=None):
    """
    Find dates in raw HTML.

    Parse HTML with regex to find dates with supported formats. The dates
    returned are formatted like year/month/day (or year/month if day is
    missing). The dates are returned ordered.

    List of supported formats:

    DMY: 13 October 2020
    MDY: October 13, 2020
    YMD: 2020 October 13
    MY: October 2020 AND  October, 2020
    ISO: 2020-10-13

    Arguments
    ---------
    raw_html : str
        HTML of webpage to parse
    output : str, optional, default None
        Optional output filename to store the found dates. Filename can be
        specified without extension as .txt will be added regardless whether
        specified or not.

    Returns
    -------
    matches : list
        Found dates (ordered)

    Raises
    ------
    TypeError : if 'output' is not str
    """

    all_matches = []  # for storing final results

    # regex for DAY pattern (ISO)
    day = '(?P<day>[0-9]{2})'
    # regex for DAY pattern (more flexible, allows e.g. 1 Jan and 01 Jan)
    day2 = '(?P<day>[0-9]{1}|[0-9]{2})'
    # regex for YEAR pattern
    year = '(?P<year>[0-9]{4})'
    # regex for MONTH pattern (digits)
    month_d = '(?P<month_d>[0-9]{2})'
    # regex for MONTH pattern (words)
    months = '|'.join(list(month_abbr[1:])+list(month_name[1:]))
    month_w = f"(?P<month_w>(?:{months}))"

    # Replacement dict: text month -> numeric month
    repl_dict = dict(map(reversed, enumerate(month_abbr)))
    repl_dict.update(dict(map(reversed, enumerate(month_name))))
    for k, v in repl_dict.items():
        repl_dict[k] = str(v).zfill(2)

     # regex pattern for ISO format
    regex_iso = re.compile(fr'{year}-{month_d}-{day}')
    # check for occurrence
    search_iso_match = re.search(regex_iso, raw_html)
    if search_iso_match is not None:
        # if occurrence, find all matches
        iso_matches = re.findall(regex_iso, raw_html)
        for iso_match in iso_matches:
            # reformat and append to final result storage
            all_matches.append(f"{iso_match[0]}/{iso_match[1]}/{iso_match[2]}")

    # regex pattern for DMY
    regex_dmy = re.compile(fr'{day2}\ {month_w}\ {year}')
    # check for occurrence
    search_dmy_match = re.search(regex_dmy, raw_html)
    # print(search_dmy_match)
    if search_dmy_match is not None:
        # if occurrence, find all matches
        dmy_matches = re.findall(regex_dmy, raw_html)
        for dmy_match in dmy_matches:
            all_matches.append(
                f"{dmy_match[2]}/{repl_dict[dmy_match[1]]}/{dmy_match[0].zfill(2)}")

    # regex pattern for MDY
    regex_mdy = re.compile(fr'{month_w}\ {day2}\, {year}')
    # check for occurrence
    search_mdy_match = re.search(regex_mdy, raw_html)
    # print(search_dmy_match)
    if search_mdy_match is not None:
        # if occurrence, find all matches
        mdy_matches = re.findall(regex_mdy, raw_html)
        for mdy_match in mdy_matches:
            all_matches.append(
                f"{mdy_match[2]}/{repl_dict[mdy_match[0]]}/{mdy_match[1].zfill(2)}")

    # regex pattern for YMD
    regex_ymd = re.compile(fr'{year}\ {month_w}\, {day2}')
    # check for occurrence
    search_ymd_match = re.search(regex_ymd, raw_html)
    # print(search_dmy_match)
    if search_ymd_match is not None:
        # if occurrence, find all matches
        ymd_matches = re.findall(regex_ymd, raw_html)
        for ymd_match in ymd_matches:
            all_matches.append(
                f"{ymd_match[0]}/{repl_dict[ymd_match[1]]}/{ymd_match[2].zfill(2)}")

    # regex pattern for MY
    regex_my = re.compile(fr'{month_w}(?:\,?)(?:\s?)+{year}')
    # check for occurrence
    search_my_match = re.search(regex_my, raw_html)
    # print(search_dmy_match)
    if search_my_match is not None:
        # if occurrence, find all matches
        my_matches = re.findall(regex_my, raw_html)
        for my_match in my_matches:
            all_matches.append(
                f"{my_match[1]}/{repl_dict[my_match[0]]}")

    # sort dates
    all_matches.sort()

    if output is not None:
        if not isinstance(output, str):
            raise TypeError("'output' must be str")

        filename, file_extension = os.path.splitext(output)
        if file_extension != ".txt":
            file_extension = ".txt"

        filename = filename + file_extension
        with open(filename, "w") as f:
            for line in all_matches:
                f.write(line + "\n")

    return all_matches


if __name__ == "__main__":

    urls = ["https://en.wikipedia.org/wiki/Linus_Pauling",
            "https://en.wikipedia.org/wiki/Hans_Rosling",
            "https://en.wikipedia.org/wiki/Rafael_Nadal",
            "https://en.wikipedia.org/wiki/J._K._Rowling",
            "https://en.wikipedia.org/wiki/Richard_Feynman"]

    outputs = ["Linus_Pauling", "Hans_Rosling",
               "Rafael_Nadal", "J_K_Rowling", "Richard_Feynman"]

    path = "filter_dates_regex/dates_"

    for url, output in zip(urls, outputs):
        r = get_html(url)
        dates = find_dates(r.text, output=path + output)
