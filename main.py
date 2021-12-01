from pprint import pprint
from flask import Flask, render_template, redirect, url_for, request
from flask_sqlalchemy import SQLAlchemy
import requests
from datetime import datetime
import config
app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app, session_options={"expire_on_commit": False})

TMDB_API_KEY = config.API_KEY


class User(db.Model):
    username = db.Column(db.String(100), primary_key=True, nullable=False)
    eml = db.Column(db.String(100), nullable=False)
    pswd = db.Column(db.String(100), nullable=False)
    bio = db.Column(db.String(100), nullable=False)
    djoin = db.Column(db.String(100), nullable=False)
    dbrth = db.Column(db.String(100), nullable=False)
    fvdir = db.Column(db.String(100), nullable=False)
    fvmov = db.Column(db.String(100), nullable=False)
    prflng = db.Column(db.String(100), nullable=False)
    prfgen = db.Column(db.String(100), nullable=False)

    def __repr__(self):
        return f'<User {self.username}>'


class TopMovie(db.Model):
    username = db.Column(db.String(100), primary_key=True, nullable=False)
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    title = db.Column(db.String(100), nullable=False, unique=True)
    year = db.Column(db.Integer(), nullable=False)
    tag = db.Column(db.String(500), nullable=False)
    rating = db.Column(db.Float(), nullable=True)
    ranking = db.Column(db.Integer(), nullable=True)
    review = db.Column(db.String(500), nullable=True)
    img_url = db.Column(db.String(500), nullable=False)

    def __repr__(self):
        return f'<Movie {self.title}>'


db.create_all()

global user



# *----- Main Landing Page -----*
@app.route('/')
def home():
    return render_template("main.html")


# *----- Main Landing Page -----*

# *----- Signup & Profile Creation -----*

@app.route('/signup')
def signup():
    return render_template("signup.html")


@app.route('/profcrt', methods=["GET", "POST"])
def profcrt():
    global user
    if request.method == "POST":
        usnm = request.form.get('name')
        eml = request.form.get('email')
        pswd = request.form.get('pwd')
        dbr = request.form.get('db')
        dob = datetime.strptime(dbr, "%Y-%m-%d")
        dobst = dob.strftime("%d %b, %Y")
        djn = datetime.now().strftime("%d %b, %Y")
        bio = request.form.get('bio')
        favdir = request.form.get('favdir')
        favmov = request.form.get('favmov')
        preflang = request.form.get('preflang')
        prefgen = request.form.get('prefgen')
        print(usnm, eml, pswd, dobst, bio, favdir, favmov, preflang, prefgen)
        new_user = User(
            username=usnm,
            eml=eml,
            pswd=pswd,
            bio=bio,
            djoin=djn,
            dbrth=dobst,
            fvdir=favdir,
            fvmov=favmov,
            prflng=preflang,
            prfgen=prefgen
        )
        already_exists = db.session.query(User.username).filter_by(username=usnm).first() is not None
        if already_exists:
            data = ['Uh Oh!!', "This username already exists.", 'Signup Screen', 'signup']
            return render_template("intermd.html", data=data)
        else:
            db.session.add(new_user)
            db.session.commit()
            user = new_user
            data = ['Success!!', "Your account has been created successfully!!", 'Profile', 'profile']
            return render_template("intermd.html", data=data)


# *----- Signup & Profile Creation -----*


# *----- Login and validation -----*

@app.route('/login')
def login():
    return render_template("signin.html")


@app.route('/validate', methods=["GET", "POST"])
def validate():
    global user
    if request.method == "GET":
        return redirect(url_for("profile"))
    if request.method == "POST":
        usnm = request.form.get('name')
        pswd = request.form.get('pwd')
        exists = db.session.query(User.username).filter_by(username=usnm).first() is not None
        if exists:
            user_to_verify = User.query.get(usnm)
            if (usnm == user_to_verify.username) and (pswd == user_to_verify.pswd):
                user = user_to_verify
                data = ['Success!!', "You have been logged in successfully!!", 'Continue', 'profile']
                return render_template("intermd.html", data=data)
            else:
                data = ['Oops!!', "Your Username and Password Do Not Match", 'Login Screen', 'login']
                return render_template("intermd.html", data=data)
        else:
            data = ['Oops!!', "This Username Does Not Exist", 'Signup Screen', "signup"]
            return render_template("intermd.html", data=data)


