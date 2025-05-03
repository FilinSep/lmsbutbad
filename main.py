from flask import *

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('home_page.html')

app.run()