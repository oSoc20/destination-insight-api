from urllib.parse import unquote
import mysql.connector
import pandas as pd
import unidecode

def filter_position(df, side=None, quantity=None):
    """Filter observations by either top or bottom"""
    if side == 'top':
        df = df[:quantity]
    elif side == 'bottom':
        df = df[-quantity:]
    return df

def obtain_city(url, stations):
    """Decode city field"""

    # columns with alternative names
    name_alts = ['name', 'alternative-fr', 'alternative-nl', 'alternative-de', 'alternative-en', 'alternative-wp']

    # decode url
    url = unquote(url)
    url_split = url.split('@')

    # find text that represents the location
    for item in url_split:
        if 'O=' in item:
            entry = item[2:]

            # check if it is a bus station
            bus_station = any([bus_company in entry for bus_company in ['[TEC]', '[De Lijn]', '[STIB]', '[MIVB]']])
            if bus_station:
                return 'Bus Station'

            # check if it is in the netherlands
            elif '(nl)' in entry.lower():
                return 'Netherlands'

            else:
                entry_search = unidecode.unidecode(entry.lower())

                # look for location in the table with the station names
                for alt in name_alts:

                    # if the station is found, change name to default one to standardize all the searches
                    try:
                        idx = pd.Index(stations[alt]).get_loc(entry_search)
                        entry = stations['name-original-cap'][idx]
                        break
                    except:
                        pass

                # if no station is found, return the original location as is
                return entry

def obtain_time(time):
    """If necessary decode time field"""
    if '%' in time:
        return unquote(time)
    else:
        return time

def query_data(vars, start, end, date_type, alternative_query = None):
    """Query searches table filtering between the dates 'start' and 'end'.
    The 'date_type' can be either 'request' or 'travel' depending on what you want to filter by.
    'vars' is a list of strings with the variable names that you want to extract."""

    # connect to database
    db = mysql.connector.connect(
        host="db4free.net",
        user="nmbstest",
        password="nmbsRoutePlannerDataAnalysis"
    )
    curs = db.cursor()
    curs.execute("USE routeplannerdata")

    # format variable names
    vars_format = ', '.join(vars)

    if alternative_query is None:
        query = 'select ' + vars_format + ' from searches where date_' + date_type + ' between CAST("' + start + '" as DATE) and CAST("' + end + '" as DATE)'
    else:
        query = alternative_query

    # query data
    curs.execute(query)

    # turn results to dataframe
    data = pd.DataFrame(curs.fetchall())
    data.columns = vars

    # close connection to database
    curs.close()
    db.close()

    return data
