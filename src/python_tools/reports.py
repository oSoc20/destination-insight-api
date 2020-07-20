import pandas as pd
import datetime
from collections import Counter
import matplotlib.pyplot as plt

from misc import filter_position
from misc import query_data

def count_repetitions(column,
                      start = None,
                      end = None,
                      date_type = None,
                      df = None,
                      side = None,
                      quantity = None,
                      draw_plot = False,
                      return_json = False):
    """Count the repetitions for each unique value in the specific column"""

    # query data if no dataframe is provided
    if not df:
        df = query_data([column], start, end, date_type)

    # count repetitions of unique values
    counter = df[column].value_counts().reset_index()
    counter.columns = [column.title(), 'Counts']

    # draw plot
    if draw_plot:
        counter.hist(column='Counts', bins=10, log=True)
        plt.title(column.title() + ' Stations')
        plt.xlabel('Number of searches')
        plt.ylabel('Number of stations')
        plt.savefig('output/' + column + '.png')

    # give top (or bottom) unique values (by count)
    counter = filter_position(counter, side = side, quantity = quantity)

    # return in json format
    if return_json:
        counter = counter.to_json(orient='records')

    return counter

def count_links(start = None,
                end = None,
                date_type = None,
                df = None,
                side = None,
                quantity = None,
                draw_plot = False,
                return_json = False):
    """Count the repetitions for each link between stations"""

    # query data if no dataframe is provided
    if not df:
        df = query_data(['origin', 'destination'], start, end, date_type)

    # count repetitions of unique departure-destination pairs
    destination_pairs = [set([row[1]['origin'], row[1]['destination']]) for row in df.iterrows()]
    counter = Counter(frozenset(s) for s in destination_pairs)
    counter = pd.DataFrame.from_dict(counter, orient='index').reset_index()
    counter.columns = ['DestinationPairs', 'Counts']
    counter['DestinationPairs'] = [' to/from '.join(list(item)) for item in counter['DestinationPairs']]
    counter = counter.sort_values(by=['Counts'], ascending=False)

    # draw plot
    if draw_plot:
        counter.hist(column='Counts', bins=10, log=True)
        plt.title('Origin - Destination pairs')
        plt.xlabel('Number of searches')
        plt.ylabel('Number of station pairs')
        plt.savefig('output/links.png')

    # give top (or bottom) unique values (by count)
    counter = filter_position(counter, side=side, quantity=quantity)

    # return json
    if return_json:
        counter = counter.to_json(orient='records')
    return counter

def travel_versus_request_times(df, draw_plot = False, return_json = False):
    """Compare the travel and request times"""

    # obtain request and travel times
    request_times = [datetime.datetime.strptime(row['date_request'] + ':' + row['time_request'],
                                                '%Y-%m-%d:%H:%M')
                     for i, row in df.iterrows()]
    travel_times = [datetime.datetime.strptime(row['date_travel'] + ':' + row['time_travel'],
                                                '%Y-%m-%d:%H:%M')
                     for i, row in df.iterrows()]

    # difference in request and travel times in days (only consider request for future travels
    difference_times = [min((b-a).total_seconds()/86400,30) for a,b in zip(request_times, travel_times) if b>=a]

    # draw plot
    if draw_plot:
        plt.hist(difference_times, bins=100)
        plt.title('Difference in search and travel times (days)')
        plt.xlabel('Difference in search and travel times (days)')
        plt.ylabel('Number of searches')
        plt.savefig('time_diff.png')

    # return json
    if return_json:
        difference_times = difference_times.to_json()
    return difference_times

