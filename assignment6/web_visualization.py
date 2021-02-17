"""
Web-based visualization of the COVID-19 cases in Norwegian counties made
publicly available by the Norwegian Institute of Public Health (NIPH - FHI).
"""

#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import datetime
import json
import tempfile

import altair as alt
import pandas as pd
from flask import Flask, render_template, request

app = Flask(__name__, static_url_path='/', static_folder='docs/_build/html/')

# Global variables
allowed_counties = ['all_counties', 'agder', 'innlandet', 'more-og-romsdal',
                    'nordland', 'oslo', 'rogaland', 'troms-og-finnmark',
                    'trondelag', 'vestfold-og-telemark', 'vestland', 'viken']

county_repl = ['All Counties', 'Agder', 'Innlandet', 'Møre og Romsdal',
               'Nordland', 'Oslo', 'Rogaland', 'Troms og Finnmark',
               'Trøndelag', 'Vestfold og Telemark', 'Vestland', 'Viken']

repl_dict = dict(zip(allowed_counties, county_repl))


def read_data(county="all_counties", time_interval="daily"):
    """
    Read COVID-19 cases in Norwegian counties into Pandas DataFrame.

    Read data of COVID-19 cases in a specified Norwegian county from a
    comma-separated values (csv) file provided by the Norwegian Institute of
    Public Health (NIPH - FHI) into a Pandas DataFrame. The county can be
    specified by the ``county`` keyword argument. The time interval
    representation of reported cases can be specifed as either ``daily`` or
    ``weekly`` by the ``time_interval`` keyword argument.

    Arguments
    ---------
    county : str, optional, default ``all_counties``
        The county with the reported cases to retrieve and store in DataFrame.

        **Allowed counties:** ``all_counties``, ``agder``, ``innlandet``,
        ``more-og-romsdal``, ``nordland``, ``oslo``, ``rogaland``,
        ``troms-og-finnmark``, ``trondelag``, ``vestfold-og-telemark``,
        ``vestland``, ``viken``.
    time_interval : str, optional, default ``daily``
        Time interval representation of the reported cases. Can be either
        ``daily`` or ``weekly``.

    Returns
    -------
    df : pandas.Dataframe
        The reported cases (csv file) is returned as two-dimensional data
        structure with labeled axes.

    Raises
    ======
    TypeError
        If ``county`` or ``time_interval`` is not str.
    ValueError
        If ``county`` is not in allowed counties (see above) or if
        ``time_interval`` is not ``daily`` or ``weekly``.
    """
    if not isinstance(county, str):
        raise TypeError("'county' must be str")

    if not isinstance(time_interval, str):
        raise TypeError("'time_interval' must be str")

    if not county in allowed_counties:
        raise ValueError(f"'county' must be one of {allowed_counties}")

    if not time_interval in ["daily", "weekly"]:
        raise ValueError("'time_interval' must be either 'daily' or 'weekly'")

    path = "csv_files/"
    shared_filename = "covid-19-"
    extension = ".csv"
    df = pd.read_csv(f"{path}{shared_filename}{time_interval}-{county}{extension}",
                     parse_dates=["Dato"],
                     infer_datetime_format=True,
                     dayfirst=True)

    return df


def chart_base(county="all_counties", time_interval="daily",
               start=datetime.date(2020, 2, 21), end=datetime.date(2020, 11, 9)):
    """
    Create base of Altair Chart for COVID-19 cases in Norwegian counties.

    Arguments
    ---------
    county : str, optional, default ``all_counties``
        The county with the reported cases to retrieve and store in DataFrame.

        **Allowed counties:** ``all_counties``, ``agder``, ``innlandet``,
        ``more-og-romsdal``, ``nordland``, ``oslo``, ``rogaland``,
        ``troms-og-finnmark``, ``trondelag``, ``vestfold-og-telemark``,
        ``vestland``, ``viken``.
    time_interval : str, optional, default ``daily``
        Time interval representation of the reported cases. Can be either
        ``daily`` or ``weekly``.
    start : datetime object, optional, default ``datetime.date(2020, 2, 21)``
        Start date of reported cases to represent in Altair Chart. The object
        defaults to the date of the outbreak in Norway (Feb 21, 2020).
    end : datetime object, optional, default ``datetime.date(2020, 11, 9)``
        End date of reported cases to represent in Altair Chart. The object
        defaults to the last entry in the provided COVID-19 cases data.

    Returns
    -------
    base : altair.Chart
        Base of Altair Chart.
    """

    df = read_data(county=county, time_interval=time_interval)

    if time_interval == "weekly":
        # Convert datetime objects to Year-Week Number format
        start = start.strftime('%Y-%V')
        end = end.strftime('%Y-%V')

    source = df.set_index('Dato')[start:end]

    base = alt.Chart(source.reset_index()).encode(
        alt.X('Dato', sort=None, axis=alt.Axis(title='Date')))

    return base


