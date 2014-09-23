import logging
from pybrain.datasets import SupervisedDataSet

from LoadData import loadData
from PybrainNetwork import makeNetwork
from SgfLoader import *

import StreamingPickle

np.set_printoptions(threshold=np.nan)
logging.basicConfig(level=logging.DEBUG)

in_layer_size = 361*2
out_layer_size = 361

network = makeNetwork(in_layer_size, 2000, out_layer_size)

dataset = SupervisedDataSet(in_layer_size, out_layer_size)
trainer = BackpropTrainer(network, dataset, learningrate=0.1/200)

for epoch in range(3):
    print("Epoch " + str(epoch+1))
    
    training_file = open("training-data.pkl", "rb")
    validation_file = open("validation-data.pkl", "rb")

    batch_iter = 0
    while True:
        print("batch_iter: " + str(batch_iter))
        training_set_x, training_set_y = loadData(training_file, 1)
        print(len(training_set_x))
        if len(training_set_x) == 0:
            break
        
        print("there")
        for i in range(len(training_set_x)):
            dataset.addSample(training_set_x[i],training_set_y[i])
        print("here")
        trainer.train()
        print("now")
        dataset.clear()
        batch_iter += 1
    
    # Clear references to these so the garbage collector can clean them
    # once the garbage collector chooses to.
    del training_set_x
    del training_set_y
    
    correct = 0
    total = 0
    while True:
        
        print("Testing validation set")
        
        validation_set_x, validation_set_y = loadData(validation_file, 1)
        if len(validation_set_x) == 0:
            break
        
        for i in range(len(validation_set_x)):
            net_result = np.argmax(network.activate(validation_set_x[i]))
            actual_result = np.argmax(validation_set_y[i])
            #print("net_result: " + str(net_result) + "; actual_result: " + str(actual_result))
            total += 1
            if net_result == actual_result:
                correct += 1
                
    del validation_set_x
    del validation_set_y

    if total > 0:
        print("Correct/Total: " + str(correct) + "/" + str(total) + " (" + str(correct/total) + ")")
    
    training_file.close()
    validation_file.close()
