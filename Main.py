import communication
import os
import pickle
import json


def look_for_file(file_name):
    """
    return:
        0   have original file but no file to run
        1   have original file and the file to run
        3   have file to run
        404 no file
    """
    main_file_name = os.path.splitext(file_name)[0]  # get the main name
    # have the original html file
    if os.path.exists(main_file_name + ".html"):
        # have original file and the file to run
        if os.path.exists(main_file_name + ".py"):
            return 1, main_file_name + ".html", main_file_name + ".py"
        # have original file but no file to run
        return 0, main_file_name + ".html", None
    # have file to run
    if os.path.exists(main_file_name + ".py"):
        return 3, main_file_name + ".py", None
    # cant find the file
    else:
        return 404, None, None


def run_file(file_name, ip_addr, get, post):
    # write the file to a place where can reach it
    with open(file_name, "r") as f:
        file_to_run = f.read()
    with open("temp.py", "w") as f:
        f.write(file_to_run)

    # write the arguments to argu.pickle
    with open("argu.pickle", "wb") as f:
        f.write(pickle.dumps([ip_addr, get, post]))
    os.system("python run_the_file.py")

    # read the out.txt
    with open("out.txt", "r") as f:
        s = f.read()
    return s


def run_and_send(file_name, ip, get, post):
    # get the json string
    return_of_ins = run_file(os.path.splitext(file_name)[0] + ".py", ip, get, post)
    # load the json string
    return_of_ins = json.loads(return_of_ins)
    # read the file
    with open(file_name, "r", encoding="utf-8") as f:
        s = f.read()
    # change the final file
    for i in return_of_ins:
        s = s.replace("{{%s}}" % i, return_of_ins[i])
    return s


def response(request: str, addr):
    print(request)
    request_line = request.splitlines()
    info = request_line[0].split(" ")
    method = info[0]
    path = info[1]
    if "?" in path:
        get = "?".join(path.split("?")[1:])
        get_list = get.split("&")
        get = {}
        for i in get_list:
            i = i.split("=")
            get[i[0]] = i[1]
    else:
        get = {}
    
    i = 0
    while request_line[i] != "":
        i += 1
    head = request_line[1:i]
    try:
        post = request_line[i + 1]
        post_list = post.split("&")
        post = {}
        for i in post_list:
            i = i.split("=")
            post[i[0]] = i[1]
    except:
        post = {}



    file_code = look_for_file("html" + path.replace("/", "\\"))

    found = file_code[0]

    if found == 0:
        with open(file_code[1], "rb") as f:
            s = f.read()
        return 200, s
    if found == 1:
        return 200, run_and_send(file_code[1], addr[0], pickle.dumps(get), pickle.dumps(post)).encode("utf-8")
    if found == 3:
        return 200, run_file(file_code[1], addr[0], pickle.dumps(get), pickle.dumps(post)).encode("utf-8")
    if found == 404:
        with open("html\\404.html", "rb") as f:
            s = f.read()
        return 404, s


def write_response(file_given):
    dictionary = {200: "200 OK", 404: "404 Not Found"}
    return ("HTTP/1.1 " + dictionary[file_given[0]] + "\r\n\r\n").encode("utf-8"), file_given[1]


def oper_main(a, b):
    serv = write_response(response(a, b))
    print(serv)
    print("*" * 100)
    return serv


def test(a, b):
    print(a, b)
    return "hello".encode("utf-8")


main = communication.Server("", 80, oper_main)
main.start_service()
