import pandas as pd
from collections import Counter
import numpy as np
import matplotlib.pyplot as plt
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
    theta = np.linspace(0, 2*np.pi, num_vars, endpoint=False)

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

def filter_position(df, side = None, quantity = None):
    'Filter observations by either top or bottom'
    if side == 'top':
        df = df[:quantity]
    elif side == 'bottom':
        df = df[-quantity:]
    return df

def count_repetitions(df, column, side = None, quantity = None, draw_plot = False, return_json = False):
    'Count the repetitions for each unique value in the specific column'
    counter = df[column].value_counts().reset_index()
    counter.columns = [column.title(), 'Counts']
    counter.hist(column='Counts', bins = 10, log= True)
    if draw_plot:
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
    counter.hist(column='Counts', bins=10, log=True)
    if draw_plot:
        plt.title('Origin - Destination pairs')
        plt.xlabel('Number of searches')
        plt.ylabel('Number of station pairs')
        plt.savefig('output/links.png')
    counter = filter_position(counter, side=side, quantity=quantity)
    if return_json:
        counter = counter.to_json()
    return counter
