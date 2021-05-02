import temp
import json

with open("argu.json", "r") as f:
    json_str = f.read()

json_str = json.loads(json_str)

with open("out.txt", "w") as f:
    f.write(temp.Application(json_str[0], json.loads(json_str[1]), json.loads(json_str[2])))