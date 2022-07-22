from apachepy import createHttp, Response

sv = createHttp('0.0.0.0', 5000)


@sv.AddPage(page="/login")
def login(request: dict):
    return Response.ok + open("./www/login/index.html").read()


@sv.AddPage(page="/")
def hello(request: dict):
    print(request["body"])
    return Response.ok + '{"status":"ok"}'


@sv.AddPage(page="/about")
def about(request: dict):
    return Response.ok + open("./www/home/index.html").read()


sv.start()
