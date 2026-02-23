from generate_pdf import generate_portfolio_pdf
from flask import Flask, render_template, request, send_file
import requests
import json

app = Flask(__name__)

portfolios = {
    "portfolio_one": {
        "name": "Secure Growth",
        "description": "Designed for investors who prioritize capital protection over high returns. This portfolio focuses primarily on debt instruments, high quality bonds, and stable large-cap assets to generate steady and predictable income with minimal volatility. Ideal for short to medium term goals and risk averse investors.",
        "risk_level": "Low Risk",
        "expected_return": "7-9% annually",
        "allocation": [
            {"asset": "Debt Funds", "percent": 50, "example": "HDFC Short Term Debt Fund", "scheme_code": "100033"},
            {"asset": "Gold ETF", "percent": 30, "example": "Nippon India Gold ETF", "scheme_code": "135781"},
            {"asset": "Nifty 50 Index Fund", "percent": 20, "example": "UTI Nifty 50 Index Fund", "scheme_code": "120716"},
        ]
    },
    "portfolio_two": {
        "name": "Titan Growth",
        "description": "Built for long-term capital appreciation, this portfolio is heavily allocated to equities, including mid cap and high growth sectors. It aims for higher returns but may experience significant short term volatility.",
        "risk_level": "High Risk",
        "expected_return": "14-18% annually",
        "allocation": [
            {"asset": "Mid & Small Cap Funds", "percent": 60, "example": "Nippon India Small Cap Fund", "scheme_code": "118778"},
            {"asset": "Nifty 50 Index Fund", "percent": 30, "example": "Parag Parikh Flexi Cap Fund", "scheme_code": "122639"},
            {"asset": "Gold ETF", "percent": 10, "example": "SBI Gold ETF", "scheme_code": "135781"},
        ]
    }
}


def recommend_portfolio(risk):
    if risk == "low risk":
        return "portfolio_one"
    else:
        return "portfolio_two"


def get_fund_history(scheme_code):
    try:
        url = f"https://api.mfapi.in/mf/{scheme_code}"
        response = requests.get(url, timeout=5)
        data = response.json()
        nav_data = data["data"][:12]
        nav_data.reverse()
        labels = [item["date"] for item in nav_data]
        values = [float(item["nav"]) for item in nav_data]
        return labels, values
    except:
        return [], []


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/details")
def details():
    return render_template("details.html")


@app.route("/risk", methods=["GET", "POST"])
def risk():
    return render_template("risk.html", request=request)


@app.route("/result", methods=["POST"])
def result():
    name = request.form.get("name")
    age = request.form.get("age")
    occupation = request.form.get("occupation")
    risk_level = request.form.get("risk")

    portfolio_key = recommend_portfolio(risk_level)
    portfolio = portfolios[portfolio_key]

    main_fund = portfolio["allocation"][0]
    labels, values = get_fund_history(main_fund["scheme_code"])

    chart_data = {
        "labels": labels,
        "values": values,
        "fund_name": main_fund["example"]
    }

    return render_template(
        "result.html",
        name=name,
        age=age,
        occupation=occupation,
        risk=risk_level,
        portfolio=portfolio,
        chart_data=json.dumps(chart_data)
    )

@app.route("/download-pdf", methods=["POST"])
def download_pdf():
    name = request.form.get("name")
    age = request.form.get("age")
    occupation = request.form.get("occupation")
    risk = request.form.get("risk")
    portfolio_key = recommend_portfolio(risk)
    portfolio = portfolios[portfolio_key]
    pdf_buffer = generate_portfolio_pdf(name, age, occupation, risk, portfolio)
    return send_file(pdf_buffer, as_attachment=True, download_name=f"PortfolioIQ_{name}.pdf", mimetype="application/pdf")


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)