from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/', methods=['POST']) 
def foo():
    data = request.json
    return jsonify(data)


app.run(port=5050)