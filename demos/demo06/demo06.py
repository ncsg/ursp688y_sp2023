import requests
from datetime import datetime
import pytz
import os
import time
import logging
import math

import matplotlib.pyplot as plt
import numpy as np

def power_function_plot(function, x_label, y_label, title, here=2):
    x = np.linspace(0, 10, 1000)
    y = function(x)
    plt.plot(x, y, color='red')
    plt.scatter(here, function(here), color='blue', zorder=2)
    plt.text(
        x=here + 0.2, 
        y=function(here) - 0.1, 
        s='We are here', 
        horizontalalignment='left', 
        color='blue')
    plt.title(title)
    plt.xlabel(x_label)
    plt.ylabel(y_label)
    plt.tick_params(
        left = False, 
        right = False , 
        labelleft = False , 
        labelbottom = False, 
        bottom = False)
    plt.gca().spines[['top', 'right']].set_visible(False)
    plt.show() 

def plot_capability_for_syntax(steepness=2, here=2):
    power_function_plot(
        function=lambda x: x ** steepness,
        x_label='Syntax Knowledge', 
        y_label='Capability', 
        title='Python Learning Curve', 
    )

def plot_syntax_for_capability(steepness=2, here=2):
    power_function_plot(
        function=lambda x: x ** (1/steepness),
        x_label='Capability', 
        y_label='Syntax Knowledge', 
        title='Python Learning Curve', 
        here=here,
    )

def get(url):
    """Retrieves json-formatted data from a url

    returns: nested lists and dictionaries
    """
    data = requests.get(url).json()
    return data

def count_keys(data):
    """Counts the instances of keys in dictionaries stored in a list
    
    data: list of dictionaries

    returns: dictionary of unique keys with counts as values
    """
    keys = {}
    for record in data:
        for k, v in record.items():
            if k in keys:
                keys[k] += 1
            else:
                keys[k] = 1
    return keys