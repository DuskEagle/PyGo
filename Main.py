from SgfLoader import *
import NeuralNetwork

sgf_files_file = open("sgffiles.txt")
# TEST: Windows
sgf_files = list(map(lambda filename : filename.strip('\n').strip('\r'), sgf_files_file.readlines()))
sgf_files_file.close()

training_data = SgfLoader.loadData(sgf_files[0:20])
test_data = SgfLoader.loadData(sgf_files[20:40])

net = NeuralNetwork.NeuralNetwork([361, 180, 361])
net.SGD(training_data, 1, 10, 100.0)

evaluation = net.evaluate(test_data)
len_test_data = len(test_data)
print("Weights:")
print(net.weights)
print("Biases:")
print(net.biases)
print("Passed on {}/{} ({:.1f}%).".format(evaluation, len_test_data, (evaluation/len_test_data)*100))