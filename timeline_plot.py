"""
CSCI 141
Author: Scott Bullock
Project
This program using index_tools.py, numpy, and matplotlib
to help program run as desired. This program plots a line graph
and box and whisker plot of regions inputted by the user.
"""
import numpy as np
import numpy.ma as ma
import matplotlib.ticker as mticker
import matplotlib.pyplot as plt
import datetime as dt
import matplotlib.dates as mdates
import copy
import index_tools

def build_plottable_array(xyears, regiondata):
    """
    Creates an array that can be plotted using the matplotlib module.
    Precondition: regiondata must consist of annualHPI objects
    :param xyears: a list of integer year values
    :param regiondata: a list of AnnualHPI objects.
    :return: An array that can be plotted with using matplotlib
    and the array will have masked values if the info does not exist
    """
    unmasked = []
    mask = []
    for year in xyears:
        year_index = None
        for data in regiondata:
            if int(year) == int(data.year):
                year_index = float(data.index)
        unmasked.append(year_index)
    for element in unmasked:
        if element is None:
            mask.append(1)
        else:
            mask.append(0)
    yvalues = ma.array(unmasked, mask=mask)
    return yvalues

def filter_years(data, year1, year2):
    """
    Gets a dictionary of annual objects that are between year1 and year2
    Precondition: data ust consist of annualHPI objects, and year1 must come
    before year2
    :param data: a dictionary mapping from regions to lists of AnnualHPI objects
    :param year1: the starting year to filter data
    :param year2: the ending year to filter data
    :return: A dictionary mapping regions to list of sorted HPI values that are
    within the year0 to year1 inclusive range.
    """
    filtered_data = {}
    for region in data.keys():
        for element in data[region]:
            if int(element.year) >= year1 and int(element.year) <= year2:
                if region in filtered_data:
                    filtered_data[region].append(element)
                else:
                    filtered_data[region]=[element]
    return filtered_data

def plot_HPI(data, regionlist):
    """
    Displays a lines graph that includes all regions in
    regionlist, the y-axis is the house price index and the x-axis
    are the regions
    Precondition: Data includes only annualHPI objects and elements
    in regionlist are keys in the data dictionary
    :param data: a dictionary mapping a state or zip code to a list
    of AnnualHPI objects
    :param regionlist: a list of key values whose type is string
    """
    for region in regionlist:
        min_year = 2022
        max_year = 0
        xyears = []
        length = len(data[region])
        if int(data[region][0].year) < int(min_year):
            min_year = int(data[region][0].year)
        if int(data[region][length-1].year) > int(max_year):
            max_year = int(data[region][length-1].year)
        for i in range(min_year, max_year+1):
            xyears.append(i)
        data_line = build_plottable_array(xyears, data[region])
        plt.plot(xyears, data_line, marker="*", label=region, markeredgecolor="black")
    plt.legend(loc="upper left")
    plt.title("Home Index Prices from "+str(xyears[0]) +
              "-"+str(xyears[len(xyears)-1]))
    print("CLose display window to continue")
    plt.show()

def plot_whiskers(data, regionlist):
    """
    Displays a box and whisker plot that includes all regions in
    regionlist, the y-axis is the house price index and the x-axis
    are the regions
    Precondition: Data includes only annualHPI objects and elements
    in regionlist are keys in the data dictionary
    :param data: a dictionary mapping a state or zip code to a list
    of AnnualHPI objects
    :param regionlist: a list of key values whose type is string
    """
    all_data = []
    x_axis = []
    for region in regionlist:
        min_year = 2022
        max_year = 0
        xyears = []
        length = len(data[region])
        if int(data[region][0].year) < int(min_year):
            min_year = int(data[region][0].year)
        if int(data[region][length-1].year) > int(max_year):
            max_year = int(data[region][length-1].year)
        for i in range(min_year, max_year+1):
            xyears.append(i)
        data_line = build_plottable_array(xyears, data[region])
        x_axis.append(str(region))
        all_real_values = data_line[data_line.mask == False]
        all_data.append(all_real_values)
    custom_mean = dict(marker='D', markeredgecolor='black', markerfacecolor='red')
    custom_median = dict(color='red')
    custom_whisker = dict(linestyle='--', color='blue')
    custom_box = dict(color='blue')
    plt.boxplot(all_data, labels=x_axis, showmeans=True, meanprops=custom_mean,
                medianprops=custom_median, whiskerprops=custom_whisker, boxprops=custom_box)
    plt.title("Home Index Price Comparison. Median is a line. Mean is a diamond")
    print("CLose display window to continue")
    plt.show()

def main():
    """
    Asks the user for a file and depending on the file type it will
    read the file accordingly. The program also prompts the user to
    enter the starting and ending years to plot. Then the programs
    makes the user enter regions until they press ENTER. Lastly, the
    data will get filtered, and plotted on a line graph and box and
    whisker plot.
    """
    file = input("Enter region-based house price index filename: ")
    file = "data/" + file
    year1 = int(input("Enter start year of the range to plot: "))
    year2 = int(input("Enter end year of the range to plot: "))
    if file == "data/HPI_AT_ZIP5.txt":
        regions = []
        data = index_tools.read_zip_house_price_data(file)
        region = "placeholder"
        while region != "":
            region = input("Enter a region (Hit ENTER to stop): ")
            regions.append(region)
        regions.remove("")
        filter_data = filter_years(data, year1, year2)
        plot_HPI(filter_data, regions)
        plot_whiskers(filter_data, regions)
    else:
        regions = []
        data_quarter = index_tools.read_state_house_price_data(file)
        data_annual = index_tools.annualize(data_quarter)
        region = "placeholder"
        while region != "":
            region = input("Enter a region (Hit ENTER to stop): ")
            regions.append(region)
        regions.remove("")
        for region in regions:
            print('=' * 72)
            index_tools.print_range(data_quarter, region)
            index_tools.print_range(data_annual, region)
        filter_data = filter_years(data_annual, year1, year2)
        plot_HPI(filter_data, regions)
        plot_whiskers(filter_data, regions)

if __name__ == "__main__":
    main()
