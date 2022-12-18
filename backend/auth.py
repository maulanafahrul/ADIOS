from flask import Blueprint , render_template, request, jsonify, redirect, url_for, flash, session
from db import db
from werkzeug.security import generate_password_hash, check_password_hash

authapp = Blueprint('authapp', __name__)

from functools import wraps

def login_required(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        if 'user' in session:
            return f(*args, **kwargs)
        else:
            flash('Anda harus login', 'danger')
            return redirect(url_for('authapp.login'))
    return wrapper

@authapp.route('/login', methods=['POST', 'GET'])
def login():
    # ambil data dari form
    if request.method == 'POST':
        data = {
            'username': request.form['username']
        }
    # lakukan pengecekan user 
        user = {}
        user_ref = db.collection('users').where('username', '==', data['username']).stream()
        for ur in user_ref:
            user = ur.to_dict()

        if user:
            if check_password_hash(user['password'], request.form['password']):
                session['user'] = user
                flash('Berhasil Login!', 'success')
                return redirect(url_for('mhsapp.mahasiswa'))
                # return jsonify(session['user'])
                
        flash('salah!', 'danger')
        return redirect(url_for('authapp.login'))
    
    if 'user' in session:
        return redirect(url_for('mhsapp.mahasiswa'))
    return render_template('login.html')

@authapp.route('/register', methods=['POST', 'GET'])
def register():
    if request.method == 'POST':
        # mengambil data
        data = {
            'nama_lengkap': request.form['nama_lengkap'],
            'username': request.form['username'],
            'email': request.form['email'],
            'role': 'admin'
        }
        # pengecekan pass 
        if request.form['password'] != request.form['password_1']:
            flash('Password Tidak Sama!', 'danger')
            redirect(url_for('authapp.register'))
        
        if len(request.form['password']) <= 5:
            flash('Password Harus Lebih Dari 5!', 'danger')
            return redirect(url_for('authapp.register'))
        
        data['password'] = generate_password_hash( request.form['password'], 'sha256')
        # cek username
        user = {}
        user_ref = db.collection('users').where('username', '==', data['username']).stream()
        for ur in user_ref:
            user = ur.to_dict()
        if user:
            flash('Username sudah ada!', 'danger')
            return redirect(url_for('authapp.register'))
        # masukan ke database
        db.collection('users').document().set(data)
        # flash
        flash('Register Berhasil!', 'success')
        # kembali ke halaman login
        return redirect(url_for('authapp.login'))
    return render_template('register.html')


@authapp.route('/logout')
def logout():
    session.clear()
    flash('Anda Berhasil Keluar!', 'danger')
    return redirect(url_for('authapp.login'))