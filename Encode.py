from SgfLoader import *
import logging
import StreamingPickle

logging.basicConfig(level=logging.DEBUG)

sgf_files_file = open("sgffiles.txt")
# TEST: Windows
sgf_files = list(map(lambda filename : filename.strip('\n').strip('\r'), sgf_files_file.readlines()))
sgf_files_file.close()

training_file = open("training-data.pkl", "wb")
validation_file = open("validation-data.pkl", "wb")
testing_file = open("testing-data.pkl", "wb")

games_per_batch = 100
#for i in range(0, len(sgf_files), games_per_batch):
for i in range(0, 500, games_per_batch):
    print(str(i) + " out of " + str(len(sgf_files)) + " done encoding.") 
    data = SgfLoader.loadData(sgf_files[i:i+games_per_batch], library="pybrain", format="format2")
    num_examples = len(data[0])
    training_data = (data[0][:int(num_examples*.8)], data[1][:int(num_examples*.8)])
    validation_data = (data[0][int(num_examples*.8):int(num_examples*.9)], data[1][int(num_examples*.8):int(num_examples*.9)])
    testing_data = (data[0][int(num_examples*.9):], data[1][int(num_examples*.9):])
    
    StreamingPickle.s_dump(training_data, training_file)
    StreamingPickle.s_dump(validation_data, validation_file)
    StreamingPickle.s_dump(testing_data, testing_file)

training_file.close()
validation_file.close()
testing_file.close()
