import pickle

def load_pickle(path):
    with open(path, 'rb') as file:
        data = pickle.load(file)
        return list(data['url'])