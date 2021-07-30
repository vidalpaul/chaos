from datetime import datetime
import io
import time
import threading
from wsgiref.validate import validator
from wsgiref.simple_server import make_server
 
EXAMPLE_FILE = "./example.dat"
 
 
def update_EXAMPLE_FILE():
    """Writes the current date and time every 1 seconds into the example file. The file is created if it does not exist."""
    print("Will update to example file")
    while True:
        with io.open(EXAMPLE_FILE, "w") as f:
            f.write(datetime.now().isoformat())
        time.sleep(1)
 
 
def simple_app(environ, start_response):
    """Read the content of the example file and return it."""
    start_response('200 OK', [('Content-type', 'text/plain')])
    with io.open(EXAMPLE_FILE) as f:
        return [f.read().encode('utf-8')]
 
 
if __name__ == '__main__':
    t = threading.Thread(target=update_EXAMPLE_FILE)
    t.start()
 
    httpd = make_server('', 8080, simple_app)
    print("Listening to localhost:8080...")
 
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        httpd.shutdown()
        t.join(timeout=1)