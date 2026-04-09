from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # allows frontend to connect

# EMI Calculation Function
def calculate_emi(p, r, y):
    r = r / (12 * 100)   # monthly interest
    n = y * 12           # total months
    x = (1 + r) ** n

    emi = (p * r * x) / (x - 1)
    total = emi * n
    interest = total - p

    return emi, interest, total


# API Route
@app.route('/calculate', methods=['POST'])
def calculate():
    try:
        data = request.get_json()

        p = float(data['principal'])
        r = float(data['rate'])
        y = float(data['years'])

        emi, interest, total = calculate_emi(p, r, y)

        return jsonify({
            "emi": round(emi, 2),
            "interest": round(interest, 2),
            "total": round(total, 2)
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 400


# Home route (optional - to check server)
@app.route('/')
def home():
    return "EMI Calculator Backend is Running 🚀"


# Run server
if __name__ == "__main__":
    app.run(debug=True, port=5050)