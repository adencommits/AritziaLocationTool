from flask import Flask
from views import views

app = Flask(__name__)
app.register_blueprint(views, url_prefix='/views')

@app.route('/')  # Make sure the decorator is directly above the function
def home():
    return 'Hello, World!'

if __name__ == '__main__':
    app.run(debug=True)