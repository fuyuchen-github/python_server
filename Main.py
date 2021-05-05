import communication
import os
import json


with open("settings.json", "r") as f:
    settings = f.read()
settings = json.loads(settings)

def look_for_file(file_name):
    """
    return:
        0   there is original file but no file to run
        1   there is original file and the file to run
        3   this is file to run
        404 no file
    """
    print(file_name)

    if settings["hot sites"].get(file_name[4:]) != None:
        return look_for_file("html" + settings["hot sites"][file_name[4:]])

    main_file_name = os.path.splitext(file_name)[0]  # get the main name
    if main_file_name[0] == "'":
        return 0
    # have the original html file
    if os.path.exists(main_file_name + ".html"):
        # have original file and the file to run
        if os.path.exists(main_file_name + "-html.py"):
            return 1, main_file_name + ".html", main_file_name + "-html.py"
        # have original file but no file to run
        return 0, main_file_name + ".html", None
# repeat{
    if os.path.exists(main_file_name + ".css"):
        # have original file and the file to run
        if os.path.exists(main_file_name + "-css.py"):
            return 1, main_file_name + ".css", main_file_name + "-css.py"
        # have original file but no file to run
        return 0, main_file_name + ".css", None
    if os.path.exists(main_file_name + ".js"):
        # have original file and the file to run
        if os.path.exists(main_file_name + "-js.py"):
            return 1, main_file_name + ".js", main_file_name + "-js.py"
        # have original file but no file to run
        return 0, main_file_name + ".js", None
# }
    # have file to run
    if os.path.exists(main_file_name + ".py"):
        return 3, main_file_name + ".py", None
    # can open the file whithout any operations
    if os.path.exists(file_name):
        return 0, file_name, None
    # can't find the file
    else:
        return 404, None, None


def run_file(file_name, ip_addr, get, post):
    # write the file to a place where can reach it
    with open(file_name, "r", encoding="utf-8") as f:
        file_to_run = f.read()
    with open("temp.py", "w", encoding="utf-8") as f:
        f.write(file_to_run)

    # write the arguments to argu.json
    with open("argu.json", "w") as f:
        f.write(json.dumps([ip_addr, get, post]))
    os.system("python run_the_file.py")

    # read the out.txt
    with open("out.txt", "r") as f:
        s = f.read()

    if s.split(" ")[0] == "spec":
        return s.split(" ")[1:]

    return s


def run_and_send(html_file_name, py_file_name, ip, get, post):
    # get the json string
    return_of_ins = run_file(py_file_name, ip, get, post)
    if isinstance(type(return_of_ins), list):
        if return_of_ins[0] == "jump":
            pass
    # load the json string
    return_of_ins = json.loads(return_of_ins)
    # read the file
    with open(html_file_name, "r", encoding="utf-8") as f:
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
        return 200, run_and_send(file_code[1], file_code[2], addr[0], json.dumps(get), json.dumps(post)).encode("utf-8")
    if found == 3:
        return 200, run_file(file_code[1], addr[0], json.dumps(get), json.dumps(post)).encode("utf-8")
    else:
        with open("html\\%s.html" % found, "rb") as f:
            s = f.read()
        return found, s


def write_response(file_given):
    dictionary = {200: "200 OK", 404: "404 Not Found", 403: "403 Forbidden"}
    return ("HTTP/1.1 " + dictionary[file_given[0]] + "\r\n\r\n").encode("utf-8"), file_given[1]


def oper_main(a, b):
    serv = write_response(response(a, b))
    for i in serv:
        print(i.decode("utf-8"))
    print("*" * 100)
    return serv


def test(a, b):
    print(a, b)
    return "hello".encode("utf-8")


main = communication.Server("", 80, oper_main)
main.start_service()
