from flask import Blueprint , render_template, request, jsonify, redirect, url_for, flash, session
from db import db, get_all_collection
from backend.auth import login_required

absenapp = Blueprint('absenapp', __name__)

@absenapp.route('/absensi')
@login_required
def absensi():
    mahasiswa = get_all_collection('mahasiswa')
    return render_template('absensi/absensi.html', data = mahasiswa)