# *----- Login and validation -----*

# *----- Logout Path -----*

@app.route('/logout')
def logout():
    data = ['Goodbye', "Thank you for visiting our site.", 'Logout', 'home']
    return render_template("intermd.html", data=data)


# *----- Logout Path -----*

# *----- Profile Path -----*

@app.route('/profile')
def profile():
    global user
    y = datetime.strptime(user.dbrth, "%d %b, %Y").year
    m = datetime.strptime(user.dbrth, "%d %b, %Y").month
    d = datetime.strptime(user.dbrth, "%d %b, %Y").day
    yc = datetime.now().year
    mc = datetime.now().month
    dc = datetime.now().day
    age = yc - y - 1
    if mc > m:
        age += 1
    elif mc == m:
        if dc >= d:
            age += 1
    print(y, m, d, yc, mc, dc, age)
    return render_template('profile.html', user_data=user, age=age)


# *----- Profile Path -----*

# *----- Movie Detail Search Path -----*

@app.route('/movsrc')
def movsrc():
    return render_template('mov_search.html')


def get_movies(movname):
    # Getting the Movie ID from the Movie name
    movie_id_url = f"https://api.themoviedb.org/3/search/movie?api_key={TMDB_API_KEY}&query={movname}"
    image_url = "http://image.tmdb.org/t/p/w500"
    data = requests.get(f"{movie_id_url}").json()['results']
    if len(data) > 5:
        movies = data[:5]
    else:
        movies = data
    # pprint(movies)
    movie_data = []
    index = 97
    for movie in movies:
        new_movie = {
            'id': movie['id'],
            'css': chr(index),
            'title': movie['title'],
            'backdrop': f"{image_url}{movie['backdrop_path']}",
            'poster': f"{image_url}{movie['poster_path']}",
            'year': movie['release_date'].split('-')[0] if movie['release_date'].split('-') else "Not Available"
        }
        movie_data.append(new_movie)
        index += 1
    # pprint(movie_data)
    return movie_data


@app.route('/movsrcresall', methods=["GET", "POST"])
def movsrcresall():
    movname = request.form.get('movname')
    movies = get_movies(movname)
    return render_template('allmovres.html', movies=movies, goto="movsrcresult")


def get_movie_deets(movie_id):
    # All required API queries
    image_url = "http://image.tmdb.org/t/p/w500"
    cast_info_url = f"https://api.themoviedb.org/3/movie/{movie_id}/credits?"
    movie_data_url = f"https://api.themoviedb.org/3/movie/{movie_id}"
    mov_dat_params = {
        "api_key": TMDB_API_KEY,
        "language": "en-US"
    }

    # Getting Cast Info and Director
    director = ""
    cast_data = []
    response = requests.get(cast_info_url, params=mov_dat_params).json()
    cast = response['cast'][:6]
    crew = response['crew']
    for i in crew:
        if i['job'] == "Director":
            director = i['name']
            break
    for i in cast:
        tmp = {
            'actor': i['original_name'],
            'character': i['character'],
            'img': f"{image_url}{i['profile_path']}"
        }
        cast_data.append(tmp)

    # Getting Movie Info
    response = requests.get(movie_data_url, params=mov_dat_params).json()
    # pprint(response)
    genres = []
    for i in response['genres']:
        genres.append(i['name'])
    languages = []
    for i in response['spoken_languages']:
        languages.append(i['english_name'])
    movie_data = {
        'title': response['original_title'],
        'overview': response['overview'],
        'tag': response['tagline'],
        'runtime': response['runtime'],
        'rating': response['vote_average'],
        'year': response['release_date'].split('-')[0],
        'genres': genres,
        'language': languages,
        'poster': f"{image_url}{response['poster_path']}",
        'backdrop': f"{image_url}{response['backdrop_path']}",
        'director': director
    }
    # pprint(cast_data)
    # pprint(movie_data)
    all_data = [cast_data, movie_data]
    return all_data


