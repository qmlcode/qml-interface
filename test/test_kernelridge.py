from __future__ import division, absolute_import, print_function

import numpy as np

from time import time

from qml.data import XYZDataProvider
from qml.machines import GenericKRR


def get_data(filename):

    f = open(filename)
    lines = f.readlines()
    f.close

    properties = [] 
    filenames = []

    for line in lines:
        tokens = line.split()
        filenames.append("qm7/" + tokens[0])
        properties.append(float(tokens[1]))

    return np.array(properties), filenames


def test_krr():

    properties, filenames = get_data("data/train2.txt")
    test_properties, test_filenames = get_data("data/test.txt")

    data = XYZDataProvider(properties, name="train")
    test = XYZDataProvider(test_properties, name="test")

    # data.add_structures(filenames)
    # test.add_structures(test_filenames)
    
    data.read_database("train.db")
    test.read_database("test.db")

    krr = GenericKRR("energy", sigma=80.0, llambda=1e-10)

    output_log = krr.train(data)
    print(output_log)

    krr.save("test_save/")
    krr.restore("test_save/")
    
    prediction = krr.predict(test)

    print(np.mean(np.abs(prediction - test_properties)))

if __name__ == "__main__":

    test_krr()
