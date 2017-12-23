from matplotlib import pyplot as plot
from matplotlib import dates
import datetime
import sqlite3
import sys


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

    # TODO: add text box that displays the overall average sentiment

    plot.show()


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

        # establish database connection to read all of the data
        db = sqlite3.connect('sodium.db')
        db.row_factory = sqlite3.Row

        # reads from the database and returns a list of tuples. (sentiment, timestamp)
        values = []
        for row in db.execute('SELECT sentiment, submission_date FROM sodium ORDER BY date(submission_date) ASC'):
            values.append((row[0], row[1]))
        db.close()

        if arguments[0] == 'plot':
            # TODO: add functionality for customizing the plot
            # i.e.:
            # allow users to specify the range of dates to plot
            # allow users to specify the interval for x-axis ticks, like hourly, daily, etc.
            plot_data(values)
        else:  # if it's not 'plot', then it must be 'print'
            # TODO: add print_data(values) function
            # should simply print out the overall average sentiment over the date range where data was collected
            pass
