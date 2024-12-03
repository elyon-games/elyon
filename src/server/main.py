from flask import Flask, request
global app

def Main(config, options):
    global app
    print("Start Server...")
    app = Flask(f"Elyon Server ({__name__})")
    initRoute()
    app.run(host="0.0.0.0", port=3300)

def initRoute():
    global app
    @app.route("/")
    def test():
        return "sa"