'''
This script is adpated from the jupyter notebook with the same name under the same directory with function encapsulation.
Author: Ao Chen, on a train.
'''

from re import search
import pandas as pd
import olca
import uuid
import math
from datetime import datetime

from matplotlib import pyplot as plt
import matplotlib.mlab as mlab
from matplotlib import rcParams
import matplotlib.patches as mpatches
import seaborn as sns

client = olca.Client(8080)

def process_search(client, key):
    # Get all process dataset in database
    process_descriptor = client.get_descriptors(olca.Process)
    process_list = []
    id_list = []
    location_list = []

    for process in process_descriptor:
        process_list.append(process.name)
        id_list.append(process.id)
        location_list.append(process.location)
    processes_df = pd.DataFrame(list(zip(process_list,
                                    id_list, location_list)),
                                columns=['name', 'id', 'location'])

    # Search specific process databases with key word(s)
    # Note that the search is blankspace-sensitive
    search_process_df = processes_df[processes_df['name'].str.contains(key)] # TODO: change keywords
    search_process_df.reset_index(drop=True, inplace=True)

    return search_process_df

