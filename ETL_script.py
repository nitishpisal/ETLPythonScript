import csv
import re
import pickle
import dicttoxml
from xml.dom.minidom import parseString
import json

result_dict = dict({})
host_name = []
host = ""
average =0
my_list = []
final_list = []


def save_to_json(dictionary_object):
    with open('data.json','w') as output_file:
        json.dump(dictionary_object, output_file)


def save_to_xml(dictionary_object):
    xml_snippet = dicttoxml.dicttoxml(dictionary_object)
    dom = parseString(xml_snippet)
    pickle.dump(dom.toprettyxml().encode('ascii'),open('data.xml','wb'))
    #print dom.toprettyxml()

def calculate():
    with open('PythonTest.csv') as csv_file:
        reader=csv.reader(csv_file, delimiter=',')
        #Each row read from the csv file is returned as a list of strings.
        count = 0
        c = 0
        overall = {}
        stats = []
        for columns in reader:
            # print "each row= ", columns[1:]
            if count == 0:
                for column in columns[1:]:
                    key = re.search(r'HOST\d+', column)
                    stats_dict = {}
                    stats_dict['host_max'] = 0.0
                    stats_dict['host_min'] = 100.0
                    stats_dict['sum'] = 0.0
                    stats_dict['hostname'] = key.group()
                    stats.append(stats_dict)
                    overall['max'] = 0.0
                    overall['min'] = 100.0
                    overall['sum'] = 0.0
            else:
                row_max = 0.0
                row_min = 100.0
                row_sum = 0.0
                c = 0
                for column in columns[1:]:
                    # print "column", column
                    if (not column is '' and not column is None):
                        stats_dict = stats.__getitem__(c)
                        if float(column) > float(stats_dict['host_max']):
                            stats_dict['host_max'] = float(column)
                        if float(column) < float(stats_dict['host_min']):
                            stats_dict['host_min'] = float(column)
                        stats_dict['sum'] = float(stats_dict['sum']) + float(column)
                        stats_dict['avg'] = format((float(stats_dict['sum']) / (count)), '.2f')

                        if float(stats_dict['host_max']) > float(row_max):
                            row_max = float(stats_dict['host_max'])
                        if float(stats_dict['host_min']) < float(row_min):
                            row_min = float(stats_dict['host_min'])
                        row_sum += stats_dict['sum']
                    c += 1

                if row_max > float(overall['max']):
                    overall['max'] = float(row_max)
                if row_min < float(overall['min']):
                    overall['min'] = float(row_min)
                overall['sum'] = row_sum

            count += 1

        overall['avg'] = format((float(overall['sum']) / ((count-1)*c)), '.2f') # count should be 1 less for offsetting header row
        print "Overall Statistics: ",overall
        print "Each Host Statistics: ",stats
        save_to_xml(stats)
        save_to_json(stats)


if __name__ == "__main__":
    calculate()