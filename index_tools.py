"""
CSCI 141
Author: Scott Bullock
Project
This program includes alot of helper functions that will
be used in other programs. These functions read the file,
get an index range, print a range of values, prints a ranking
of values and annualized a dictionary full of quarterHPI objects
"""
from dataclasses import dataclass
import timeline_plot

@dataclass
class QuarterHPI:
    """
    A dataclass that the year represents the year the data is from
    the quarter is the quarter of the years the data is from. And
    the index is what the house price index was for that year and
    quarter
    """
    year: int
    qtr: int
    index: float

@dataclass
class AnnualHPI:
    """
    A dataclass that the year represents the year the data is from
    and the index is what the house price index was for that year
    """
    year: int
    index: float

def read_state_house_price_data(file):
    """
    Reads the file and reads each lines and converts the line into
    an quarterHPI object and determines if data is unavailable, if so
    the program will say so and if not the quarterHPI object will be
    added to the dictionary.
    Precondition: The file does not contain "ZIP" in the file name and
    that the file exists in the data folder
    :param file: The file that will be read
    :return: A dictionary mapping state abbreviation strings to lists
    of quarterHPI objects
    """
    state_price_data = {}
    with open(file) as fd:
        fd.readline()
        for line in fd:
            info = line.strip("\n").split("\t")
            info_object = QuarterHPI(info[1], info[2], info[3])
            if info_object.index == ".":
                print("data unavailable:")
                print(info[0], info_object.year, info_object.qtr, info_object.index, end="")
                print(" ", info_object.index, "warning: data unavailable in original source")
            else:
                if info[0] in state_price_data:
                    state_price_data[info[0]].append(info_object)
                else:
                    state_price_data[info[0]] = [info_object]
    return state_price_data

def read_zip_house_price_data(zip_file):
    """
    Reads the file and reads each lines and converts the line into
    an annualHPI object and determines if data is unavailable, if so
    the program will add one to the variable "uncounted" and if not
    the annualHPI object will be added to the dictionary and will add
    one to the variable "counted" and once the file is done being read
    it will display how much data there was and was not
    Precondition: The file contains the word "ZIP"
    :param zip_file: The file that will be read
    :return: A dictionary mapping zip codes to lists of annualHPI objects.
    """
    zip_price_data = {}
    uncounted = 0
    counted = 0
    with open(zip_file) as fd:
        fd.readline()
        for line in fd:
            info = line.strip("\n").split("\t")
            info_object = AnnualHPI(info[1], info[3])
            if info[2] == "." and info[3] == "." and info[4] == "." and info[5] == ".":
                uncounted += 1
            else:
                counted += 1
                if info[0] in zip_price_data:
                    zip_price_data[info[0]].append(info_object)
                else:
                    zip_price_data[info[0]] = [info_object]
        print("count: ", counted, "uncounted: ", uncounted)
        return zip_price_data

def index_range(data, region):
    """
    Given a dictionary and a desired region the function will
    get the high and low indexes in dictionary in the region
    Precondition: data is a dictionary mapping of HPI object
    and the region must be present in the form of a key that is
    in the data dictionary
    :param data: A dictionary mapping of HPI objects
    :param region:A region desired that is in the data dictionary
    :return: A tuple of the *HPI objects that are respectively the low
    and high index values of the dataset.
    """
    un_sorted_data = []
    lowest_object = None
    highest_object = None
    for ele in data[region]:
        un_sorted_data.append(float(ele.index))
    sorted_data = sorted(un_sorted_data, key=float)
    lowest_index = (sorted_data[0])
    highest_index = (sorted_data[len(sorted_data)-1])
    for ele in data[region]:
        if float(ele.index) == lowest_index:
            lowest_object = ele
        elif float(ele.index) == highest_index:
            highest_object = ele
        else:
            pass
    return (lowest_object, highest_object)

