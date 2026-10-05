from flask import Flask, render_template
from Database.DBUncompress import uncompressDB
app = Flask(__name__)

@app.route('/')
def Start():
    return render_template("home.html", loadingInfo = "Hello ...")

if(__name__ == "__main__"):
    uncompressDB()
    app.run()

