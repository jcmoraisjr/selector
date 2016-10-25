import json, BaseHTTPServer

class Server:
    def __init__(s, clustersRef, locksRef):
        global clusters, locks
        clusters = clustersRef
        locks = locksRef

    def listen(s, port):
        s.server = BaseHTTPServer.HTTPServer(('', port), RequestHandler)
        s.server.serve_forever()

class RequestHandler(BaseHTTPServer.BaseHTTPRequestHandler):
    def do_GET(s):
        s.response404()

    def do_POST(s):
        try:
            s.handlePost()
        except:
            s.response400()
            raise

    def response(s, code, status, data, log):
        s.send_response(code)
        s.send_header("Content-Type", "application/json")
        s.end_headers()
        data["status"] = status
        s.wfile.write(json.dumps(data))
        print "{0} {1} -- {2}({3}) {4}".format(s.command, s.path, code, status, log)

    def responseMsg(s, code, status, msg, log=""):
        if log == "":
            log = msg
        s.response(code, status, {"msg": msg}, log)

    def response400(s, msg="", log=""):
        if msg == "":
            msg = "Bad request"
        s.responseMsg(400, "fail", msg, log)

    def response404(s):
        s.responseMsg(404, "fail", "Not found")

    def log_request(s, code):
        pass

    def handlePost(s):
        request = json.loads(s.rfile.read(int(s.headers.getheader("Content-Length"))))
        if s.path == "/acquire":
            s.acquire(request)
        elif s.path == "/release":
            s.release(request)
        else:
            s.response404()

    def acquire(s, request):
        qty = request["qty"]
        cluster = request["cluster"]
        if clusters.hasCluster(cluster):
            locks.acquire()
            try:
                availCount = clusters.size(cluster) - locks.size(cluster)
                if not isinstance(qty, (int, long)) or (qty <= 0):
                    s.response400("Invalid qty: {0}".format(qty))
                elif availCount < qty:
                    s.responseMsg(200, "fail", "Cluster {0} has {1} available item(s)".format(cluster, availCount), "cluster: {0} request: {1} avail: {2}".format(cluster, qty, availCount))
                else:
                    availItems = clusters.acquireUnlocked(qty, cluster, locks.items(cluster))
                    locks.addItems(cluster, availItems)
                    locks.write()
                    s.response(200, "ok", {"id":locks.strNextId(), "items":availItems}, "cluster: {0} id: {1} qty: {2} items: {3}".format(cluster, locks.strNextId(), qty, availItems))
            finally:
                locks.release()
        else:
            s.responseMsg(200, "fail", "Cluster not found: {0}".format(cluster))

    def release(s, request):
        strId = request["id"]
        locks.acquire()
        try:
            if locks.removeItems(strId):
                locks.write()
                s.responseMsg(200, "ok", "Id {0} released".format(strId))
            else:
                s.responseMsg(200, "fail", "Id not found: {0}".format(strId))
        finally:
            locks.release()
