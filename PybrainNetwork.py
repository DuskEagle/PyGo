from pybrain.structure import FeedForwardNetwork, FullConnection, LinearLayer, SigmoidLayer
from pybrain.supervised.trainers import BackpropTrainer

def createNetwork (in_layer_size, hidden_layer_size, out_layer_size):
    network = FeedForwardNetwork()
    in_layer = LinearLayer(in_layer_size)
    hidden_layer = SigmoidLayer(hidden_layer_size)
    out_layer = LinearLayer(out_layer_size)

    network.addInputModule(in_layer)
    network.addModule(hidden_layer)
    network.addOutputModule(out_layer)

    in_to_hidden = FullConnection(in_layer, hidden_layer)
    hidden_to_out = FullConnection(hidden_layer, out_layer)

    network.addConnection(in_to_hidden)
    network.addConnection(hidden_to_out)

    network.sortModules()
    
    return network