"""
CSCI 141
Author: Scott Bullock
Project
The program uses the math libray to calculate the cagr
and we use index_tools.py functions. The function will
get compound annual growth rates and sorts them into a list
"""
import math
import index_tools

def cagr(idxlist, periods):
    """
    Computes the compound annual growth rate for a period.
    Precondition: HPI0's year is before HPI1's year, idxlist is a list
    of two HPI objects
    :param idxlist: a 2-item list of [HPI0, HPI1]
    :param periods: The number that represents the amount of years
    between both HPI0 and HPI1
    :return: A float representing the compound annual growth rate
    """
    ratio = (idxlist[1]/idxlist[0])
    compound = (math.pow(ratio, (1/periods))-1)*100
    return compound

def calculate_trends(data, year1, year2):
    """
    Sorts regions by their compound annual growth rate and puts them
    in a list that includes tuples that are sorted
    Precondition: year1 has to be before year2 and data includes only
    annualHPI objects
    :param data: a dictionary from region to a list of AnnualHPI objects
    :param year1: The starting year to calculate the CAGR
    :param year2: The ending year to calculate the CAGR
    :return: A list of (region, rate) tuples sorted in descending order
    by the compound annual growth rate
    """
    period = year2-year1
    region_year1_year2 = []
    region_cagr = []
    for region in data.keys():
        year1_in_list = False
        year2_in_list = False
        for element in data[region]:
            if int(element.year) == year1:
                year1_in_list = True
                year1_index = float(element.index)
            if int(element.year) == year2:
                year2_in_list = True
                year2_index = float(element.index)
        if year1_in_list is True and year2_in_list is True:
            region_year1_year2.append((region, year1_index, year2_index))
    for info in region_year1_year2:
        region_cagr.append((info[0], cagr([info[1], info[2]], period)))
    sorted_cagr = sorted(region_cagr, key=lambda x: float(x[1]), reverse=True)
    return sorted_cagr

def main():
    """
    Asks the user for a file and depending on the type of file it will read it
    The user will be also be prompted to enter a starting and ending year.
    THen the data will be sorted by the cagr's and printing in a top 10 and
    bottom 10 order.
    """
    file = input("Enter region-based house price index filename: ")
    file = "data/" + file
    year1 = int(input("Enter starting year of interest: "))
    year2 = int(input("Enter ending year of interest: "))
    if file == "data/HPI_AT_ZIP5.txt":
        data = index_tools.read_zip_house_price_data(file)
        data_sorted = calculate_trends(data, year1, year2)
        index_tools.print_ranking(data_sorted)
    else:
        data = index_tools.read_state_house_price_data(file)
        annual = index_tools.annualize(data)
        data_sorted = calculate_trends(annual, year1, year2)
        index_tools.print_ranking(data_sorted)

if __name__ == "__main__":
    main()
