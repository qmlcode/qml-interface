import numpy as np

from qml.dataprovider import XYZDataProvider
from qml.kernelridge import GenericKRR

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

    properties, filenames = get_data("data/train.txt")
    test_properties, test_filenames = get_data("data/test.txt")

    data = XYZDataProvider(properties, name="train")
    test = XYZDataProvider(test_properties, name="test")

    data.add_structures(filenames)
    test.add_structures(test_filenames)
    
    # data.read_database("train.db")
    # test.read_database("test.db")

    krr = GenericKRR("energy", sigma=250.0, llambda=1e-10)

    krr.train(data)
    krr.save("test_save/")
    krr.restore("test_save/")
    
    prediction = krr.predict(test)

    print np.mean(np.abs(prediction - test_properties))

if __name__ == "__main__":

    test_krr()
