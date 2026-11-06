# Recebe POSTs do Studio e grava em recebidos/<path>
import http.server, os, sys
DEST = sys.argv[1]
class H(http.server.BaseHTTPRequestHandler):
    def do_POST(self):
        n = int(self.headers.get('Content-Length', 0))
        dados = self.rfile.read(n)
        nome = os.path.basename(self.path.strip('/')) or 'sem_nome'
        with open(os.path.join(DEST, nome), 'wb') as f:
            f.write(dados)
        self.send_response(200); self.end_headers(); self.wfile.write(b'ok %d' % len(dados))
http.server.HTTPServer(('127.0.0.1', 8766), H).serve_forever()
