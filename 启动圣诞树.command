#!/bin/zsh
set -eu
ROOT="${0:A:h}"
if ! command -v python3 >/dev/null 2>&1; then
  printf '这个设备没有 Python 3，先为你打开无需摄像头的版本。\n'
  open "$ROOT/圣诞星愿.html"
  exit 0
fi
exec python3 - "$ROOT" <<'PY'
import functools
import http.server
import subprocess
import sys
import urllib.parse

class Handler(http.server.SimpleHTTPRequestHandler):
    extensions_map = {**http.server.SimpleHTTPRequestHandler.extensions_map,
                      '.mjs': 'text/javascript', '.wasm': 'application/wasm',
                      '.task': 'application/octet-stream'}
    def list_directory(self, path):
        self.send_error(404)
    def log_message(self, fmt, *args):
        pass

handler = functools.partial(Handler, directory=sys.argv[1])
with http.server.ThreadingHTTPServer(('127.0.0.1', 0), handler) as server:
    url = f'http://127.0.0.1:{server.server_port}/' + urllib.parse.quote('圣诞星愿.html')
    print('圣诞星愿已启动：' + url, flush=True)
    print('关闭这个终端窗口或按 Ctrl+C 即可停止。照片和摄像头画面不会上传。', flush=True)
    subprocess.run(['open', url], check=False)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
PY
