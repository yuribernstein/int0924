from flask import Flask
app = Flask(__name__)  # __name__ helps Flask locate resources and configurations

@app.route('/', methods=['GET'])
def home():
    return "Welcome to my Flask app!"

@app.route('/text')
def text_response():
    return "This is a plain text response."

@app.route('/json')
def json_response():
    return {"message": "This is a JSON response"}, 200  # JSON response with status code

from flask import request

@app.route('/submit', methods=['POST'])
def submit_data():
    data = request.get_json()  # Parse JSON payload
    return {"received": data}, 200

@app.route('/user/<username>')
def greet_user(username):
    return f"Hello, {username}!"

@app.route('/search')
def search():
    query = request.args.get('query')  # Retrieves ?query=value
    return f"Search results for: {query}"

@app.route('/check')
def check_headers():
    user_agent = request.headers.get('User-Agent')
    return f"User-Agent: {user_agent}"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)
