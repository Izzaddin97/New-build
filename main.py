import socket
import threading
import time
import logging
from flask import Flask, render_template, jsonify, request
import os
import OpenAI
# The original erroneous line was likely a mistake.
# Set up OpenAI client
api_key = os.environ['OPENAI_API_KEY']
organization_id = os.environ.get('OPENAI_ORG_ID')  # Optional
client = OpenAI(api_key=api_key, organization=organization_id)

# Flask app for web interface
app = Flask(__name__)

@app.route('/chat', methods=['POST'])
def chat_with_ai():
    data = request.get_json()
    user_input = data.get('message', '')

    if not user_input:
        return jsonify({'error': 'No message provided'}), 400

    try:
        # Generate a response using OpenAI
        response = client.Completions.create(
            engine="text-davinci-003",
            prompt=user_input,
            max_tokens=150
        )
        
        ai_response = response.choices[0].text.strip()
        return jsonify({'response': ai_response})
    except Exception as e:
        logging.error(f"Error communicating with OpenAI: {e}")
        return jsonify({'error': 'Failed to get response from AI'}), 500

# Configure logging
logging.basicConfig(level=logging.INFO, format='[%(asctime)s] %(message)s', datefmt='%Y-%m-%d %H:%M:%S')

vpn_server_instance = None
server_logs = []

class LogHandler(logging.Handler):
    def emit(self, record):
        global server_logs
        log_message = self.format(record)
        server_logs.append(log_message)
        if len(server_logs) > 100:  # Keep only last 100 logs
            server_logs = server_logs[-100:]

# Add custom log handler
log_handler = LogHandler()
log_handler.setFormatter(logging.Formatter('[%(asctime)s] %(message)s', datefmt='%H:%M:%S'))
logging.getLogger().addHandler(log_handler)

class VPNServer:
    def __init__(self, host='0.0.0.0', port=5000):
        self.host = host
        self.port = port
        self.running = False
        self.clients = []
        # Use Cloudflare DNS servers
        self.dns_servers = ['1.1.1.1', '1.0.0.1']
        self.fast_mode_enabled = True
        
    # other methods remain unchanged

@app.route('/')
def index():
    return render_template('index.html', server_host='0.0.0.0', server_port=5001)

# other routes remain unchanged

def main():
    print("FastVPN - Android VPN Server with Web GUI")
    print("=========================================")
    print("Web interface: http://0.0.0.0:5000")
    print("VPN server will run on port 5001")
    
    # Start Flask web interface
    app.run(host='0.0.0.0', port=5000, debug=False)
 
    # Check if the input message is empty
    if not user_input:
        return jsonify({'error': 'No message provided'}), 400

    try:
        # Generate a response using OpenAI
        response = client.Completions.create(
            engine="text-davinci-003",  # specify the engine you want to use
            prompt=user_input,
            max_tokens=150
        )
        
        ai_response = response.choices[0].text.strip()
        return jsonify({'response': ai_response})
    except Exception as e:
        logging.error(f"Error cocommunicatingith OpenAI: {e}")
        return jsonify({'error': 'Failed to get response from AI'}), 500  
        
# add error responsefunction sendMessage() {

