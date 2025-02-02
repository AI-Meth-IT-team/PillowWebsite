from flask import Flask, jsonify, send_from_directory
from flask_cors import CORS
import asyncio
import websockets
import os
from datetime import datetime
import logging
from threading import Thread
from threading import Thread, Lock  # Add Lock here
import time
from collections import defaultdict

# Add this global variable after message_queues
reaction_times = defaultdict(dict)  # {client_id: {"start": float, "end": float}}
# Konfiguracja
SERVER_IP = "192.168.4.1"
HTTP_PORT = 5000
WS_PORT = 8080
STATIC_DIR = "/home/integralsenso/Desktop/repo/PillowWebsite/WebSite/"
LOG_FILE = None

def startLog():
    """Initialize logging and create a log file."""
    global LOG_FILE
    print("Log files process")
    LOG_DIR = "/home/integralsenso/Desktop/logs"
    os.makedirs(LOG_DIR, exist_ok=True)
    log_file_name = f"log_{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.log"
    LOG_FILE = os.path.join(LOG_DIR, log_file_name)
    print(f"Log file created: {LOG_FILE}")

def logInf(msg):
    """Log information to both the console and the log file."""
    dateTime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    formatted_msg = f"INF {dateTime}.{datetime.now().microsecond // 1000:03d} {msg}"
    print(formatted_msg)
    
    if LOG_FILE:
        with open(LOG_FILE, "a") as f:
            f.write(formatted_msg + "\n")

# Konfiguracja aplikacji Flask
app = Flask(__name__, static_folder=STATIC_DIR)
CORS(app)

# Konfiguracja logowania
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Global variables for thread safety
main_event_loop = None
loop_lock = Lock()  # Add this line

# WebSocket configuration
clients = []
message_queues = {}

# Routing dla statycznych plików
@app.route('/')
def serve_index():
    return send_from_directory(STATIC_DIR, 'index.html')

@app.route('/<path:path>')
def serve_static(path):
    return send_from_directory(STATIC_DIR, path)

# Game endpoints
@app.route('/start-game', methods=['POST'])
def start_game():
    logger.info(f"Aktualna liczba połączonych klientów: {len(clients)}")
    
    if len(clients) < 3:
        return jsonify({"error": f"Za mało graczy! Potrzeba co najmniej 3. Aktualnie: {len(clients)}"}), 400

    try:
        global main_event_loop, loop_lock  # Add this line
        with loop_lock:
            if main_event_loop is None:
                logger.error("Main event loop not initialized!")
                return jsonify({"error": "Server not ready"}), 500

            # Schedule game_loop in the main event loop
            asyncio.run_coroutine_threadsafe(game_loop(), main_event_loop)
            logger.info("Game loop started successfully")
        
        return jsonify({"status": "Gra rozpoczęta!"}), 200
    except Exception as e:
        logger.error(f"Error starting game: {e}")
        return jsonify({"error": str(e)}), 500


# WebSocket handlers
async def handler(websocket):
    clients.append(websocket)
    message_queues[websocket] = asyncio.Queue()
    logger.info(f"New client connected: {websocket.remote_address}")
    logInf(f"Total clients: {len(clients)}")

    try:
        async for message in websocket:
            logger.info(f"Received message from {websocket.remote_address}: {message}")
            await message_queues[websocket].put(message)
    except websockets.exceptions.ConnectionClosed as e:
        logger.info(f"Connection closed: {websocket.remote_address}, {e}")
    finally:
        clients.remove(websocket)
        del message_queues[websocket]
        logInf(f"Client disconnected. Total clients: {len(clients)}")

async def game_loop():
    logInf("Game loop started (one round with timing).")
    current_clients = list(clients)
    
    for client_index, client in enumerate(current_clients):
        try:
            client_id = f"{client.remote_address[0]}:{client.remote_address[1]}"
            
            # Record start time
            reaction_times[client_id]["start"] = time.time()
            
            await client.send("TURN_ON")
            logInf(f"Sent TURN_ON to {client_id}")

            try:
                message = await asyncio.wait_for(message_queues[client].get(), timeout=30)
                if message == "BUTTON_PRESSED":
                    # Record end time and calculate reaction time
                    reaction_times[client_id]["end"] = time.time()
                    reaction_time = reaction_times[client_id]["end"] - reaction_times[client_id]["start"]
                    reaction_times[client_id]["reaction"] = round(reaction_time, 3)
                    
                    logInf(f"{client_id} reaction: {reaction_time:.3f}s")
            except asyncio.TimeoutError:
                logInf(f"Timeout for {client_id}")
                reaction_times[client_id]["reaction"] = None

        except Exception as e:
            logInf(f"Error with client {client_id}: {str(e)}")
            continue

    logInf("One round completed with timing data collected")

# Add this new endpoint
@app.route('/get-times', methods=['GET'])
def get_times():
    simplified = {
        client: data["reaction"] 
        for client, data in reaction_times.items()
        if "reaction" in data and data["reaction"] is not None
    }
    return jsonify({
        "times": simplified,
        "stats": {
            "average": sum(simplified.values())/len(simplified) if simplified else 0,
            "max": max(simplified.values()) if simplified else 0,
            "min": min(simplified.values()) if simplified else 0
        }
    })

async def run_websocket_server():
    logger.info(f"Starting WebSocket server on ws://{SERVER_IP}:{WS_PORT}")
    async with websockets.serve(handler, SERVER_IP, WS_PORT):
        await asyncio.Future()  # Run the server until it's stopped

def run_flask():
    app.run(host='192.168.4.1', port=HTTP_PORT, debug=True, use_reloader=False)

async def main():
    global main_event_loop
    main_event_loop = asyncio.get_running_loop()  # This captures the correct event loop
    
    # Start WebSocket server
    logger.info(f"Starting WebSocket server on ws://{SERVER_IP}:{WS_PORT}")
    async with websockets.serve(handler, SERVER_IP, WS_PORT):
        # Start Flask in a separate thread
        flask_thread = Thread(target=run_flask)
        flask_thread.daemon = True
        flask_thread.start()
        
        await asyncio.Future()  # Run indefinitely

if __name__ == "__main__":
    startLog()
    asyncio.run(main())