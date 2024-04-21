import os
from os.path import join, dirname
from dotenv import load_dotenv
from flask import Flask, render_template, request,redirect, url_for
from pymongo import MongoClient
from datetime import datetime
from bson import ObjectId

dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)

MONGODB_URI = os.environ.get("MONGODB_URI")
DB_NAME =  os.environ.get("DB_NAME")

client = MongoClient(MONGODB_URI)
db = client[DB_NAME]

app = Flask(__name__)

@app.route('/',methods=['GET', 'POST'])
def home():
    toko = list(db.tukangBuah.find({}))
    return render_template('dashboard.html', buahnya=toko)

@app.route('/index', methods=['GET', 'POST'])
def index():
    toko = list(db.tukangBuah.find({}))
    return render_template('index.html',buahnya=toko)

@app.route('/add', methods=['GET', 'POST'])
def add():
    if request.method =='POST':
        buah = request.form['fruitsName']
        harga = request.form['price']
        gambar = request.files['image']
        if gambar:
            today = datetime.now()
            my_time = today.strftime('%Y-%m-%d-%H-%M-%S')
            extension = gambar.filename.split('.')[-1]
            namaGambar = f'static/gambarBuah/buah-{my_time}.{extension}'
            gambar.save(namaGambar)
        else: 
            namaGambar = None
        deskripsi = request.form['descriptionProduct']

        doc = {
            'buah': buah,
            'harga': harga,
            'gambar': namaGambar,
            'deskripsi': deskripsi
        }
        db.tukangBuah.insert_one(doc)
        return redirect(url_for('index'))
    return render_template('AddFruit.html')


@app.route('/edit/<_id>', methods=['GET', 'POST'])
def edit(_id):
    if request.method == 'POST':
        buah = request.form['fruitsName']
        harga = request.form['price']
        gambar = request.files['image']
        deskripsi = request.form['descriptionProduct']
        doc = {
            'buah': buah,
            'harga': harga,
            'deskripsi': deskripsi
        }
        if gambar:
            today = datetime.now()
            my_time = today.strftime('%Y-%m-%d-%H-%M-%S')
            extension = gambar.filename.split('.')[-1]
            namaGambar = f'static/gambarBuah/buah-{my_time}.{extension}'
            gambar.save(namaGambar)
            doc['gambar'] = namaGambar
        else: 
            namaGambar = None
        db.tukangBuah.update_one({'_id':ObjectId(_id)}, {'$set':doc})
        return redirect(url_for('index'))

    id = ObjectId(_id)
    data = list(db.tukangBuah.find({'_id':id}))
    return render_template('EditFruit.html', data=data)

@app.route('/delete/<_id>',methods=['GET', 'POST'])
def delete(_id):
    db.tukangBuah.delete_one({'_id':ObjectId(_id)})
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run('0.0.0.0', port =5000, debug=True)