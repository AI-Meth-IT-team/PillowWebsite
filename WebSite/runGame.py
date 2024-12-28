from flask import Flask, request, jsonify
import subprocess

app = Flask(__name__)

@app.route('/run-python', methods=['POST'])
def run_python_script():
    data = request.json
    script_path = data.get('path')
    arguments = data.get('args', [])

    try:
        result = subprocess.run(
            ['python3', script_path, *arguments],
            text=True,
            capture_output=True,
            check=True
        )
        return jsonify({'output': result.stdout})
    except subprocess.CalledProcessError as e:
        return jsonify({'error': e.stderr}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
