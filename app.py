from flask import Flask, request, jsonify
from flask_cors import CORS
import joblib
from urllib.parse import urlparse

app = Flask(__name__)
CORS(app)

# Load model and vectorizer
model = joblib.load("model.pkl")
vectorizer = joblib.load("vectorizer.pkl")

# Keep a simple in-memory counter for dashboard
stats = {"safe": 0, "phishing": 0}


# Function to explain why a URL might be suspicious
def explain_url(url):
    reasons = []
    suspicious_keywords = ["login", "secure", "update", "account", "verify", "bank", "paypal"]
    unusual_tlds = [".xyz", ".top", ".info", ".online", ".ru", ".tk"]

    parsed = urlparse(url)

    # Keyword check
    if any(k in url.lower() for k in suspicious_keywords):
        reasons.append("Suspicious keyword in URL")

    # URL length check
    if len(url) > 75:
        reasons.append("URL is unusually long")

    # TLD check
    if parsed.hostname:
        tld = "." + parsed.hostname.split(".")[-1]
        if tld in unusual_tlds:
            reasons.append(f"Unusual TLD detected ({tld})")

    # Too many subdomains
    if parsed.hostname and parsed.hostname.count(".") > 3:
        reasons.append("Too many subdomains (possible obfuscation)")

    # HTTP instead of HTTPS
    if parsed.scheme == "http":
        reasons.append("Uses insecure HTTP instead of HTTPS")

    if not reasons:
        reasons.append("No obvious suspicious features detected")

    return reasons


@app.route("/check", methods=["POST"])
def check_url():
    data = request.json
    urls = data.get("urls", []) or [data.get("url", "")]

    results = []
    for u in urls:
        # Vectorize and predict
        u_vector = vectorizer.transform([u])
        pred = model.predict(u_vector)[0]
        result_text = "Phishing ❌" if pred == 1 else "Safe ✅"

        # Update stats
        if pred == 1:
            stats["phishing"] += 1
        else:
            stats["safe"] += 1

        # Explainability
        reasons = explain_url(u)

        results.append({"url": u, "prediction": result_text, "reasons": reasons})

    return jsonify({"results": results})


@app.route("/stats", methods=["GET"])
def get_stats():
    total = stats["safe"] + stats["phishing"]
    return jsonify({
        "total": total,
        "safe": stats["safe"],
        "phishing": stats["phishing"]
    })


if __name__ == "__main__":
    import os
    port = int(os.environ.get("PORT", 5000))
    app.run(debug=True, host="0.0.0.0", port=port)
