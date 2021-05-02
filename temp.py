import json


def Application(ip, get, post):
    if post.get("username") == "" or post.get("password") == "" or post.get("username") == None or post.get("password") == None:
        return '{"message":"Password and username cannot be empty."}'
    with open("f\\users.json", "rb") as f:
        s = json.loads(f.read())
    if s.get(post["username"]) == None:
        return '{"message":"User dose not exist."}'
    if s[post["username"]]["password"] == post["password"]:
        ok = True
    else:
        ok = False
    if ok:
        return '{"message":"correct"}'
    return '{"message":"The password is incorrect."}'
