from flask import Flask, render_template, request, url_for, redirect
from connect_db import connect_to_db
import re


app = Flask(__name__)

nawigation = [{'href': 'kino', 'caption': 'kino'},
              {'href': 'film', 'caption': 'film'},
              {'href': 'bilet', 'caption': 'bilet'},
              {'href': 'platnosc', 'caption': 'platnosc'},
              {'href': 'seans', 'caption': 'seans'}
              ]
regex = r"[0-9]{4}(\.|-)([1]{1}[0-2]{1}|[0]{1}[0-9]{1})(\.|-)([0-2]{1}[0-9]{1}|[3]{1}[0-1]{1})"


@app.route('/')
def main_page():
    return render_template('index.html', nawigation=nawigation)


@app.route('/kino')
def show_kino():
    html = {}
    return render_template('kino.html', html=html, nawigation=nawigation)


@app.route('/kino', methods=['POST'])
def kino():
    conn = connect_to_db('cinemas_db')
    cur = conn.cursor()
    if request.method == 'POST':
        if request.form['submit'] == 'cinema':
            name = request.form['name']
            adres = request.form['address']
            seats = request.form['seats']
            sql_insert_into_kino = 'INSERT INTO Kino VALUES(default, %s, %s, %s)'
            cur.execute(sql_insert_into_kino, (name, adres, seats,))
        if request.form['submit'] == 'usun':
            name_cin = request.form['del_cinema']
            sql_del_kino = 'DELETE FROM Kino WHERE id=%s;'
            cur.execute(sql_del_kino, (name_cin,))
        if request.form['submit'] == 'znajdz':
            name_find = request.form['find_cinema']
            sql_find_cinema = 'SELECT * FROM Kino Where name like "%{}%";'.format(name_find)
            cur.execute(sql_find_cinema)
        if request.form['submit'] == 'show':
            sql_find_cinema = 'SELECT * FROM Kino'
            cur.execute(sql_find_cinema)
    html = {}
    for row in cur:
        html[row[0]] = row[1]
    cur.close()
    conn.close()
    return render_template('kino.html', html=html, nawigation=nawigation)


@app.route('/kino_site/<id>')
def kino_site(id):
    select_id = id
    conn = connect_to_db('cinemas_db')
    cur = conn.cursor()
    sql_info_kino = 'SELECT Film.name as name FROM Seans JOIN Film ON Seans.movie_id=Film.id ' \
                    'JOIN Kino ON Seans.cinema_id=Kino.id where Kino.id={}'.format(select_id)
    cur.execute(sql_info_kino)
    html = ''
    film = []
    for row in cur:
        film_pom = '{}'.format(row[0])
        film.append(film_pom)
        html = '{}'.format(film)
    cur.close()
    conn.close()
    return render_template('kino_site.html', html=html, nawigation=nawigation)


@app.route('/film')
def show_film():
    html = {}
    return render_template('film.html', html=html, nawigation=nawigation)


@app.route('/film', methods=['POST'])
def add_movie():
    conn = connect_to_db('cinemas_db')
    cur = conn.cursor()
    if request.method == 'POST':
        if request.form['submit'] == 'movie':
            name = request.form['name']
            desc = request.form['desc']
            try:
                rating = int(request.form['rating'])
                if rating in range(1, 11):
                    sql_insert_into_film = 'INSERT INTO Film VALUES(default, %s, %s, %s)'
                    cur.execute(sql_insert_into_film, (name, desc, rating,))
                else:
                    return render_template('error.html')
            except ValueError:
                pass
        if request.form['submit'] == 'show':
            sql_show_movie = 'SELECT *FROM Film;'
            cur.execute(sql_show_movie)
        if request.form['submit'] == 'znajdz':
            title_find = request.form['mov_find']
            sql_find_movie_title = 'SELECT * FROM Film Where name LIKE "%{}%";'.format(title_find)
            cur.execute(sql_find_movie_title)
        if request.form['submit'] == 'rating_f':
            try:
                rat_find_min = int(request.form['rat_find'])
                rat_find_max = rat_find_min+1
                sql_find_movie_rating = 'SELECT *FROM Film Where rating>={} and rating<{};'.format(rat_find_min,
                                                                                                   rat_find_max)
                cur.execute(sql_find_movie_rating)
            except ValueError:
                pass
        if request.form['submit'] == 'usun':
            del_movie = request.form['del_movie']
            sql_del_movie = 'DELETE FROM Film WHERE id = %s;'
            cur.execute(sql_del_movie, (del_movie,))
    html = {}
    for row in cur:
        html[row[0]] = row[1]
    cur.close()
    conn.close()
    return render_template('film.html', html=html, nawigation=nawigation)


@app.route('/film_site/<id>')
def film_site(id):
    select_id = id
    conn = connect_to_db('cinemas_db')
    cur = conn.cursor()
    sql_info_film = 'SELECT description, rating, Kino.name as kino from Seans JOIN Film ON Seans.movie_id=Film.id ' \
                    'JOIN Kino ON Seans.cinema_id=Kino.id where Film.id = {}'.format(select_id)
    cur.execute(sql_info_film)
    html = ''
    kina = []
    for row in cur:
        kina_pom = '{}'.format(row[2])
        kina.append(kina_pom)
        html = '{} -- {}pkt. {}'.format(row[0], row[1], kina)
    cur.close()
    conn.close()
    return render_template('film_site.html', html=html, nawigation=nawigation)


@app.route('/bilet')
def show_bilet():
    return render_template('bilet.html', nawigation=nawigation)


