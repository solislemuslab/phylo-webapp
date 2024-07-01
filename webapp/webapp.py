from flask import Flask, render_template, redirect, url_for, request, session
from julia import Main

Main.eval("using CSV")
Main.eval("using DataFrames")
Main.eval("using QuartetNetworkGoodnessFit")
Main.eval("using PhyloNetworks")
Main.eval("using Plots")

app = Flask(__name__)
app.secret_key = "hello"

@app.route("/")
def home():
    return render_template('home.html')

@app.route("/upload", methods = ["POST", "GET"])
def upload():
    if request.method == "POST":
        data = request.form["dt"]
        session["data"] = data
        return redirect(url_for("data"))
    else:
        return render_template("data_upload.html")

@app.route("/data")
def data():
    if "data" in session:
        data = session["data"]
        return f"<h1>{data}</h1>"
    else:
        return redirect(url_for("upload"))

@app.route("/clustering")
def clustering():
    return "This is the clustering page."

@app.route("/goodness")
def goodness():    
    return render_template('goodness.html', title = "Goodness-of-fit")

# define a route to handle the parameters
@app.route("/process", methods = ["POST"])
def process():
    parameters = request.form['parameter']
    return redirect(url_for("goodness"))

if __name__ == "__main__":
    app.run(debug = True)
