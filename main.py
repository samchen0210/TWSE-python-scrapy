#Package import
import os
import glob
import time
import datetime
import requests
import pandas as pd
from io import StringIO
from datetime import date

# Chart drawing
import plotly as py
import plotly.io as pio
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from plotly.offline import download_plotlyjs, init_notebook_mode, plot, iplot

#create new folder
def createFolder(directory): #directory means the file's name
    try:
        if not os.path.exists(directory):
            os.makedirs(directory)
    except OSError:
        print ('Error: Creating directory. ' + directory)
# Example
#createFolder('./5501/')
# Creates a folder in the current directory called data


