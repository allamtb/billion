import datetime


def getwjj():

    current_time = datetime.datetime.now()
    str_date_time = current_time.strftime("%Y%m%d%H%M%S%f")
    return str_date_time

