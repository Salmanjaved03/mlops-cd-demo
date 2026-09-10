import os
import subprocess
from flask import Flask, jsonify, request

app = Flask(__name__)

APPLICATION_VERSION = "1.3.0"
MODEL_VERSION = "model-7"

def get_git_commit():
    commit = os.environ.get("GIT_COMMIT")
    if not commit:
        try:
            commit = subprocess.check_output(
                ["git", "rev-parse", "--short", "HEAD"]
            ).decode("ascii").strip()
        except Exception:
            commit = "unknown"
    return commit

@app.route("/")
def home():
    return jsonify({
        "service": "mlops-demo",
        "status": "running"
    })

@app.route("/health")
def health():
    return jsonify({
        "application_version": APPLICATION_VERSION,
        "model_version": MODEL_VERSION,
        "git_commit": get_git_commit(),
        "status": "healthy"
    })

@app.route("/predict", methods=["POST"])
def predict():
    data = request.get_json()
    value = float(data["value"])
    # Dummy ML prediction for teaching
    prediction = value * 2
    return jsonify({
        "input": value,
        "prediction": prediction,
        "model_version": MODEL_VERSION,
        "application_version": APPLICATION_VERSION
    })

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
