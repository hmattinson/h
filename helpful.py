import re
import pandas as pd
import datetime

# Pretty
# **********************************************

def log_progress(sequence, every=None, size=None, name='Items'):
    from ipywidgets import IntProgress, HTML, VBox
    from IPython.display import display

    is_iterator = False
    if size is None:
        try:
            size = len(sequence)
        except TypeError:
            is_iterator = True
    if size is not None:
        if every is None:
            if size <= 200:
                every = 1
            else:
                every = int(size / 200)     # every 0.5%
    else:
        assert every is not None, 'sequence is iterator, set every'

    if is_iterator:
        progress = IntProgress(min=0, max=1, value=1)
        progress.bar_style = 'info'
    else:
        progress = IntProgress(min=0, max=size, value=0)
    label = HTML()
    box = VBox(children=[label, progress])
    display(box)

    index = 0
    try:
        for index, record in enumerate(sequence, 1):
            if index == 1 or index % every == 0:
                if is_iterator:
                    label.value = '{name}: {index} / ?'.format(
                        name=name,
                        index=index
                    )
                else:
                    progress.value = index-1 # So that the bar isn't full until done
                    label.value = u'{name}: {index} / {size}'.format(
                        name=name,
                        index=index,
                        size=size
                    )
            yield record
    except:
        progress.bar_style = 'danger'
        raise
    else:
        progress.bar_style = 'success'
        progress.value = index
        label.value = "{name}: {index}".format(
            name=name,
            index=str(index or '?')
        )
        
class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    Blink='\033[5m'
    Inverted='\033[7m'
    Hidden='\033[8m'

    Black='\033[30m'
    Red='\033[31m'
    Green='\033[32m'
    Yellow='\033[33m'
    Blue='\033[34m'
    Purple='\033[35m'
    Cyan='\033[36m'
    LightGray='\033[37m'
    DarkGray='\033[30m'
    LightRed='\033[31m'
    LightGreen='\033[32m'
    LightYellow='\033[93m'
    LightBlue='\033[34m'
    LightPurple='\033[35m'
    LightCyan='\033[36m'
    White='\033[97m'
    
def bcolors_print(msg, bcolor):
    print(bcolor + msg + bcolors.ENDC)

# Maths
# **********************************************
        
def safe_divide(a,b):
    if b==0:
        return 0
    else:
        return a/b
    
# Dates + Times
# **********************************************
    
# generates a datetime with the given time
def fake_date(time):
    return datetime.datetime.combine(datetime.date(2000,1,1),time)

# finds the difference between 2 times
def datetime_time_diff(a,b):
    return fake_date(a) - fake_date(b)

# create pd.DateOffset from a string e.g. '3d9h' 
def parse_time_offset(time_str):
    regex = re.compile(r'((?P<years>\d+?)y)?((?P<months>\d+?)M)?((?P<weeks>\d+?)w)?((?P<days>\d+?)d)?((?P<hours>\d+?)h)?((?P<minutes>\d+?)m)?((?P<seconds>\d+?)s)?')
    parts = regex.match(time_str)
    if not parts:
        return
    parts = parts.groupdict()
    time_params = {}
    for (name, param) in parts.items():
        if param:
            time_params[name] = int(param)
    return pd.DateOffset(**time_params)

# checks if 2 isoformat timestamps are the same day
def different_days(s1,s2):
    return s1[:10]!=s2[:10]
    #return pd.Timestamp(s1).date() != pd.Timestamp(s2).date()

# DataFrames
# ************************************************

def expanding_daily_max(df,col_to_max):
    x = list(ticks.groupby(df['ts'].dt.date)[col_to_max])[0][1].expanding().max()
    for day in list(df.groupby(ticks['ts'].dt.date)[col_to_max])[1:]:
        x = x.append(day[1].expanding().max())
    return x

def drop_columns(df, colummns):
    return df.drop(columns, axis=1)