def plot_reported_cases(county="all_counties", time_interval="daily", **kwargs):
    """
    Create Altair Chart of reported COVID-19 cases in Norwegian counties.

    Arguments
    ---------
    county : str, optional, default ``all_counties``
        The county with the reported cases to retrieve.

        **Allowed counties:** ``all_counties``, ``agder``, ``innlandet``,
        ``more-og-romsdal``, ``nordland``, ``oslo``, ``rogaland``,
        ``troms-og-finnmark``, ``trondelag``, ``vestfold-og-telemark``,
        ``vestland``, ``viken``.
    time_interval : str, optional, default ``daily``
        Time interval representation of the reported cases. Can be either
        ``daily`` or ``weekly``.
    **kwargs
        Arbitrary keyword arguments are passed along to ``chart_base()``.

    Returns
    -------
    bar : altair.Chart
        Altair Chart of reported cases.
    """

    base = chart_base(county=county, time_interval=time_interval, **kwargs)

    # interactive pop-up
    nearest = alt.selection(type='single', nearest=True, on='mouseover',
                            fields=['Dato'], empty='none')

    # Altair chart for reported cases
    bar = base.mark_bar(opacity=0.5, color='#5276A7').encode(
        alt.Y('Nye tilfeller:Q', sort=None, axis=alt.Axis(
            title='New cases', titleColor='#5276A7', labelColor='#5276A7')),
        tooltip=[alt.Tooltip('Dato', title='Date'), alt.Tooltip(
            'Nye tilfeller:Q', title='Reported Cases')],
    ).properties(
        title=repl_dict[county],
        width=400,
        height=300
    )

    return bar


def plot_cumulative_cases(county="all_counties", time_interval="daily", **kwargs):
    """
    Create Altair Chart of cumulative COVID-19 cases in Norwegian counties.

    Arguments
    ---------
    county : str, optional, default ``all_counties``
        The county with the reported cases to retrieve.

        **Allowed counties:** ``all_counties``, ``agder``, ``innlandet``,
        ``more-og-romsdal``, ``nordland``, ``oslo``, ``rogaland``,
        ``troms-og-finnmark``, ``trondelag``, ``vestfold-og-telemark``,
        ``vestland``, ``viken``.
    time_interval : str, optional, default ``daily``
        Time interval representation of the reported cases. Can be either
        ``daily`` or ``weekly``.
    **kwargs
        Arbitrary keyword arguments are passed along to ``chart_base()``.

    Returns
    -------
    line : altair.Chart
        Altair Chart of cumulative cases.
    """
    base = chart_base(county=county, time_interval=time_interval, **kwargs)

    nearest = alt.selection(type='single', nearest=True, on='mouseover',
                            fields=['Dato'], empty='none')

    line = base.mark_line(color='#F18727').encode(
        alt.Y('Kumulativt antall:Q', sort=None, axis=alt.Axis(
            title='Cumulative cases', titleColor='#F18727', labelColor='#F18727')),
        # tooltip=['Dato:T', 'Kumulativt antall:Q'],
        tooltip=[alt.Tooltip('Dato', title='Date'), alt.Tooltip(
            'Kumulativt antall:Q', title='Cumulative Cases')],
    ).properties(
        title=repl_dict[county],
        width=400,
        height=300
    )

    return line


def plot_both(county="all_counties", time_interval="daily", **kwargs):
    """
    Create Altair Chart of both reported and cumulative COVID-19 cases in
    Norwegian counties.

    Arguments
    ---------
    county : str, optional, default ``all_counties``
        The county with the reported cases to retrieve.

        **Allowed counties:** ``all_counties``, ``agder``, ``innlandet``,
        ``more-og-romsdal``, ``nordland``, ``oslo``, ``rogaland``,
        ``troms-og-finnmark``, ``trondelag``, ``vestfold-og-telemark``,
        ``vestland``, ``viken``.
    time_interval : str, optional, default ``daily``
        Time interval representation of the reported cases. Can be either
        ``daily`` or ``weekly``.
    **kwargs
        Arbitrary keyword arguments are passed along to ``chart_base()``.

    Returns
    -------
    both : altair.Chart
        Altair Chart of both reported and cumulative cases.
    """
    bar = plot_reported_cases(
        county=county, time_interval=time_interval, **kwargs)
    line = plot_cumulative_cases(
        county=county, time_interval=time_interval, **kwargs)

    both = alt.layer(bar, line).resolve_scale(y='independent')

    return both


@app.route("/home")
def main():
    """The main /home page serves the ``plot.html`` template"""
    return render_template("plot.html")


@app.route("/plot.json", methods=["POST"])
def plot():
    """POST requests to /plot.json

    The response will be the vega chart spec as JSON
    """
    content = request.json
    chart = content.get("chart")
    county = content.get("county")
    time_interval = content.get("interval")

    if chart == "reported":
        fig = plot_reported_cases(county=county, time_interval=time_interval)
    elif chart == "cumulative":
        fig = plot_cumulative_cases(county=county, time_interval=time_interval)
    elif chart == "both":
        fig = plot_both(county=county, time_interval=time_interval)

    return json.dumps(fig.to_dict()), 200, {"Content-Type": "application/json"}


@app.route('/help')
@app.route('/<path:path>')
def serve_sphinx_docs(path='index.html'):
    """The /help page serves the html documentation generated by Sphinx"""
    return app.send_static_file(path)


if __name__ == "__main__":
    app.run(port=5001)
