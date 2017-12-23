from matplotlib import pyplot as plot
from matplotlib import dates
import datetime
import sqlite3

# establish database connection to read all of the data
db = sqlite3.connect('sodium.db')
db.row_factory = sqlite3.Row

# reads from the database and returns a list of tuples. (sentiment, timestamp)
values = []
for row in db.execute('SELECT sentiment, submission_date FROM sodium ORDER BY date(submission_date) ASC'):
    values.append((row[0], row[1]))
db.close()

# y-axis values
sentiments = [tup[0] for tup in values]
# x-axis values
timestamps = [datetime.datetime.strptime(tup[1], "%Y-%m-%d %H:%M:%S") for tup in values]

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
timedelta = datetime.timedelta(hours=6)
plot.xlim(timestamps[0] - timedelta, timestamps[-1] + timedelta)
plot.ylim(-1.1, 1.1)

plot.show()
