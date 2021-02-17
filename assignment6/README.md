# IN4110 Assignment 6

Python version 3.7 >

Install dependencies

    $ pip install requirements.txt

Start server with:

    $ python web_visualization.py

The home page is hosted at http://127.0.0.1:5001/home

Update docs page: `cd` into `docs` folder and run

    $ make html

The help page is hosted at http://127.0.0.1:5001/help

**Comment:** The function `plot_both()` displays the **Cumulative number of cases** on the *right-hand side y-axis* and the **Number of reported cases** on the *left-hand side y-axis*, opposite of the specification given in the exercise text. The change is, however, intentional, as I thought this was more aesthetically pleasing.
