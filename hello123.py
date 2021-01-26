from flask import Flask
server = Flask(name)


@server.route("/")
def hello():
    return "Hello Kritsadeeka "


if name == "main":
    server.run(host='0.0.0.0', port=80)
