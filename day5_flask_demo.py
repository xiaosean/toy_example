from flask import Flask
app = Flask(__name__)

@app.route("/test")
def abc():
# check 127.0.0.1:5000/test
    return "In test page"


@app.route("/")
def hello():
# check 127.0.0.1:5000
    return "Hello World!"

if __name__ == "__main__":
    app.run()