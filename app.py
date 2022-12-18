from flask import Flask , render_template, request, jsonify, redirect, url_for, flash, session
from db import db
from werkzeug.security import generate_password_hash, check_password_hash
from backend.auth import authapp
from backend.mahasiswa import mhsapp
from backend.jurusan import jurusanapp
from backend.absensi import absenapp

app = Flask(__name__, static_folder='static', static_url_path='')
app.secret_key = 'afa 1ya'

app.register_blueprint(authapp)
app.register_blueprint(mhsapp)
app.register_blueprint(jurusanapp)
app.register_blueprint(absenapp)

@app.route('/')
def index():
    return render_template('index.html')




# @app.route('/cek_session')
# def cek_session():
#     return jsonify(session['user'])


if __name__ == '__main__':
    app.run(debug=True)