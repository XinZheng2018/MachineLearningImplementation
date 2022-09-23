# Spring 2022 10601 HW1
# Author: Xin Zheng

import numpy as np
import sys

def read_in_file(filepath):
    '''
    This function read in tab-separated files and return the data as nparray
    :param filepath: the path to the file
    :return: a nparray storing data in the file
    '''
    file = np.genfromtxt(filepath,dtype=str,delimiter='\t')
    return file

def count_label(data, education=False):
    '''
    This function count the number of each label in the politician data
    :param data: np array of politician data
    :return: the number of democrat, the number of republican
    '''
    label1 = data[1][-1]
    label2 = ''
    label1_count = 0
    label2_count = 0
    for i in range(1, len(data)):
        row = data[i]
        if row[-1] == label1:
            label1_count += 1
        else:
            if label2 == '':
                label2 = row[-1]
            label2_count += 1
    return label1, label1_count, label2, label2_count

def train_data(data):
    '''
    find the most common label
    :param data: np array of data
    :return: the label that appears the most times in the data
    '''
    label1, label1_count, label2, label2_count = count_label(data)
    if label1_count > label2_count:
        return label1
    elif label1_count < label2_count:
        return label2
    else:
        return label2 if label1 < label2 else label1

def get_error_rate(majority_label, data):
    '''
    get the ratio of the number of errors to the total number test
    :param majority_label: most common label
    :param data: np array of data
    :return: the error rate
    '''
    error = 0
    for i in range(1, len(data)):
        row = data[i]
        if row[-1] != majority_label:
            error += 1
    return error/(len(data)-1)

def write_labels(data, path, majority_label):
    '''
    write the label files
    :param data: np array of data
    :param path: output path
    :param majority_label: most common label
    :return: None
    '''
    with open(path, mode='w') as file:
        for i in range(1,len(data)):
            file.write(majority_label + '\n')
    file.close()

def write_metrics(error_train, error_test, metrics):
    '''
    write the metrics file
    :param error_train: error rate of training set
    :param error_test: error rate of testing set
    :param metrics: path to the metrics file
    :return: None
    '''
    with open(metrics, mode='w') as file:
        file.write("error(train): " + str(error_train) + '\n')
        file.write("error(test): " + str(error_test))


if __name__ == '__main__':
    # get the file path from sys argv
    train_path = sys.argv[1]
    test_path = sys.argv[2]
    train_labels = sys.argv[3]
    test_labels = sys.argv[4]
    metrics = sys.argv[5]

    # read in training file
    train_set = read_in_file(train_path)

    # get the majority label
    MAJORITY_LABEL = train_data(train_set)

    # write training .labels file
    write_labels(train_set, train_labels, MAJORITY_LABEL)

    # read in test file
    test_set = read_in_file(test_path)

    # write testing .labels file
    write_labels(test_set, test_labels, MAJORITY_LABEL)

    # compute the error rate
    error_rate_train = get_error_rate(MAJORITY_LABEL, train_set)
    error_rate_test = get_error_rate(MAJORITY_LABEL, test_set)

    # write the metrics file
    write_metrics(error_rate_train, error_rate_test, metrics)


