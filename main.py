from pypache import createHttp, Response

sv = createHttp('0.0.0.0', 5000)
rp = Response()

@sv.AddPage("/", method="GET")
def main(request :dict):
    body = '{"status":"ok"}'
    return rp.header(rp.ok, "application/json", body)

@sv.AddPage("/api/register", method="POST")
def register(request :dict):
    request['']
    return '{"status":"ok"}'

@sv.AddPage("/api/login", method="POST")
def login(request :dict):
    body = session.sign("Token", "PUTOOOO", 1)
    return rp.header(rp.ok, "plain/text", body)

@sv.AddPage("/api/auth", method="GET")
def auth(request :dict):
    # Verifica que exista session-token
    try:
        token = request["session-token"]
    except KeyError:
        body = "<h1>Request no valida</h1>"
        return rp.header(rp.badrequest, "text/html", body)
    
    # Cheackea que existe el token
    if session.check(token) != True:# No existe o expiro 
        body = "<h1>Acceso Denegado</h1>" 
        return rp.header(rp.forbidden,"text/html", body) 
    else: # Existe
        body = '{"status":"autentificado"}'
        return rp.json(rp.ok, "{'Status': 'ok'}")

sv.start()
