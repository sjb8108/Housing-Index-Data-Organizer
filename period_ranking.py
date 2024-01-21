"""
CSCI 141
Author: Scott Bullock
Project
The program uses function from index_tools.py to utizile
the functions in this program. The function including getting
all the quarter data desired by the user and the annual data
desired by the user
"""
import index_tools

def quarter_data(data, year, quarter):
    """
    Gets all the objects that share the year and quarter in the parameter
    and then sorts the data from highest to lowest
    Precondition: The data dictionary must only include quarterHPI objects
    :param data: a dictionary mapping a state region to a
    list of QuarterHPI objects
    :param year: year of interest
    :param quarter: quarter of interest, expressed as an integer between 1 and 4.
    :return: A list of (region, HPI) tuples sorted from high value
    HPI to low value HPI.
    """
    unsorted_list_quarter = []
    for state in data.keys():
        for element in data[state]:
            if element.year == str(year) and element.qtr == str(quarter):
                state_index = (state, float(element.index))
                unsorted_list_quarter.append(state_index)
    sorted_list_quarter = sorted(unsorted_list_quarter,
                                 key=lambda x: float(x[1]), reverse=True)
    return sorted_list_quarter

def annual_data(data, year):
    """
    Gets all the objects that share the year in the parameter
    and then sorts the data from highest to lowest
    Precondition: data dictionary must only include annualHPI objects
    :param data: a dictionary mapping a state or zip code
    to a list of AnnualHPI objects
    :param year: year of interest
    :return: A list of (region, HPI) tuples sorted from high value
    HPI to low value HPI.
    """
    unsorted_list_annual = []
    for region in data.keys():
        for element in data[region]:
            if float(element.year) == float(year):
                region_index = (region, float(element.index))
                unsorted_list_annual.append(region_index)
    sorted_list_annual = sorted(unsorted_list_annual,
                                key=lambda x: float(x[1]), reverse=True)
    return sorted_list_annual

def main():
    """
    Asks the user to enter a file and depending on the file it would
    read the file a type of way and then asks the user to enter regions
    until the user hits ENTER. Lastly it prints the ranking of the house
    index prices
    """
    file = input("Enter region-based house price index filename: ")
    file = "data/" + file
    year = int(input("Enter year of interest for house prices: "))
    if file == "data/HPI_AT_ZIP5.txt":
        data = index_tools.read_zip_house_price_data(file)
        sort_annual_data = annual_data(data, year)
        print("")
        print(year, "Annual Ranking")
        index_tools.print_ranking(sort_annual_data)
    else:
        data = index_tools.read_state_house_price_data(file)
        annual = index_tools.annualize(data)
        sort_annual_data = annual_data(annual, year)
        print("")
        print(year, "Annual Ranking")
        index_tools.print_ranking(sort_annual_data)

if __name__ == "__main__":
    main()
