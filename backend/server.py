import json
import os
from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import urlparse

from openai import OpenAI


CLIENT = OpenAI(
    api_key=os.getenv("DASHSCOPE_API_KEY"),
    base_url=os.getenv("DASHSCOPE_BASE_URL", "https://dashscope.aliyuncs.com/compatible-mode/v1"),
)

DEFAULT_VISION_MODEL = os.getenv("QWEN_VISION_MODEL", "qwen3-vl-plus")


def json_response(handler, status, payload):
    body = json.dumps(payload, ensure_ascii=False).encode("utf-8")
    handler.send_response(status)
    handler.send_header("Content-Type", "application/json; charset=utf-8")
    handler.send_header("Access-Control-Allow-Origin", "*")
    handler.send_header("Access-Control-Allow-Methods", "POST, OPTIONS")
    handler.send_header("Access-Control-Allow-Headers", "Content-Type, Authorization")
    handler.send_header("Content-Length", str(len(body)))
    handler.end_headers()
    handler.wfile.write(body)


def read_json(handler):
    length = int(handler.headers.get("Content-Length", "0") or "0")
    if length == 0:
        return {}
    return json.loads(handler.rfile.read(length).decode("utf-8"))


def build_vision_messages(prompt, image_urls):
    content = []
    for url in image_urls:
        content.append({"type": "image_url", "image_url": {"url": url}})
    content.append({"type": "text", "text": prompt})
    return [{"role": "user", "content": content}]


class Handler(BaseHTTPRequestHandler):
    def do_OPTIONS(self):
        self.send_response(204)
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type, Authorization")
        self.end_headers()

    def do_POST(self):
        path = urlparse(self.path).path
        try:
            data = read_json(self)
        except Exception as exc:
            json_response(self, 400, {"error": f"Invalid JSON: {exc}"})
            return

        if path == "/api/vision":
            prompt = data.get("prompt", "请用一句话描述图像中的场景。")
            image_urls = data.get("image_urls") or []
            model = data.get("model", DEFAULT_VISION_MODEL)
            if not image_urls:
                json_response(self, 400, {"error": "image_urls is required"})
                return
            completion = CLIENT.chat.completions.create(
                model=model,
                messages=build_vision_messages(prompt, image_urls),
            )
            json_response(self, 200, {"output": completion.choices[0].message.content})
            return

        json_response(self, 404, {"error": "Not Found"})


def main():
    host = os.getenv("HOST", "0.0.0.0")
    port = int(os.getenv("PORT", "8000"))
    server = HTTPServer((host, port), Handler)
    print(f"Backend listening on http://{host}:{port}")
    server.serve_forever()


if __name__ == "__main__":
    main()