@app.route('/bilet', methods=['POST'])
def add_ticket():
    conn = connect_to_db('cinemas_db')
    cur = conn.cursor()
    if request.method == 'POST':
        if request.form['submit'] == 'ticket':
            try:
                quantity = int(request.form['quantity'])
                price = float(request.form['price'])
                sql_insert_to_bilet = 'INSERT INTO Bilet VALUES(default, %s, %s)'
                cur.execute(sql_insert_to_bilet, (quantity, price,))
            except ValueError:
                pass
        if request.form['submit'] == 'show':
            sql_show_ticket = 'SELECT * FROM Bilet;'
            cur.execute(sql_show_ticket)
        if request.form['submit'] == 'usun':
            del_ticket = request.form['del_ticket']
            sql_del_ticket = 'DELETE FROM Bilet WHERE id=%s;'
            cur.execute(sql_del_ticket, (del_ticket,))
    html = []
    for row in cur:
        linia = 'ID. {}. Ilość: {}, cena: {}'.format(row[0], row[1], row[2])
        html.append(linia)
    cur.close()
    conn.close()
    return render_template('bilet.html', html=html, nawigation=nawigation)


@app.route('/platnosc')
def show_platnosc():
    return render_template('platnosc.html', nawigation=nawigation)


@app.route('/platnosc', methods=['POST'])
def add_payment():
    conn = connect_to_db('cinemas_db')
    cur = conn.cursor()
    result = ''
    if request.method == 'POST':
        if request.form['submit'] == 'payment':
            option = request.form['payment_type']
            if option == 'transfer':
                result = 'przelew'
            if option == 'cash':
                result = 'gotowka'
            if option == 'card':
                result = 'karta'
            dataa = request.form['payment_date']
            matches = re.match(regex, dataa)
            if matches:
                sql_insert_into_platnosc = 'INSERT INTO Platnosc VALUE(default, %s, %s)'
                cur.execute(sql_insert_into_platnosc, (result, matches.group()))
            else:
                return render_template('error.html')
        if request.form['submit'] == 'show':
            sql_show_payment = 'SELECT * FROM Platnosc'
            cur.execute(sql_show_payment)
        if request.form['submit'] == 'show_option':
            option1 = request.form['variant']
            data_find_1 = request.form['day_payment']
            matches_find_1 = re.match(regex, data_find_1)
            if matches_find_1:
                if option1 == 'before':
                    sql_find_payment = 'SELECT * FROM Platnosc WHERE data <= "{}"'.format(matches_find_1.group())
                    cur.execute(sql_find_payment)
                if option1 == 'after':
                    sql_find_payment = 'SELECT * FROM Platnosc WHERE data >= "{}"'.format(matches_find_1.group())
                    cur.execute(sql_find_payment)
                if option1 == 'in_day':
                    sql_find_payment = 'SELECT * FROM Platnosc WHERE data = "{}"'.format(matches_find_1.group())
                    cur.execute(sql_find_payment)
            else:
                return render_template('error.html')
        if request.form['submit'] == 'show_betw':
            data_find_2 = request.form['from_day']
            data_find_3 = request.form['to_day']
            matches_find_2 = re.match(regex, data_find_2)
            matches_find_3 = re.match(regex, data_find_3)
            if matches_find_2 and matches_find_3:
                sql_find_payment = 'SELECT * FROM Platnosc WHERE data BETWEEN "{}" AND "{}"'.\
                    format(matches_find_2.group(), matches_find_3.group())
                cur.execute(sql_find_payment)
            else:
                return render_template('error.html')
        if request.form['submit'] == 'usun':
            del_payment = request.form['del_payment']
            sql_del_payment = 'DELETE FROM Platnosc WHERE id = {}'.format(del_payment)
            cur.execute(sql_del_payment)
    html = []
    for row in cur:
        linia = 'ID. {}. Typ płatności : {}, data płatności: {}'.format(row[0], row[1], row[2])
        html.append(linia)
    cur.close()
    conn.close()
    return render_template('platnosc.html', html=html, nawigation=nawigation)


@app.route('/seans', methods=['GET', 'POST'])
def seans():
    conn = connect_to_db('cinemas_db')
    cur = conn.cursor()
    movies = {}
    cinemas = {}
    query = "SELECT id, name FROM Film"
    cur.execute(query)
    for row in cur:
        movies[row[0]] = row[1]
    query = "SELECT id, name FROM Kino"
    cur.execute(query)
    for row in cur:
        cinemas[row[0]] = row[1]
    if request.method == 'POST':
        if request.form['submit'] == 'send':
            movie_id = request.form.get('movie_id')
            cinema_id = request.form.get('cinema_id')
            sql_insert_seans = 'INSERT INTO Seans(movie_id,cinema_id) VALUES({},{})'.format(movie_id, cinema_id)
            cur.execute(sql_insert_seans)
        if request.form['submit'] == 'show':
            sql_show_seans = 'SELECT seans_id, Kino.name as kino, Film.name as film, description,' \
                             'rating from Seans JOIN Kino ON Seans.cinema_id=Kino.id ' \
                             'JOIN Film ON Seans.movie_id=Film.id'
            cur.execute(sql_show_seans)
        if request.form['submit'] == 'usun':
            del_seans = request.form['del_seans']
            sql_del_seans = 'DELETE FROM Seans where seans_id = {}'.format(del_seans)
            cur.execute(sql_del_seans)
    html = []
    for row in cur:
        linia = 'ID.{}. {}: {} ----- {} - [{}pkt.]'.format(row[0], row[1], row[2], row[3], row[4])
        html.append(linia)
    cur.close()
    conn.close()
    return render_template('seans.html', movies=movies, cinemas=cinemas, nawigation=nawigation, html=html)


app.run(debug=True)
