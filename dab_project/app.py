from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

NAfrekvens = 96

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/settFrekvens', methods=['POST'])
def settFrekvens():
    global NAfrekvens
    frequency = request.json['frequency']
    NAfrekvens = frequency
    return jsonify({"status": "Frekvens mottatt", "frequency": NAfrekvens})

@app.route('/FAfrekvens', methods=['GET'])
def FAfrekvens():
    return jsonify({"frequency": NAfrekvens})

if __name__ == '__main__':
    app.run(debug=True)
