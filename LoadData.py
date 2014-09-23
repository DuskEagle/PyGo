import StreamingPickle

def loadData(fileobj, batch_size):
    """ Loads the dataset

    :type dataset: FileObj, typically created by `open(filename, 'rb')`
    :param dataset: the path to the dataset
    
    :type batch_size: int
    :param batch_size: Maximum number of examples to load.
    """

    # Load the dataset
    data_set = ([],[])
    gen = StreamingPickle.s_load(fileobj)
    for i in range(batch_size):
        try:
            d = next(gen)
            print(len(d))
            data_set[0].extend(d)
            data_set[1].extend(next(gen))
        except StopIteration:
            break
    return data_set