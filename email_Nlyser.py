from flask import Flask, request, jsonify, render_template
import re

app = Flask(__name__)

def analyze_header(header_text):
    results = {
        "spoofed_domain": False,
        "missing_dkim": False,
        "missing_spf": False,
        "missing_dmarc": False,
        "from_vs_return_path_mismatch": False
    }

    if "dkim=fail" in header_text.lower() or "dkim=none" in header_text.lower():
        results["missing_dkim"] = True
    if "spf=fail" in header_text.lower() or "spf=none" in header_text.lower():
        results["missing_spf"] = True
    if "dmarc=fail" in header_text.lower() or "dmarc=none" in header_text.lower():
        results["missing_dmarc"] = True

    from_match = re.search(r"From:.*?<([^>]+)>", header_text)
    return_path_match = re.search(r"Return-Path:.*?<([^>]+)>", header_text)

    if from_match and return_path_match:
        if from_match.group(1).split('@')[-1] != return_path_match.group(1).split('@')[-1]:
            results["from_vs_return_path_mismatch"] = True
            results["spoofed_domain"] = True

    return results

@app.route("/", methods=["GET", "POST"])
def home():
    if request.method == "POST":
        header = request.form["header"]
        result = analyze_header(header)
        return render_template("result.html", result=result)
    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True)
