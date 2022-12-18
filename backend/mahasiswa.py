from flask import Blueprint , render_template, request, jsonify, redirect, url_for, flash, session
from db import db, get_all_collection, storage
from werkzeug.security import generate_password_hash, check_password_hash
from backend.auth import login_required

mhsapp = Blueprint('mhsapp', __name__)

@mhsapp.route('/mahasiswa')
@login_required
def mahasiswa():
    # cek session
    daftar_mahasiswa = []
    # mengambil smua data dari collection 
    mahasiswa_ref = db.collection('mahasiswa').stream()
    # melakukan looping
    for mr in mahasiswa_ref:
        mhs = mr.to_dict()
        mhs['id'] = mr.id
    # menampilkan ke halaman
        daftar_mahasiswa.append(mhs)
    return render_template('mahasiswa.html', data=daftar_mahasiswa)

@mhsapp.route('/mahasiswa/delete/', methods=['POST'])
@login_required
def hapus_data():
    if request.method == 'POST':
        uid = request.form.get('uid')
        # menghapus data pada collection 
        db.collection('mahasiswa').document(uid).delete()
        # kembali ke halaman mahasiswa
        flash('Berhasil Menghapus Data Baru!', 'danger')
        return redirect(url_for('.mahasiswa'))
@mhsapp.route('/mahasiswa/<uid>')
@login_required
def detail(uid):
    mhs = db.collection('mahasiswa').document(uid).get().to_dict()
    return render_template('detail.html', data=mhs)

@mhsapp.route('/mahasiswa/tambah', methods=['POST', 'GET'])
@login_required
def tambah_data():
    if request.method == 'POST':
        #mengambil data dari front end 
        data = {
            'nama_lengkap': request.form['nama_lengkap'],
            'nim': request.form['nim'],
            'jurusan': request.form['jurusan'],
            'tgl_lahir': request.form['tgl_lahir'],
            'email': request.form['email'],
            'role': 'mahasiswa',
            'is_active': True
        }
        # kondisi foto
        if 'foto' in request.files and request.files['foto']:
            image = request.files['foto']
            ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}
            filename = image.filename
            lokasi = f"profil/{filename}"
            ext = filename.rsplit('.', 1)[1].lower()
            if ext in ALLOWED_EXTENSIONS:
                storage.child(lokasi).put(image)
                data['foto'] = storage.child(lokasi).get_url(None)
            else:
                flash("Foto tidak diperbolehkan", "danger")
                return redirect(url_for('.tambah_data'))
        # meyimpan ke database
        # create
        db.collection('mahasiswa').document().set(data)
        # menampilkan kembali ke frond end
        flash('Berhasil Menambahkan Data Baru!', 'success')
        return redirect(url_for('.mahasiswa'))
    jurusan = get_all_collection('jurusan')
    return render_template('tambah_mahasiswa.html', jurusan = jurusan)

@mhsapp.route('/mahasiswa/edit/<uid>', methods=['POST', 'GET'])
@login_required
def edit_data(uid):
    # mengambil data sesuai uid
    mhs = db.collection('mahasiswa').document(uid).get().to_dict()
    # memperbaharui data lama ke data baru
    if request.method == 'POST':
        data = {
            'nama_lengkap': request.form['nama_lengkap'],
            'nim': request.form['nim'],
            'jurusan': request.form['jurusan'],
            'tgl_lahir': request.form['tgl_lahir'],
            'email': request.form['email']
        }
        db.collection('mahasiswa').document(uid).update(data)
    # menyimpan kembali ke database 
        flash('Berhasil Memperbaharui Data Baru!', 'success')
        return redirect(url_for('.mahasiswa'))
    # mengembalikan ke halaman mahasiswa 
    return render_template('edit_mahasiswa.html', data=mhs)
    # return jsonify(mhs)