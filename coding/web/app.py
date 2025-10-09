from flask import Flask, render_template



app = Flask(__name__)

@app.route('/')
def home():
    return render_template('main.html')


def main():
    app.run(host='0.0.0.0', port=8080, debug=True)

if __name__ == '__main__':
    main()



    