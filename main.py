from flask import Flask, request, redirect, render_template
import random as rd
import os
import pymysql.cursors

# Veritabanı bağlantı bilgileri
db = pymysql.connect(host='localhost',
                             user='root',
                             password='1234',
                             db='alhost',
                             charset='utf8mb4',
                             cursorclass=pymysql.cursors.DictCursor)

# İşaretçimizi oluşturalım
con = db.cursor()

app = Flask(__name__)

@app.route('/')
def host():
    return render_template('host.html')

@app.route('/host', methods=['POST'])
def hosting():
    global rand
    if request.method == 'POST':
        try:
            file = request.files['file']
            if file:
                rand = rd.randint(0, 999999999)
                filename = str(rand) + '.html'

                filepath = os.path.join(app.root_path, 'templates', filename)
                with open(filepath, 'wb') as files:
                    files.write(file.read())

                return redirect('/{}'.format(rand))
        except:
            return redirect('/error')


@app.route('/<int:rand>')
def hosts(rand):
    return render_template(str(rand) + '.html')

@app.route('/error')
def error():
    return render_template('error.html', rand=rand)

@app.route('/kullanici_yukle')
def kullanici_yukle():
    return render_template('kullanici_yukle.html')

@app.route('/user_upload', methods = ['POST'])
def user_upload():
    if request.method == 'POST':
        file = request.files['file']
        name = request.form.get('name')
        password = request.form.get('password')
        if file:
            rand = rd.randint(0, 999999999)
            filename = str(rand) + '.html'
            con.execute('INSERT INTO user_uploads VALUES(%s, %s, %s, %s)',(rand, name, password, str(filename)))
            db.commit()

            filepath = os.path.join(app.root_path, 'templates', filename)
            with open(filepath, 'wb') as files:
                files.write(file.read())

            return redirect(f'/{rand}')
        
@app.route('/html_yuklemeler')
def uploads():
    return render_template('uploads.html')

@app.route('/find', methods=['POST'])
def find():
    global name, password
    if request.method == 'POST':
        name = request.form.get('name')
        password = request.form.get('password')


        db.commit()

        return redirect('/found')


@app.route('/found')
def found():
    global name, password
    con.execute('SELECT file_id, upload_id FROM user_uploads WHERE user = %s AND password = %s',(name,password))
    files = con.fetchall()  
    return render_template('found.html', files=files, password=password)


@app.route('/upload_css')
def upload_css():
    return render_template('load_css.html')

@app.route('/user_upload_css', methods=['POST'])
def user_upload_css():
    if request.method == 'POST':
        css = request.files['css']
        name = request.form.get('name')
        password = request.form.get('password')
        file_id = rd.randint(0, 999999999)

        con.execute('INSERT INTO upload_css VALUES(%s, %s, %s, %s)',(int(file_id), name, password, str(file_id)+'.css'))
        db.commit()

        css_filepath = os.path.join(app.root_path, 'static', str(file_id)+'.css')
        with open(css_filepath, 'wb') as files:
            files.write(css.read())

        return redirect('/upload_css')
    
@app.route('/uploads_css')
def uploads_css():
    return render_template('css_uploads.html')

@app.route('/find_css', methods=['POST'])
def find_css():
    global name, password
    if request.method == 'POST':
        name = request.form.get('name')
        password = request.form.get('password')

        return redirect('/found_css')
    


@app.route('/found_css')
def found_css():
    global name, password
    con.execute('SELECT upload_id, css_id FROM upload_css WHERE user = %s AND password = %s',(name, password))
    csss = con.fetchall()    
    return render_template('found_css.html', csss=csss)    


@app.route('/read_file')
def read_file():
    return render_template('find_read.html')

@app.route('/read', methods = ['POST'])
def finding():
    if request.method == 'POST':
        filekind = request.form.get('filekind')
        name= request.form.get('filename')
        if filekind == 'css':
            return redirect(f'/read_css/{name}')
        elif filekind == 'html':
            return redirect(f'/read_html/{name}')
            

@app.route('/read_html/<string:fileid>')
def read_html(fileid):
    filepath = os.path.join(app.root_path, 'templates', f'{fileid}.html')
    if os.path.exists(filepath):
        with open(filepath, 'r', encoding='utf-8') as readHTML:
            include = readHTML.readlines()
        return render_template('read.html', include=include)
    else:
        return "Dosya bulunamadı!"
    

@app.route('/read_css/<string:fileid>')
def read_css(fileid):
    filepath = os.path.join(app.root_path, 'static', f'{fileid}.css')
    if os.path.exists(filepath):
        with open(filepath, 'r', encoding='utf-8') as readHTML:
            include = readHTML.readlines()
        return render_template('read.html', include=include)
    else:
        return "Dosya bulunamadı!"

if __name__ == '__main__':
    app.run(debug=True)