fetch('/chat', {
method: 'POST',
headers: {
'Content-Type': 'application/json'
        },
        body: JSON.stringify({message: userInput})
    })
    .then(response => response.json())
    .then(data => {
        if (data.response) {
            addLog(`AI: ${data.response}`);
        } else { addLog(`Error: ${data.error || 'Failed to receive response'}`);
"/home/runner/workspace/main.py" }<input type="text" id="userInput" placeholder="Type your message here">}
    .
catch(error => {
        console.error('Error communicating with AI:', error);
        addLog('Error communicating with AI');
    });
<button onclick="sendMessage()">Send</button>
<div id="logContainer" class="log-container">
    <!-- Logs will appear here -->
</div>body {
    font-family: 'Roboto', sans-serif;
    color: white;
    overflow-x: hidden;

        server_logs.append(log_message)
        if len(server_logs) > 100:  # Keep only last 100 logs
            server_logs = server_logs[-100:]

# Add custom log handler
log_handler = LogHandler()
log_handler.setFormatter(logging.Formatter('[%(asctime)s] %(message)s', datefmt='%H:%M:%S'))
logging.getLogger().addHandler(log_handler)

class VPNServer:
    def __init__(self, host='0.0.0.0', port=5000):
        self.host = host
        self.port = port
        self.running = False
        self.clients = []
        # Use Cloudflare DNS servers
        self.dns_servers = ['1.1.1.1', '1.0.0.1']
        self.fast_mode_enabled = True
        
    def start(self):
        """Start the VPN server"""
        try:
            self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            
            # Set keepalive options (fix for the previous error)
            self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_KEEPALIVE, 1)
            
            # Bind and listen
            self.server_socket.bind((self.host, self.port))
            self.server_socket.listen(5)
            self.running = True
            
            logging.info(f"VPN Server started on {self.host}:{self.port}")
            logging.info(f"Using DNS servers: {', '.join(self.dns_servers)}")
            logging.info("Fast mode available for Android clients")
            
            # Accept connections
            while self.running:
                try:
                    client_socket, addr = self.server_socket.accept()
                    logging.info(f"New connection from {addr}")
                    
                    # Handle client in separate thread
                    client_thread = threading.Thread(
                        target=self.handle_client,
                        args=(client_socket, addr)
                    )
                    client_thread.daemon = True
                    client_thread.start()
                    
                except socket.error as e:
                    if self.running:
                        logging.error(f"Socket error: {e}")
                    break
                    
        except Exception as e:
            logging.error(f"Server error: {e}")
        finally:
            self.stop()
    
    def handle_client(self, client_socket, addr):
        """Handle individual client connections"""
        try:
            # Send DNS configuration to client
            dns_config = {
                'primary_dns': self.dns_servers[0],
                'secondary_dns': self.dns_servers[1],
                'fast_mode': self.fast_mode_enabled
            }
            
            # Send welcome message with DNS config
            welcome_msg = f"VPN Connected! DNS: {dns_config['primary_dns']}, Fast Mode: {dns_config['fast_mode']}\n"
            client_socket.send(welcome_msg.encode())
            
            self.clients.append(client_socket)
            
            # Keep connection alive
            while self.running:
                try:
                    data = client_socket.recv(1024)
                    if not data:
                        break
                    
                    # Echo back for testing
                    response = f"Received: {data.decode()}\n"
                    client_socket.send(response.encode())
                    
                except socket.error:
                    break
                    
        except Exception as e:
            logging.error(f"Client handler error: {e}")
        finally:
            if client_socket in self.clients:
                self.clients.remove(client_socket)
            client_socket.close()
            logging.info(f"Client {addr} disconnected")
    
    def stop(self):
        """Stop the VPN server"""
        self.running = False
        for client in self.clients:
            client.close()
        if hasattr(self, 'server_socket'):
            self.server_socket.close()
        logging.info("Server stopped")

@app.route('/')
def index():
    return render_template('index.html', server_host='0.0.0.0', server_port=5001)

@app.route('/start_server', methods=['POST'])
def start_server():
    global vpn_server_instance
    try:
        if vpn_server_instance is None or not vpn_server_instance.running:
            vpn_server_instance = VPNServer(port=5001)  # Use port 5001 for VPN
            server_thread = threading.Thread(target=vpn_server_instance.start)
            server_thread.daemon = True
            server_thread.start()
            time.sleep(1)  # Give it time to start
            return jsonify({'success': True, 'message': 'Server started'})
        else:
            return jsonify({'success': False, 'message': 'Server already running'})
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)})

@app.route('/stop_server', methods=['POST'])
def stop_server():
    global vpn_server_instance
    try:
        if vpn_server_instance and vpn_server_instance.running:
            vpn_server_instance.stop()
            vpn_server_instance = None
            return jsonify({'success': True, 'message': 'Server stopped'})
        else:
            return jsonify({'success': False, 'message': 'Server not running'})
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)})

@app.route('/get_logs')
def get_logs():
    return jsonify({'logs': server_logs[-20:]})  # Return last 20 logs

@app.route('/get_status')
def get_status():
    client_count = 0
    if vpn_server_instance:
        client_count = len(vpn_server_instance.clients)
    return jsonify({
        'running': vpn_server_instance.running if vpn_server_instance else False,
        'client_count': client_count
    })

def main():
    print("FastVPN - Android VPN Server with Web GUI")
    print("=========================================")
    print("Web interface: http://0.0.0.0:5000")
    print("VPN server will run on port 5001")
    
    # Start Flask web interface
    app.run(host='0.0.0.0', port=5000, debug=False)

if __name__ == "__main__":
    main()
