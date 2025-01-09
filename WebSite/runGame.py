from flask import Flask, Response, request
import subprocess

app = Flask(__name__)

@app.route('/start-game', methods=['POST'])
def start_game():
    data = request.json
    script_path = data.get('path')
    arguments = data.get('args', [])
    
    def generate_output():
        # Uruchom proces i czytaj dane w czasie rzeczywistym
        process = subprocess.Popen(
            ['python3', script_path, *arguments],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        
        # Czytaj stdout w czasie rzeczywistym i zwracaj każdą linię
        for line in process.stdout:
            yield line  # Wysyłanie każdej linii do klienta
        
        # Po zakończeniu procesu zwróć ewentualne błędy
        for line in process.stderr:
            yield f"ERROR: {line}"

    return Response(generate_output(), content_type='text/plain')