@app.route('/movsrcresult/<int:movid>', methods=["GET", "POST"])
def movsrcresult(movid):
    data = get_movie_deets(movid)
    return render_template('movie_det.html', data=data)


# *----- Movie Detail Search Path -----*

# *----- Movie Recommendation Search Path -----*

@app.route('/movrec')
def movrec():
    return render_template('rec_search.html')


@app.route('/movrecsrcall', methods=['GET', 'POST'])
def movrecsrcall():
    movname = request.form.get('movname')
    movies = get_movies(movname)
    return render_template('allmovres.html', movies=movies, goto="movrecresult")


def get_movie_recs(movie_id):
    image_url = "http://image.tmdb.org/t/p/w500"
    movie_rec_url = f"https://api.themoviedb.org/3/movie/{movie_id}/recommendations?"
    mov_dat_params = {
        "api_key": TMDB_API_KEY,
        "language": "en-US"
    }
    response = requests.get(movie_rec_url, params=mov_dat_params).json()
    all_data = response['results']
    rec_data = []
    for movie in all_data:
        temp = {
            "poster": f"{image_url}/{movie['poster_path']}",
            "title": movie["title"],
            "id": movie["id"],
            "overview": movie['overview']
        }
        rec_data.append(temp)
    # pprint(rec_data)
    # print(len(rec_data))
    return rec_data


@app.route('/movrecresult/<int:movid>', methods=["GET", "POST"])
def movrecresult(movid):
    mov_data = get_movie_recs(movid)
    return render_template("rec_result.html", mov_data=mov_data)


@app.route('/movrecfin/<int:movid>')
def movrecfin(movid):
    data = get_movie_deets(movid)
    return render_template("movie_det.html", data=data)


# *----- Movie Recommendation Search Path -----*

# *----- Top Ten Path -----*

@app.route('/topten')
def topten():
    global user
    print(user.username)
    movies = TopMovie.query.filter_by(username=user.username).order_by(TopMovie.rating.desc()).all()
    for i in range(len(movies)):
        movies[i].ranking = i + 1
    db.session.commit()
    return render_template("topten.html", movies=movies)


@app.route('/toptenedit/<int:movid>', methods=['GET', 'POST'])
def toptenedit(movid):
    global user
    if request.method == 'GET':
        return render_template('tpaddm.html', movid=movid, goto="toptenedit")
    else:
        rating = request.form.get('rating')
        review = request.form.get('review')
        upd_mov = TopMovie.query.get((user.username, movid))
        upd_mov.review = review
        upd_mov.rating = rating
        db.session.commit()
        return redirect(url_for('topten'))


@app.route('/toptenremove/<int:movid>')
def toptenremove(movid):
    global user
    movie = TopMovie.query.get((user.username, movid))
    print(movie)
    db.session.delete(movie)
    db.session.commit()
    return redirect(url_for('topten'))


@app.route('/toptenadd', methods=['GET', 'POST'])
def toptenadd():
    return render_template("top_search.html")


@app.route('/toptenresall', methods=['GET', 'POST'])
def toptenresall():
    movname = request.form.get('movname')
    movies = get_movies(movname)
    return render_template('allmovres.html', movies=movies, goto="toptenfin")


@app.route('/toptenfin/<int:movid>')
def toptenfin(movid):
    return render_template('tpaddm.html', movid=movid, goto="addtodb")


@app.route('/addtodb/<int:movid>', methods=['GET', 'POST'])
def addtodb(movid):
    global user
    rating = request.form.get('rating')
    review = request.form.get('review')
    movie_det = get_movie_deets(movid)
    print(movie_det[1])
    new_movie = TopMovie(
        username=user.username,
        id=movid,
        title=movie_det[1]['title'],
        year=movie_det[1]['year'],
        tag=movie_det[1]['tag'],
        rating=rating,
        review=review,
        img_url=movie_det[1]['poster']
    )
    db.session.add(new_movie)
    db.session.commit()
    return redirect(url_for('topten'))


# *----- Top Ten Path -----*


# *----- Running the Application on the Flask Server -----*


if __name__ == "__main__":
    app.run(debug=True)

# *----- Running the Application on the Flask Server -----*