import pandas as pd
import datetime
from collections import Counter
import matplotlib.pyplot as plt

from misc import filter_position

def count_repetitions(df, column, side = None, quantity = None, draw_plot = False, return_json = False):
    'Count the repetitions for each unique value in the specific column'
    counter = df[column].value_counts().reset_index()
    counter.columns = [column.title(), 'Counts']
    if draw_plot:
        counter.hist(column='Counts', bins=10, log=True)
        plt.title(column.title() + ' Stations')
        plt.xlabel('Number of searches')
        plt.ylabel('Number of stations')
        plt.savefig('output/' + column + '.png')
    counter = filter_position(counter, side = side, quantity = quantity)
    if return_json:
        counter = counter.to_json()
    return counter

def count_links(df, side = None, quantity = None, draw_plot = False, return_json = False):
    'Count the repetitions for each link between stations'
    destination_pairs = [set([row[1]['origin'], row[1]['destination']]) for row in df.iterrows()]
    counter = Counter(frozenset(s) for s in destination_pairs)
    counter = pd.DataFrame.from_dict(counter, orient='index').reset_index()
    counter.columns = ['Destination pairs', 'Counts']
    counter['Destination pairs'] = [' to/from '.join(list(item)) for item in counter['Destination pairs']]
    counter = counter.sort_values(by=['Counts'], ascending=False)
    if draw_plot:
        counter.hist(column='Counts', bins=10, log=True)
        plt.title('Origin - Destination pairs')
        plt.xlabel('Number of searches')
        plt.ylabel('Number of station pairs')
        plt.savefig('output/links.png')
    counter = filter_position(counter, side=side, quantity=quantity)
    if return_json:
        counter = counter.to_json()
    return counter

def travel_versus_request_times(df, draw_plot = False, return_json = False):
    'Compare the travel and request times'
    request_times = [datetime.datetime.strptime(row['date_request'] + ':' + row['time_request'],
                                                '%Y-%m-%d:%H:%M')
                     for i, row in df.iterrows()]
    travel_times = [datetime.datetime.strptime(row['date_travel'] + ':' + row['time_travel'],
                                                '%Y-%m-%d:%H:%M')
                     for i, row in df.iterrows()]
    difference_times = [min((b-a).total_seconds()/86400,30) for a,b in zip(request_times, travel_times) if b>=a]
    if draw_plot:
        plt.hist(difference_times, bins=100)
        plt.title('Difference in search and travel times (days)')
        plt.xlabel('Difference in search and travel times (days)')
        plt.ylabel('Number of searches')
        plt.savefig('time_diff.png')
    if return_json:
        difference_times = difference_times.to_json()
    return difference_times
