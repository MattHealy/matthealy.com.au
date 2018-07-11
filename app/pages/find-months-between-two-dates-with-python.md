title: Finding all months between two dates with Python
timestamp: 2018-07-12 00:00:00
slug: find-months-between-two-dates-with-python
tags: [code-snippets, python, tips-and-tricks]
author: Matt Healy

I recently wrote an API endpoint for a project at <a href="https://www.vaultrealestate.com.au/">VaultRealEstate</a> which required me to generate a month-by-month commission summary breakdown for a sales agent. The API endpoint accepts an arbitrary start and end month and should return a JSON object showing all the distinct months in that date range and the commission performance for those months (for example, for displaying a bar chart).

I found that this was actually not a trivial problem, and built-in Python libraries like <a href="https://docs.python.org/3/library/datetime.html">datetime</a> can't really solve this problem nicely. There are third party libraries like <a href="https://dateutil.readthedocs.io/en/stable/">dateutil</a> which can solve the problem, and normally I would immediately go for a library like this. However, this project is hosted on <a href="https://aws.amazon.com/lambda/">AWS Lambda</a> and I'm conscious about the deployment size of the project getting bigger with each dependency introduced, so I really like to only introduce a dependency when it's necessary.

I found the following StackOverflow answer which seemed to suit my needs:

<a href="https://stackoverflow.com/a/34898764/272193">https://stackoverflow.com/a/34898764/272193</a>

Adapting the answer for my use case results in the below snippet.


    from datetime import datetime, timedelta
    from collections import OrderedDict

    # Sample start and end dates
    start = datetime(year=2017, month=10, day=1)
    end = datetime(year=2018, month=3, day=1)

    # Get list of months >= start and < end

    months = OrderedDict(((start + timedelta(_)).strftime("%Y-%m-01"), 0) for _ in range((end - start).days)) 
    # OrderedDict([('2017-10-01', 0), ('2017-11-01', 0), ('2017-12-01', 0), ('2018-01-01', 0), ('2018-02-01', 0)])
