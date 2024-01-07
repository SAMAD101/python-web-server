import tornado.web
import tornado.ioloop
from tornado.web import Application, RequestHandler


class MainHandler(RequestHandler):
    def get(self) -> None:
        self.write("Hello, world")


if __name__ == "__main__":
    app: Application = Application(
        [
            (r"/", MainHandler),
        ]
    )
    app.listen(8888)
    print("Server listening on port 8888")
    tornado.ioloop.IOLoop.current().start()
