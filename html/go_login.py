import pickle


def Application(ip, get, post):
    print(type(post))
    with open("f\\users", "rb") as f:
        s = pickle.loads(f.read())
    if s[post["username"]]["password"] == post["password"]:
        ok = True
    else:
        ok = False
    if ok:
        return 'successfully'
    return 'failed'
