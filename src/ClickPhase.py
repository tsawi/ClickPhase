import pandas as pd
from bokeh.plotting import figure
from bokeh.models import ColumnDataSource
from bokeh.layouts import column
from bokeh.io import curdoc
from bokeh.events import Tap
import csv
from datetime import datetime
import os
from pathlib import Path

# Function to append click time to CSV file
def append_click_time_to_csv(x, waveform_filename):

    file_path = f"../results/picks/PB.B918/{waveform_filename.split('/')[-1]}"

    with open(file_path, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([waveform_filename, x])


# Function to load waveform data from CSV file
def load_waveform_from_input(input_filename):
    input_file = pd.read_csv(input_filename,header=None)
    waveform_filename = input_file.iloc[0, 0]  # First element of the first row

    df = pd.read_csv(waveform_filename)
    x = list(range(len(df))) #time; 1 Hz sampling, so this is ok
    y =  [x[0] for x in df.values] # amplitude
    return x, y, waveform_filename

# Load waveform data from CSV file
input_filename = 'input.csv'
x, y, waveform_filename = load_waveform_from_input(input_filename)

# Sample rate (assuming regular time intervals in the CSV file)
sample_rate = 1 / (x[1] - x[0])

# Create a data source
source = ColumnDataSource(data=dict(x=x, y=y))

# Create the plot
p = figure(title="Pick P-wave arrival time:", width=800, height=400, x_axis_label='Time (s)', y_axis_label='Amplitude')
p.line('x', 'y', source=source, line_width=2)


# Python callback to handle tap event
def handle_tap(event, waveform_filename=waveform_filename):
    print("Tapped at:", event.x)
    append_click_time_to_csv(event.x, waveform_filename)

# Register the Python callback with Bokeh's on_event using a lambda function
p.on_event(Tap, lambda event: handle_tap(event))


# Add the plot to the current document
curdoc().add_root(column(p))
