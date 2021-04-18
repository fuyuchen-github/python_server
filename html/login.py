import pickle


def Application(ip, get, post):
    if post.get("username") == "" or post.get("password") == "" or post.get("username") == None or post.get("password") == None:
        return '{"message":"It cannot be empty."}'
    with open("f\\users", "rb") as f:
        s = pickle.loads(f.read())
    if s[post["username"]]["password"] == post["password"]:
        ok = True
    else:
        ok = False
    if ok:
        return '{"message":"correct"}'
    return '{"message":"The password is incorrect."}'
