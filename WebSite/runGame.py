from flask import Flask, request, jsonify
import subprocess

app = Flask(__name__)

@app.route('/start-game', methods=['POST'])
def start_game():
    data = request.json
    script_path = data.get('path')  # Ścieżka do skryptu Python
    arguments = data.get('args', [])  # Lista argumentów

    try:
        # Uruchomienie skryptu Python w subprocess
        result = subprocess.run(
            ['python3', script_path, *arguments],
            text=True,
            capture_output=True,
            check=True
        )
        # Zwrócenie wyników skryptu
        return jsonify({'status': 'completed', 'output': result.stdout})
    except subprocess.CalledProcessError as e:
        # Zwrotka w przypadku błędu
        return jsonify({'status': 'error', 'error': e.stderr}), 500


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
