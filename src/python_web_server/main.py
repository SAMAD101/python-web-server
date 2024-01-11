import asyncio
import json

from tornado.web import Application, RequestHandler

from typing import List, Tuple


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


async def main() -> None:
    handlers: List[Tuple[str, RequestHandler]] = [
        (r"/", MainHandler),
        (r"/cat", ListHandler),
        (r"/isEven", QueryParamHandler),
        (r"/students/([A-Za-z]+)/([0-9]+)", ResourceParamHandler),
        (r"/list", AnotherListHandler),
    ]
    app: Application = Application(handlers, template_path="templates")
    app.listen(8888)
    print("Server listening on port 8888")
    await asyncio.Event().wait()


if __name__ == "__main__":
    asyncio.run(main())
