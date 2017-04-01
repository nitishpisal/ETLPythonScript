
import csv
from collections import defaultdict
import re
import json
import dicttoxml
import pickle
from xml.dom.minidom import parseString
filename = 'PythonTest.csv'

def save_to_json(dictionary_object):
    with open('data.json','w') as output_file:
        json.dump(dictionary_object, output_file)


def save_to_xml(dictionary_object):
    xml_snippet = dicttoxml.dicttoxml(dictionary_object)
    dom = parseString(xml_snippet)
    pickle.dump(dom.toprettyxml().encode('ascii'),open('data.xml','wb'))
    #print dom.toprettyxml()

def read_columns():
    final = dict({})
    average = 0
    sum = 0
    columns = defaultdict(list) # each value in each column is appended to a list

    with open(filename) as file:
        reader = csv.DictReader(file) # read rows into a dictionary format
        for row in reader: # read a row as {column1: value1, column2: value2,...}
            for (key,value) in row.items(): # go over each column name and value
                key = re.search(r'HOST\d+', key)
                if key:
                    if (not value is None and not value is ''):
                        columns[key.group()].append(value) # append the value into the appropriate list

                                        # based on column name k
        if 'Date / Time' in columns:
            del columns['Date / Time']

        for (key,value) in columns.items():
            #print key
            for each_val in value:
                if (not each_val is None and not each_val is ''):
                    sum = sum + float(each_val)

            average = format((sum / len(value)), '.2f')
            print (value)
            maximum = max(value)
            minimum = min(value)
            sum = 0
            final[key] = dict({'Average':average,
                               'Max':maximum,
                               'Min':minimum})
        curr_max =0.0
        curr_min =100.0
        sum = 0.0
        count = 0
        for (key,value) in final.items():
            if float(final[key]['Max']) > curr_max:
                curr_max = float(final[key]['Max'])
            if float(final[key]['Min']) < curr_min:
                curr_min = float(final[key]['Min'])
            sum = sum + float(final[key]['Average'])
            count = count + 1

        curr_avg = format((sum / count), '.2f')
        print "Final_max: ", curr_max
        print "Final_min: " , curr_min
        print "Final_average: " , curr_avg
        final.update({'Final_Count':{'Max':curr_max, 'Average':curr_avg, 'Min':curr_min}})
        print "Final JSON : ", final
        save_to_json(final)
        save_to_xml(final)

if __name__ == "__main__":
    read_columns()

