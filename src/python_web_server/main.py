import asyncio
import json

from argparse import ArgumentParser, Namespace

from tornado.web import Application, RequestHandler, StaticFileHandler

from typing import Tuple


class MainHandler(RequestHandler):
    def get(self) -> None:
        self.write("Hello, world")


class ListHandler(RequestHandler):
    def get(self) -> None:
        self.render("index.html")


class QueryParamHandler(RequestHandler):
    def get(self) -> None:
        num = self.get_argument("num")
        if num.isdigit():
            r = "odd" if int(num) % 2 else "even"
            self.write(f"{num} is {r}")


class ResourceParamHandler(RequestHandler):
    def get(self, studentName, studentID) -> None:
        self.write(f"Hello {studentName} with id {studentID}")


class AnotherListHandler(RequestHandler):
    def get(self) -> None:
        with open("list.txt", "r") as f:
            chars = f.read().splitlines()
        self.write(json.dumps(chars))

    def post(self) -> None:
        char = self.get_argument("char")
        with open("list.txt", "a") as f:
            f.write(f"{char}\n")
        self.write(json.dumps({"success": True}))


class CharacterAdderHandler(RequestHandler):
    def get(self) -> None:
        self.render("list.html")

    def post(self) -> None:
        char = self.get_argument("char")
        with open("list.txt", "a") as f:
            f.write(f"{char}\n")
        self.write(
            json.dumps({"success": True, "message": "Character added successfully!"})
        )


class UploadHandler(RequestHandler):
    def get(self) -> None:
        self.render("upload.html")

    def post(self) -> None:
        files = self.request.files["img_file"]
        for f in files:
            with open(f"media/img/{f.filename}", "wb") as img:
                img.write(f.body)
        self.write(f"localhost:8888/img/{f.filename}")


async def main(port: int) -> None:
    handlers: List[Tuple[str, RequestHandler]] = [
        (r"/", MainHandler),
        (r"/cat", ListHandler),
        (r"/isEven", QueryParamHandler),
        (r"/students/([A-Za-z]+)/([0-9]+)", ResourceParamHandler),
        (r"/list", AnotherListHandler),
        (r"/addChar", CharacterAdderHandler),
        (r"/upload", UploadHandler),
        (r"/img/(.*)", StaticFileHandler, {"path": "media/img"}),
    ]
    app: Application = Application(handlers, template_path="templates")
    app.listen(port)
    print("Server listening on port 8888")
    await asyncio.Event().wait()


if __name__ == "__main__":
    parser: ArgumentParser = ArgumentParser()
    parser.add_argument("port", help="Select Port")
    args: Namespace = parser.parse_args()
    asyncio.run(main(args.port))
