from matplotlib import pyplot as plot
from matplotlib import dates
import datetime
import sqlite3
import sys
import numpy


# takes in  a list of tuples and displays the data in a scatter plot
def plot_data(data_points):
    # y-axis values
    sentiments = [tup[0] for tup in data_points]
    # x-axis values
    timestamps = [datetime.datetime.strptime(tup[1], "%Y-%m-%d %H:%M:%S") for tup in data_points]

    fig = plot.figure()
    ax = fig.add_subplot(1, 1, 1)

    plot.plot_date(timestamps, sentiments)
    plot.setp(plot.gca().xaxis.get_majorticklabels(), 'rotation', 90)
# https://stackoverflow.com/questions/25538520/change-tick-frequency-on-x-time-not-number-frequency-in-matplotlib
    ax.xaxis.set_major_locator(dates.HourLocator(interval=6))
    # ax.xaxis.set_major_locator(dates.DayLocator(interval=1))

    # label the axes
    plot.xlabel('Time')
    plot.ylabel('Sentiments')

    # define the limits for the axes
    timedelta = datetime.timedelta(hours=6)  # this should match the locator interval
    plot.xlim(timestamps[0] - timedelta, timestamps[-1] + timedelta)
    plot.ylim(-1.1, 1.1)

    # https://matplotlib.org/1.5.3/users/recipes.html
    box_props = dict(boxstyle='round', facecolor='wheat', alpha=0.5)
    text = get_display_text(data_points)
    ax.text(0.05, 0.95, text, transform=ax.transAxes, fontsize=10,
            verticalalignment='top', bbox=box_props)

    plot.show()


# returns the formatted text for the scatter plot, detailing the subreddits polled and the average sentiment
# for the queried data
def get_display_text(data_points):
    sentiments = [tup[0] for tup in data_points]
    avg = '%.4f' % numpy.average(sentiments)
    # start by displaying the subreddits used
    with open('subreddits.txt', 'r') as file:
        subs = file.read().splitlines()
    text = '|'.join(subs)
    text += '\nAverage Sentiment: {}'.format(avg)
    return text


# takes a list of tuples and prints out the average sentiment for a given time frame
def print_data(data_points):
    sentiments = [tup[0] for tup in data_points]
    avg = '%.4f' % numpy.average(sentiments)
    start_date = data_points[0][1]
    end_date = data_points[-1][1]
    print("The average sentiment from [{start}, {end}] is {avg}".format(start=start_date, end=end_date, avg=avg))


# takes args that are expected to be start and end datetimes
# validates the strings given. If a string is invalid, this method will print out the
# offending string and exit.
# TODO: finish this
def get_query_restrictions(query_args):
    # because of the if statement that precedes the call to this function,
    # len(query_args) >= 1 will always be true
    if len(query_args) > 1:  # assumes that start is the first date and end is the second
        # ignores args other than arg[0] and arg[1]
        start_str = query_args[0]
        end_str = query_args[1]
        return None, None
    else:
        # if there's only 1 (correctly formatted) argument, then the other return value in the tuple
        # should just be None
        return None, None


# takes a string and validates whether or not it is formatted correctly.
# example: "2017-12-31"
# rather than try to accept multiple types of input, only match "yyyy-mm-dd hh:mm:ss"
# TODO: finish this
def validate_date_string(date_str):
    return True


# takes a string and validates whether or not it is formatted correctly.
# example: "2017-12-31 23:59:59"
def validate_datetime_string(datetime_str):
    return True


# TODO: finish this
def get_query_string(**query_args):
    start_time = query_args['start']
    end_time = query_args['end']
    # need to know whether or not to include query constraints, i.e.:
    # date <= start_time AND date >= end_time
    # for the purposes of this application, assume <= and >= rather than
    # allowing for more options than that.
    query_str = 'SELECT sentiment, submission_date FROM sodium ORDER BY date(submission_date) ASC'
    if start_time is not None:
        query_str += ' WHERE submission_date <= {}'.format(start_time)
        if end_time is not None:  # if both are not None
            query_str += ' AND submission_date >= {}'.format(end_time)
    elif end_time is not None:
        query_str += ' WHERE submission_date >= {}'.format(end_time)
        # only end_time given
    # if both are None, no modifications are made to the query string
    return query_str


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Needs at least 1 argument: 'plot' or 'print'")
        exit(1)
    else:
        # make all arguments lower case, and ignore the first argument, the name of the script
        arguments = [s.lower() for s in sys.argv[1:]]
        if arguments[0] != 'plot' and arguments[0] != 'print':
            print("Unrecognized argument: {}\nExpects 'plot' or 'print'".format(arguments[0]))
            exit(1)

        # define optional start / end dates and times for query
        # in order for options to be defined, there must be more args
        # arguments variable already excludes the script name, so we want
        # 3 args total: type, start, end
        # examples
        # python visualize.py plot -startDateTime 2017-12-30 01:00:00 -endDateTime 2017-12-31 23:59:59
        # python visualize.py print -startDate 2017-12-30 -endDate 2017-12-31
        # aliases:
        # startDateTime = st
        # startDate = sd
        # endDateTime = et
        # endDate = ed
        # TODO: think of a better way to implement this maybe?
        start, end = (None, None)
        if len(arguments) > 1:  # if there are other arguments besides 'plot' or 'print'
            start, end = get_query_restrictions(arguments[1:])  # returns a tuple of datetimes as strings

        # reads from the database and returns a list of tuples. (sentiment, timestamp)
        values = []
        # establish database connection to read all of the data
        db = sqlite3.connect('sodium.db')
        db.row_factory = sqlite3.Row
        query = get_query_string(start=start, end=end)
        for row in db.execute(query):
            values.append((row[0], row[1]))
        db.close()

        if arguments[0] == 'plot':
            # TODO: add functionality for customizing the plot
            # i.e.:
            # allow users to specify the range of dates to plot
            # allow users to specify the interval for x-axis ticks, like hourly, daily, etc.
            plot_data(values)
        else:  # if it's not 'plot', then it must be 'print'
            # should simply print out the overall average sentiment over the date range where data was collected
            print_data(values)