def print_range(data, region):
    """
    Prints the low and high values (range) of the house price index for
    the given region
    Precondition: a dictionary mapping of HPI object
    and the region must be present in the form of a key that is
    in the data dictionary
    :param data: A dictionary mapping of HPI objects
    :param region: A region desired that is in the data dictionary
    """
    low_and_high = index_range(data, region)
    low = low_and_high[0]
    high = low_and_high[1]
    if isinstance(low, QuarterHPI) is True:
        print("Region: ", region)
        print("Low: year/quarter/index: ", low.year, "/", low.qtr, "/", low.index)
        print("High: year/quarter/index: ", high.year, "/", high.qtr, "/", high.index)
    else:
        print("Region: ", region)
        print("Low: year/index: ", low.year, "/", low.index)
        print("High: year/index: ", high.year, "/", high.index)

def print_ranking(data, heading="Ranking"):
    """
    Prints the top 10 and bottom 10 in terms of house index prices
    Precondition: a sorted list of HPI objects.
    :param data: A dictionary mapping of HPI objects
    """
    counter = 0
    print("The Top 10")
    while counter < 10:
        print(counter+1, ":", data[counter])
        counter += 1
    counter = 10
    print("The Bottom 10")
    while counter > 0:
        print((len(data)-counter)+1, ":", data[len(data)-counter])
        counter -= 1

def annualize(data):
    """
    Given a dictionary of only quarterHPI objects it convert the quarterly
    data into annual data and does this by adding all indexes that year and
    counting how many quarters of data there was that year and dividing both
    of those numbers
    Precondition: The data dictionary only includes QuarterHPI objects
    :param data: A dictionary mapping regions to lists of QuarterHPI objects.
    :return: A dictionary mapping regions to lists of AnnualHPI objects.
    """
    annualize_quarter = {}
    stateYear_allIndexes = {}
    stateYear_indexAverage = {}
    for state in data.keys():
        for element in data[state]:
            state_year = str(state)+str(element.year)
            if state_year in stateYear_allIndexes:
                stateYear_allIndexes[state_year].append(element.index)
            else:
                stateYear_allIndexes[state_year] = [element.index]
    for stateYear in stateYear_allIndexes:
        index_total = 0.0
        counter = 0
        for i in range(len(stateYear_allIndexes[stateYear])):
            index_total += float(stateYear_allIndexes[stateYear][i])
            counter += 1
        index_average = index_total/counter
        stateYear_indexAverage[stateYear] = index_average
    for stateYearKey in stateYear_indexAverage:
        info_object = AnnualHPI(int(stateYearKey[2:]),
                                stateYear_indexAverage[stateYearKey])
        states = stateYearKey[0:2]
        if states in annualize_quarter:
            annualize_quarter[states].append(info_object)
        else:
            annualize_quarter[states] = [info_object]
    return annualize_quarter

def main():
    """
    Asks the user to input the file and then depending on what file
    they entered it will either annualize the data or not. Then it
    will prompt the user to enter regions until they press enter.
    Then depending on the file it will nicely print out the top
    house index in terms of the quarter. Then it will print out the
    top values of the annual house indexes. Lastly, it will print
    all annual objects that belong to the region entered.
    """
    file = input("Enter region-based house price index filename: ")
    file = "data/" + file
    if file == "data/HPI_AT_ZIP5.txt":
        regions = []
        data_zip = read_zip_house_price_data(file)
        region = "placeholder"
        while region != "":
            region = input("Enter a region (Hit ENTER to stop): ")
            regions.append(region)
        regions.remove("")
        for region in regions:
            print('=' * 72)
            print_range(data_zip, region)
            print("Annualized Index Values for ", region)
            for regions in data_zip[region]:
                print(regions)
    else:
        regions = []
        data_quarter = read_state_house_price_data(file)
        data_annual = annualize(data_quarter)
        region = "placeholder"
        while region != "":
            region = input("Enter a region (Hit ENTER to stop): ")
            regions.append(region)
        regions.remove("")
        for region in regions:
            print('=' * 72)
            print_range(data_quarter, region)
            print_range(data_annual, region)
            print("Annualized Index Values for ", region)
            for regions in data_annual[region]:
                print(regions)

if __name__ == '__main__':
    main()
