from flask import Flask, request, jsonify, render_template

# Initialize Flask app
app = Flask(__name__)

# Configure logging
@app.route('/<filename>')
def static_file(filename):
    return app.send_static_file(filename)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/js')
def jsindex():
    return render_template('jsindex.html')

# Run the Flask app
if __name__ == '__main__':
    app.run(port=8080)
