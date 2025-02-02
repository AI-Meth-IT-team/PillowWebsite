from flask import Flask, Response, request, jsonify
from flask_cors import CORS
import subprocess

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes


@app.route('/start-game', methods=['POST'])
def start_game():
    data = request.json

    # Validate the input data
    script_path = data.get('path')
    arguments = data.get('args', [])
    if not script_path:
        return jsonify({"error": "The 'path' field is required."}), 400

    # Combine script path and arguments into a single list
    command = ['sudo', '/usr/bin/python', script_path] + arguments

    def generate_output():
        try:
            # Start the subprocess
            process = subprocess.Popen(
                command,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )
            # Stream stdout
            for line in process.stdout:
                yield line
            # Stream stderr
            for line in process.stderr:
                yield f"ERROR: {line}"
        except Exception as e:
            yield f"ERROR: {str(e)}"

    return Response(generate_output(), content_type='text/plain')

@app.route('/favicon.ico')
def favicon():
    return '', 204

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)
