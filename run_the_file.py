import temp
import pickle

with open("argu.pickle", "rb") as f:
    json_str = f.read()

json_str = pickle.loads(json_str)

with open("out.txt", "w") as f:
    f.write(temp.Application(json_str[0], pickle.loads(json_str[1]), pickle.loads(json_str[2])))