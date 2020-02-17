import math
from collections import OrderedDict
from datetime import datetime
import sys


def get_input_data(input_file_location):
    """Gets Border Crossing Entry Data from the spreadsheet,
    store into the python dictionary data structure
    """
    data = dict()
    with open(input_file_location, 'r') as file:
        header = file.readline().split(',')
        for row in file.readlines():
            port_name, state, port_code, border, date, measure, value = \
                row.split(',')[:7]
            try:
                timestamp = datetime.strptime(date, "%d/%m/%Y %H:%M:%S %p")
            except:                
                timestamp = datetime.strptime(date, "%d/%m/%Y %H:%M")
            border_measure = border + ',' + measure
            if timestamp not in data:
                data[timestamp] = dict()
            if border_measure not in data[timestamp]:
                data[timestamp][border_measure] = dict()
                data[timestamp][border_measure]['value_list'] = []
                data[timestamp][border_measure]['total'] = 0
            data[timestamp][border_measure]['value_list'].append(value)
            data[timestamp][border_measure]['total'] += int(value)
    return data


def compute_average_total(data):
    """This function computes the running monthly average of total crossings
    for a border and means of crossing across all the previous months.
    """
    data = OrderedDict(sorted(data.items(), key=lambda x: x[0], reverse=True))
    running_total_dict = dict()
    for date in list(data.keys())[::-1]:
        for border_measure, attributes in data[date].items():
            if border_measure in running_total_dict:
                current_average = running_total_dict[border_measure]['total'] / \
                    running_total_dict[border_measure]['count']
                if (float(current_average) % 1) >= 0.5:
                    data[date][border_measure]['running_total'] = math.ceil(
                        current_average)
                else:
                    data[date][border_measure]['running_total'] = round(
                        current_average)
                running_total_dict[border_measure]['count'] += 1
                running_total_dict[border_measure]['total'] += attributes['total']
            else:
                data[date][border_measure]['running_total'] = 0
                running_total_dict[border_measure] = dict()
                running_total_dict[border_measure]['count'] = 1
                running_total_dict[border_measure]['total'] = attributes['total']
    return data


def sort_border_measure(data):
    """This function sorts all the items in the dictionary in descending order 
    by Date, Value or number of crossings, Measure and Border.
    """
    for datetimestamp, borders_measures in data.items():
        sorted_borders_measures = OrderedDict(
            sorted(
                borders_measures.items(),
                key=lambda x: [
                    x[1]['total'],
                    x[0][1],
                    x[0][0]],
                reverse=True))
        data[datetimestamp] = sorted_borders_measures
    return data


def write_to_file(data, output_file_location):
    """
    Write to the output file location with file named report.csv
    with its respective columns Border, Date, Measure, Value and Average.
    """
    with open(output_file_location, 'w') as write_file:
        write_file.write('Border,Date,Measure,Value,Average\n')
        for datetimestamp, borders_measures in data.items():
            for border_measure, total_dict in borders_measures.items():
                border, measure = border_measure.split(',')
                date = datetimestamp.strftime("%d/%m/%Y %H:%M:%S AM")
                value = str(total_dict['total'])
                average = str(total_dict['running_total'])
                write_file.write(border + ',' + date + ',' + measure + ',')
                write_file.write(value + ',' + average + '\n')


def border_analytics(input_file_location, output_file_location):
    """This function performs 4 operations, 
    - gets input data
    - compute_average of the total of previous months
    - sort border measures 
    - print output to report.csv
    """
    data = get_input_data(input_file_location)
    data = compute_average_total(data)
    data = sort_border_measure(data)
    write_to_file(data, output_file_location)


if __name__ == '__main__':
    arguments = sys.argv
    if len(arguments) < 3:
        print('Function usage: python3.7 ./src/border_analytics.py '+\
            './input/Border_Crossing_Entry_Data.csv ./output/report.csv')
        sys.exit()
    input_file_location = arguments[1]
    output_file_location = arguments[2]
    print('Border Crossing Analysis Initiated')
    border_analytics(input_file_location, output_file_location)
    print('Report for Border Crossing Analysis generated')
