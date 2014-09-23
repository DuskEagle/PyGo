from pybrain.datasets import SupervisedDataSet
from pybrain.structure import FeedForwardNetwork, FullConnection, LinearLayer, SigmoidLayer
from pybrain.supervised.trainers import BackpropTrainer

from SgfLoader import *
import logging
import pickle

""" This file is a mess, as it's constantly getting rewritten. """

np.set_printoptions(threshold=np.nan)
logging.basicConfig(level=logging.DEBUG)

sgf_files_file = open("sgffiles.txt")
# TEST: Windows
sgf_files = list(map(lambda filename : filename.strip('\n').strip('\r'), sgf_files_file.readlines()))
sgf_files_file.close()

data = SgfLoader.loadData(sgf_files[0:100])
num_examples = len(data[0])

network = FeedForwardNetwork()
in_layer = LinearLayer(361*6)
hidden_layer = SigmoidLayer(361*4)
out_layer = LinearLayer(361)

network.addInputModule(in_layer)
network.addModule(hidden_layer)
network.addOutputModule(out_layer)

in_to_hidden = FullConnection(in_layer, hidden_layer)
hidden_to_out = FullConnection(hidden_layer, out_layer)

network.addConnection(in_to_hidden)
network.addConnection(hidden_to_out)

network.sortModules()

dataset = SupervisedDataSet(361*2, 361)
trainer = BackpropTrainer(network, dataset, learningrate=0.1)

#print(training_data[0][0].shape)

for datum in training_data:
    #print(datum)
    dataset.addSample(datum[0],datum[1])

for i in range(3):
    print("Epoch " + str(i+1))
    trainer.train()
    
    correct = 0
    total = 0
    for datum in test_data:
        net_result = np.argmax(network.activate(datum[0]))
        actual_result = np.argmax(datum[1])
        print("net_result: " + str(net_result) + "; actual_result: " + str(actual_result))
        total += 1
        if net_result == actual_result:
            correct += 1

    if total > 0:
        print("Correct/Total: " + str(correct) + "/" + str(total) + " (" + str(correct/total) + ")")

