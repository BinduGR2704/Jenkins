from flask import Flask, render_template, request

app = Flask(__name__)

# Home route (shows form)
@app.route('/')
def home():
    return render_template('index.html')

# Handle form submission
@app.route('/submit', methods=['POST'])
def submit():
    name = request.form['name']
    email = request.form['email']

    return f"Hello {name}, your email is {email}"

if __name__ == '__main__':
    app.run(debug=True)