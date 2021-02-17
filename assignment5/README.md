## IN4110 - Assignment 5

### Regular Expressions and Web Scraping

#### Dependencies

`Python3`: version 3.7

`requests`: version 2.24.0

`bs4`: version 4.9.3

`lxml`: version 4.6.1

`pandas`: version 1.1.3

`tabulate`: version 0.8.7

#### Install Dependencies

    $ conda install requests bs4 lxml pandas tabulate

or

    $ pip install requests bs4 lxml pandas tabulate


#### 5.1 Sending URL Requests

Run program with

    $ python requesting_urls.py

Results are located in the `requesting_urls` folder.

**Example Usage:**

```python
from requesting_urls import get_html

# URL of webpage to get
url = "https://en.wikipedia.org/w/index.php"

# Data to send in the URL's query string (optional)
params = {"title": "Hurricane_Gonzalo", "oldid": "983056166"}

# Output filename (optional). Can be specified w/o .txt extension
output = "filename"

# Retrieve response object
r = get_html(url, params=params, output=output)
```

#### 5.2 Regex for Filtering URLs

Run program with

    $ python filter_urls.py

Results are located in the `filter_urls` folder.

**Example Usage:**

```python
from requesting_urls import get_html
from filter_urls import find_urls, find_articles

# URL of webpage to get
url = "https://en.wikipedia.org/wiki/Nobel_Prize"

# Base URL (optional). If relative URLs should prepend base URL
base_url = "https://en.wikipedia.org"

# Output filename (optional). Can be specified w/o .txt extension
output = "filename"

# Retrieve response object
r = get_html(url)

# Find all URLs (anchored hyperlinks in raw HTML)
m = find_urls(r.text, base_url=base_url, output=output)

# Find Wikipedia articles (base URL prepend relative URLs automatically)
m = find_articles(url, output=output)
```

#### 5.3 Regex for Finding Dates

Run program with

    $ python collect_dates.py

Results are located in the `filter_dates_regex` folder.

**Example Usage:**

```python
from requesting_urls import get_html
from collect_dates import find_dates

# URL of webpage to get
url = "https://en.wikipedia.org/wiki/Linus_Pauling"

# Output filename (optional). Can be specified w/o .txt extension
output = "filename"

# Retrieve response object
r = get_html(url)

# Find dates in raw HTML (see docstring for supported formats)
m = find_dates(r.text, output=output)
```

#### 5.4 Soup for Filtering Datetime Objects

Run program with

    $ python time_planner.py

Results are located in the `datetime_filter` folder.

#### 5.5 NBA Player Statistics Season 2019/2020

Run program with

    $ python fetch_player_statistics.py

Results are located in the `NBA_player_statistics` folder.
