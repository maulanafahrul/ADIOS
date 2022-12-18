from flask import Blueprint , render_template, request, jsonify, redirect, url_for, flash, session
from db import db
from backend.auth import login_required

jurusanapp = Blueprint('jurusanapp', __name__)

@jurusanapp.route('/jurusan', methods=['POST', 'GET'])
@login_required
def jurusan():
    if request.method == 'POST':
        data = {
            'jurusan': request.form['jurusan']
        }

        db.collection('jurusan').document().set(data)
        flash('Berhasil Menambahkan Jurusan', 'success')
        return redirect(url_for('.jurusan'))
    

    jurusan_ref = db.collection('jurusan').stream()
    data = []
    for jr in jurusan_ref:
        use = jr.to_dict()
        use['id'] = jr.id
        data.append(use)
    
    return render_template('jurusan/jurusan.html', data = data)


@jurusanapp.route('/jurusan/delete/', methods=['POST'])
@login_required
def delete_jurusan():
    if request.method == 'POST':
        uid = request.form.get('uid')
        db.collection('jurusan').document(uid).delete()
        flash('Berhasil Menghapus Jurusan', 'danger')
        return redirect(url_for('.jurusan'))

