import firebase_admin
from firebase_admin import credentials, firestore
import pyrebase



cred = credentials.Certificate("firebase.json")
firebase_admin.initialize_app(cred)

db = firestore.client()


firebaseConfig = {
    'apiKey': "AIzaSyDR5H6rGsUP3iBisVO5-d5XF1Mh5lERrRk",
    'authDomain': "adios-9b34c.firebaseapp.com",
    'databaseURL': "https://adios-9b34c-default-rtdb.asia-southeast1.firebasedatabase.app",
    'projectId': "adios-9b34c",
    'storageBucket': "adios-9b34c.appspot.com",
    'messagingSenderId': "993192735656",
    'appId': "1:993192735656:web:d2d30c21c4ff76da44239d"
}
firebase = pyrebase.initialize_app(firebaseConfig)
storage = firebase.storage()

def get_all_collection(collection, orderBy=None, direction=None):
    if orderBy:
        collects_ref = db.collection(collection).order_by(
            orderBy, direction=direction)
    else:
        collects_ref = db.collection(collection)
    collects = collects_ref.stream()
    RETURN = []
    for collect in collects:
        ret = collect.to_dict()
        ret['id'] = collect.id
        RETURN.append(ret)
    return RETURN




# daftar_mahasiswa = [
#     {
#         'nama_lengkap': 'asasdasdasd',
#         'nim': '12323',
#         'id': 1,
#         'jurusan': 'SI',
#         'is_active': True,
#         'nilai': '3.00'
#     },
#     {
#         'nama_lengkap': 'sdfsfsdfs',
#         'nim': '345345',
#         'id': 2,
#         'jurusan': 'IT',
#         'is_active': True,
#         'nilai': '3.44'
#     },
#     {
#         'nama_lengkap': 'rtrtertet',
#         'nim': '4553453',
#         'id': 3,
#         'jurusan': 'Kedokteran',
#         'is_active': True,
#         'nilai': '3.00'
#     },
#     {
#         'nama_lengkap': 'cvxcvxvx',
#         'nim': '12323',
#         'id': 4,
#         'jurusan': 'SI',
#         'is_active': False,
#         'nilai': '3.00'
#     },
#     {
#         'nama_lengkap': 'hjhgjghjg',
#         'nim': '3434',
#         'id': 5,
#         'jurusan': 'SI',
#         'is_active': False,
#         'nilai': '3.00'
#     },
# ]

