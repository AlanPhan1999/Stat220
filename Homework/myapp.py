from bokeh.palettes import DarkText, Vibrant3 as colors
import numpy as np
import pandas as pd
import copy
import bokeh.layouts
from bokeh.models import ColumnDataSource, CustomJS, CDSView, GroupFilter
from bokeh.models.widgets import Slider
from bokeh.plotting import figure, curdoc
bokeh.io.output_notebook()

final_aggregated = pd.read_csv('../Data/aggregated.csv')
source = ColumnDataSource(final_aggregated)
l = final_aggregated['year_group'].unique()

p = figure(y_range=l, title="Cumulative population by threshold grouped by year group", height=400, width=600, x_axis_label="cumulative population", tools="")
p.hbar(y='year_group', right='cumulative_male_population', color='blue', source=source, legend_label='Male')
p.hbar(y='year_group', right='cumulative_female_population', color='red', source=source, legend_label='Female')

start = final_aggregated["threshold"].min()
end = final_aggregated["threshold"].max()

slider = bokeh.models.Slider(start = start, end = end, step = .2, value = start)

ts = final_aggregated['threshold'].unique()
def callback(attr, old, new):
    idx = np.absolute(ts - slider.value).argmin()
    value = ts[idx]

    new_ts = final_aggregated['threshold'] == value
    final_ts = final_aggregated[new_ts]
    new_source = ColumnDataSource(final_ts)
    source.data = dict(new_source.data)

slider.on_change("value", callback)

layout = bokeh.layouts.column(slider, p)
curdoc().add_root(layout)