#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""圣诞星愿 · 本地启动器（Windows / macOS / Linux 通用）

只在本机 127.0.0.1 上启动一个静态文件服务器，让浏览器可以通过
http://localhost 打开页面。这样才能正常加载 MediaPipe 手势模型，
并让摄像头被识别为「安全来源」（localhost 属于安全上下文）。

用法：
    python server.py [项目根目录]

照片与摄像头画面全部在浏览器本机处理，不会上传、不会录制。
"""

import functools
import http.server
import os
import sys
import urllib.parse
import webbrowser

# 部分系统自带的 MIME 表缺少这些后缀，补齐后浏览器才能正确加载
# 手势模型（ES Module / WebAssembly / 模型文件 / 音视频 / 字体）。
EXTRA_MIME = {
    ".mjs": "text/javascript",
    ".js": "text/javascript",
    ".wasm": "application/wasm",
    ".task": "application/octet-stream",
    ".ttf": "font/ttf",
    ".otf": "font/otf",
    ".m4a": "audio/mp4",
    ".wav": "audio/wav",
    ".webp": "image/webp",
}

PAGE_CANDIDATES = ("圣诞星愿.html", "index.html", "index.htm")


def pick_page(root):
    """挑选要打开的首页文件。"""
    for name in PAGE_CANDIDATES:
        if os.path.isfile(os.path.join(root, name)):
            return name
    return PAGE_CANDIDATES[0]


def make_server(root, page=None):
    """在 127.0.0.1 的随机端口上创建静态服务器，返回 (server, url, page)。"""
    root = os.path.abspath(root)
    if not page:
        page = pick_page(root)

    class Handler(http.server.SimpleHTTPRequestHandler):
        extensions_map = {
            **http.server.SimpleHTTPRequestHandler.extensions_map,
            **EXTRA_MIME,
        }

        # 不提供目录列表，避免误访问时暴露文件结构
        def list_directory(self, path):
            self.send_error(404, "Not Found")
            return None

        # 静默访问日志，保持窗口干净
        def log_message(self, fmt, *args):
            pass

        def end_headers(self):
            self.send_header("Cache-Control", "no-store")
            super().end_headers()

    handler = functools.partial(Handler, directory=root)
    server = http.server.ThreadingHTTPServer(("127.0.0.1", 0), handler)
    url = "http://127.0.0.1:%d/%s" % (server.server_port, urllib.parse.quote(page))
    return server, url, page


def main():
    # 尽量让控制台按 UTF-8 输出中文（失败也不影响运行）
    for stream in (sys.stdout, sys.stderr):
        try:
            stream.reconfigure(encoding="utf-8")
        except Exception:
            pass

    root = sys.argv[1] if len(sys.argv) > 1 else os.path.dirname(os.path.abspath(__file__))
    server, url, _page = make_server(root)

    print("圣诞星愿已启动：" + url, flush=True)
    print("关闭这个窗口或按 Ctrl+C 即可停止。照片和摄像头画面不会上传。", flush=True)
    try:
        webbrowser.open(url)
    except Exception:
        pass
    try:
        with server:
            server.serve_forever()
    except KeyboardInterrupt:
        pass
    print("已停止。")


if __name__ == "__main__":
    main()
