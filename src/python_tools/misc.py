import numpy as np
from urllib.parse import unquote
import mysql.connector
import pandas as pd
import unidecode

from matplotlib.patches import Circle, RegularPolygon
from matplotlib.path import Path
from matplotlib.projections.polar import PolarAxes
from matplotlib.projections import register_projection
from matplotlib.spines import Spine
from matplotlib.transforms import Affine2D


def radar_factory(num_vars, frame='circle'):
    """Create a radar chart with `num_vars` axes.

    This function creates a RadarAxes projection and registers it.

    Parameters
    ----------
    num_vars : int
        Number of variables for radar chart.
    frame : {'circle' | 'polygon'}
        Shape of frame surrounding axes.

    """
    # calculate evenly-spaced axis angles
    theta = np.linspace(0, 2 * np.pi, num_vars, endpoint=False)

    class RadarAxes(PolarAxes):

        name = 'radar'
        # use 1 line segment to connect specified points
        RESOLUTION = 1

        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            # rotate plot such that the first axis is at the top
            self.set_theta_zero_location('N')

        def fill(self, *args, closed=True, **kwargs):
            """Override fill so that line is closed by default"""
            return super().fill(closed=closed, *args, **kwargs)

        def plot(self, *args, **kwargs):
            """Override plot so that line is closed by default"""
            lines = super().plot(*args, **kwargs)
            for line in lines:
                self._close_line(line)

        def _close_line(self, line):
            x, y = line.get_data()
            # FIXME: markers at x[0], y[0] get doubled-up
            if x[0] != x[-1]:
                x = np.concatenate((x, [x[0]]))
                y = np.concatenate((y, [y[0]]))
                line.set_data(x, y)

        def set_varlabels(self, labels):
            self.set_thetagrids(np.degrees(theta), labels)

        def _gen_axes_patch(self):
            # The Axes patch must be centered at (0.5, 0.5) and of radius 0.5
            # in axes coordinates.
            if frame == 'circle':
                return Circle((0.5, 0.5), 0.5)
            elif frame == 'polygon':
                return RegularPolygon((0.5, 0.5), num_vars,
                                      radius=.5, edgecolor="k")
            else:
                raise ValueError("unknown value for 'frame': %s" % frame)

        def _gen_axes_spines(self):
            if frame == 'circle':
                return super()._gen_axes_spines()
            elif frame == 'polygon':
                # spine_type must be 'left'/'right'/'top'/'bottom'/'circle'.
                spine = Spine(axes=self,
                              spine_type='circle',
                              path=Path.unit_regular_polygon(num_vars))
                # unit_regular_polygon gives a polygon of radius 1 centered at
                # (0, 0) but we want a polygon of radius 0.5 centered at (0.5,
                # 0.5) in axes coordinates.
                spine.set_transform(Affine2D().scale(.5).translate(.5, .5)
                                    + self.transAxes)
                return {'polar': spine}
            else:
                raise ValueError("unknown value for 'frame': %s" % frame)

    register_projection(RadarAxes)
    return theta


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
                for alt in name_alts:
                    try:
                        # check if the station name exists (four languages and extra column)
                        idx = pd.Index(stations[alt]).get_loc(entry_search)
                        entry = stations['name-original-cap'][idx]# + ' (Station)'
                        break
                    except:
                        pass
                return entry

def obtain_time(time):
    """If necessary decode time field"""
    if '%' in time:
        return unquote(time)
    else:
        return time


def query_data(vars, start, end, date_type):
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
    query = 'select ' + vars_format + ' from searches where date_' + date_type + ' between CAST("' + start + '" as DATE) and CAST("' + end + '" as DATE)'

    # query data
    curs.execute(query)

    # turn results to dataframe
    data = pd.DataFrame(curs.fetchall())
    data.columns = vars
    return data