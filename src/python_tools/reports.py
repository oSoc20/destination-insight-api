import pandas as pd
import datetime
from collections import Counter
import matplotlib.pyplot as plt
import json

from misc import filter_position
from misc import query_data

def count_repetitions(column,
                      start=None,
                      end=None,
                      date_type=None,
                      df=None,
                      side=None,
                      quantity=None,
                      draw_plot=False,
                      return_json=False):
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
    counter = filter_position(counter, side=side, quantity=quantity)

    # return in json format
    if return_json:
        counter = counter.to_json(orient='records')

    return counter


def count_links(start=None,
                end=None,
                date_type=None,
                df=None,
                side=None,
                quantity=None,
                draw_plot=False,
                return_json=False):
    """Count the repetitions for each link between stations"""

    # query data if no dataframe is provided
    if not df:
        df = query_data(['origin', 'destination'], start, end, date_type)

    # count repetitions of unique departure-destination pairs
    destination_pairs = [set([row[1]['origin'], row[1]['destination']]) for row in df.iterrows()]
    counter = Counter(frozenset(s) for s in destination_pairs)
    counter = pd.DataFrame.from_dict(counter, orient='index').reset_index()

    # arrange table format
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


def travel_versus_request_times_days(start,
                                     end,
                                     date_type,
                                     draw_plot=False,
                                     return_json=False):
    """Compare the travel and request times in days"""

    # query data
    df = query_data(['date_request', 'date_travel', 'time_request', 'time_travel'], start, end, date_type)

    # obtain request and travel times
    request_times = [datetime.datetime.combine(row['date_request'], datetime.datetime.min.time()) +
                     row['time_request'] for idx, row in df.iterrows()]
    travel_times = [datetime.datetime.combine(row['date_travel'], datetime.datetime.min.time()) +
                    row['time_travel'] for idx, row in df.iterrows()]

    # difference in request and travel times in days (only consider request for future travels
    difference_times = [min((b - a).total_seconds() / 86400, 30) for a, b in zip(request_times, travel_times) if b >= a]

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


def searches_by_time(start,
                     end,
                     date_type,
                     aggregation):
    """Count the total number of searches by days, months, or years"""

    # query data
    time_var = 'date_' + date_type
    df = query_data([time_var], start, end, date_type)

    # aggregate data
    df['time_interval'] = pd.to_datetime(df[time_var]).dt.to_period(aggregation)
    df = df.groupby(df['time_interval'])
    results = df['time_interval'].agg('count', ).to_frame()

    # arrange table format
    results = pd.DataFrame({'Date': results.index.to_series().astype(str), 'Counts': results['time_interval']})

    # convert results to json
    results = results.to_json(orient='records')

    return results


def searches_by_hour(start,
                     end,
                     time_type):
    """Count total number of searches by hour of the day and day of the week (for radial plot)"""

    # query data
    date_var = 'date_' + time_type
    time_var = 'time_' + time_type
    df = query_data([time_var, date_var], start, end, time_type)

    # extract day of week and hour
    df['hour'] = df[time_var].dt.components['hours']
    df['day'] = pd.to_datetime(df[date_var]).dt.dayofweek

    # aggregate data
    df = df.groupby(['day', 'hour'])
    results = df[time_var].agg('count', ).to_frame()

    # convert results to json
    results = results.to_json()

    return results


def missing_days(start,
                 end):
    """List days for which there is no data in the database"""

    # query data
    alternative_query = 'select distinct date_request from searches'
    df = query_data([''], start, end, 'travel', alternative_query)
    df = set(df[''])

    # get list of all days between start and and date
    start = datetime.datetime.strptime(start, "%Y-%m-%d").date()
    end = datetime.datetime.strptime(end, "%Y-%m-%d").date()
    all_days = set([(start + datetime.timedelta(days=x)) for x in range((end - start).days + 1)])

    # find missing days
    results = list(all_days.difference(df))
    results.sort()
    results = [item.strftime('%Y-%m-%d') for item in results]

    # convert results to json
    results = json.dumps(results)

    return results