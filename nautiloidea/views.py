from nautiloidea import app
from flask import request, render_template

@app.route('/register', methods=["POST", "GET"]):
def register_users():
    if request.method == 'GET':
        return render_template("")
    elif request.method == 'POST':
        return render_template()


