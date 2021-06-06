import datetime

def current_time():
    return f"( {datetime.datetime.now().time()} )    "

def current_percent(bought,current):
    change = 100 * (float(current) - float(bought)) / float(bought)
    return "{:.2f}".format(change)