from flask import Flask, jsonify
import socket
import os
import logging
from datetime import datetime

# -------------------------------
# Configuration
# -------------------------------

APP_NAME = "Cloud Native DevSecOps App"
VERSION = os.getenv("APP_VERSION", "1.0.0")
PORT = int(os.getenv("PORT", 5000))

# -------------------------------
# Logging Configuration
# -------------------------------

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] [%(name)s] %(message)s"
)

logger = logging.getLogger(APP_NAME)

# -------------------------------
# Flask App Initialization
# -------------------------------

app = Flask(__name__)

startup_time = datetime.utcnow()

# -------------------------------
# Routes
# -------------------------------

@app.route("/")
def home():
    logger.info("Home endpoint accessed")

    return jsonify({
        "app": APP_NAME,
        "message": "Application is running successfully",
        "hostname": socket.gethostname(),
        "version": VERSION,
        "timestamp": datetime.utcnow().isoformat() + "Z"
    })


@app.route("/health")
def health():
    """
    Liveness probe
    """
    logger.info("Health check endpoint accessed")

    return jsonify({
        "status": "healthy"
    }), 200


@app.route("/readiness")
def readiness():
    """
    Readiness probe
    """
    uptime = (datetime.utcnow() - startup_time).total_seconds()

    logger.info("Readiness endpoint accessed")

    return jsonify({
        "status": "ready",
        "uptime_seconds": uptime
    }), 200


@app.route("/version")
def version():
    logger.info("Version endpoint accessed")

    return jsonify({
        "version": VERSION
    })


# -------------------------------
# Error Handling
# -------------------------------

@app.errorhandler(404)
def not_found(error):
    logger.warning("404 error occurred")
    return jsonify({"error": "Not Found"}), 404


@app.errorhandler(500)
def internal_error(error):
    logger.error("500 internal server error")
    return jsonify({"error": "Internal Server Error"}), 500


# -------------------------------
# Application Entry Point
# -------------------------------

if __name__ == "__main__":
    logger.info(f"Starting {APP_NAME} version {VERSION} on port {PORT}")
    app.run(host="0.0.0.0", port=PORT)
