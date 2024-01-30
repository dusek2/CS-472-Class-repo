import matplotlib.pyplot as plt
import csv
import datetime
import random

# read data from csv
def read_data(csv_file):
    data = []

    with open(csv_file, mode='r', encoding='utf-8') as file:
        reader = csv.reader(file)
        next(reader)  # Skip header
        oldestDate = datetime.datetime.now(datetime.timezone.utc)
        # go row by row and find repo creation date
        for row in reader:
            filename, author, date_str = row
            date = datetime.datetime.fromisoformat(date_str)
            if date < oldestDate:
                oldestDate = date
                print(oldestDate)
        # reset reader to line 1
        file.seek(0)
        next(reader)  # Skip header
        # go row by row and calculate weeks since start of repo
        for row in reader:
            filename, author, date_str = row
            #print(date_str)
            date = datetime.datetime.fromisoformat(date_str)
            #print(date)
            week = (date - oldestDate).days / 7
            print(week)
            #print(week)
            data.append((filename, author, week))
    return data

# plot data with random colours
def plot_scatter(data):
    colors = {}
    # assign colours randomly
    for _, author, _ in data:
        if author not in colors:
            colors[author] = (random.random(), random.random(), random.random())
    # assign numbers to files
    i = 1
    fileNumbers = {}
    for fileName, _, _ in data:
        if fileName not in fileNumbers:
            fileNumbers[fileName] = i
            i += 1
    # plot data
    for filename, author, week in data:
        plt.scatter(fileNumbers[filename], week, color=colors[author], label=author)
    # add labels
    plt.xlabel('File number')
    plt.ylabel('Week')
    plt.title('File Touches per Week by Author')
    plt.show()

# read data and plot
csv_file = 'data/file_dates_rootbeer.csv'
data = read_data(csv_file)
plot_scatter(data)
