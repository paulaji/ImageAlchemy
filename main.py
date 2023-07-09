from flask import Flask, render_template, request
app = Flask(__name__)

@app.route('/')
def home():
    return render_template("index.html")

@app.route('/edit', methods = ['GET', 'POST'])
def edit():
    if request.method == "POST":
        return "POST is now enabled, you can post your photos"
    return render_template('index.html')

app.run(debug=True, port = 5001)