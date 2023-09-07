from flask import Flask, render_template, redirect, url_for, request
from flask_bootstrap import Bootstrap5
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, IntegerField, FloatField
from wtforms.validators import DataRequired, InputRequired, Length
import requests

'''
Red underlines? Install the required packages first: 
Open the Terminal in PyCharm (bottom left). 

On Windows type:
python -m pip install -r requirements.txt

On MacOS type:
pip3 install -r requirements.txt

This will install the packages from requirements.txt for this project.
'''

app = Flask(__name__)
app.config['SECRET_KEY'] = '8BYkEfBA6O6donzWlSihBXox7C0sKR6b'
Bootstrap5(app)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///my-favourite-movies.db"
db = SQLAlchemy()
db.init_app(app)


class Movie(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(250), unique=True, nullable=False)
    year = db.Column(db.Integer, nullable=False)
    description = db.Column(db.String(500), nullable=False)
    rating = db.Column(db.Float, nullable=True)
    ranking = db.Column(db.Integer, nullable=True)
    review = db.Column(db.String(250), nullable=True)
    img_url = db.Column(db.String(250), nullable=False)


class RateMovieForm(FlaskForm):
    rating = StringField("Your Rating Out of 10. e.g. 7.5")
    review = StringField("Your Review")
    submit = SubmitField("Done")


class FindMovieForm(FlaskForm):
    title = StringField("Title", validators=[InputRequired()])
    submit = SubmitField("Add")


class AddMovie(FlaskForm):
    title = StringField("Title", validators=[InputRequired()])
    year = IntegerField()



# with app.app_context():
#     db.create_all()


# with app.app_context():
#     new_movie = Movie(
#         title="Phone Booth",
#         year=2002,
#         description="Publicist Stuart Shepard finds himself trapped in a phone booth, pinned down by an extortionist's sniper rifle. Unable to leave or receive outside help, Stuart's negotiation with the caller leads to a jaw-dropping climax.",
#         rating=7.3,
#         ranking=10,
#         review="My favourite character was the caller.",
#         img_url="https://image.tmdb.org/t/p/w500/tjrX2oWRCM3Tvarz38zlZM7Uc10.jpg"
#     )
#     db.session.add(new_movie)
#     db.session.commit()


# second_movie = Movie(
#     title="Avatar The Way of Water",
#     year=2022,
#     description="Set more than a decade after the events of the first film, learn the story of the Sully family (Jake, Neytiri, and their kids), the trouble that follows them, the lengths they go to keep each other safe, the battles they fight to stay alive, and the tragedies they endure.",
#     rating=7.3,
#     ranking=9,
#     review="I liked the water.",
#     img_url="https://image.tmdb.org/t/p/w500/t6HIqrRAclMCA60NsSmeqe9RmNV.jpg"
# )
# with app.app_context():
#     db.session.add(second_movie)
#     db.session.commit()
#


@app.route("/")
def home():
    result = db.session.execute(db.select(Movie).order_by(Movie.id))
    all_movies = result.scalars()
    return render_template("index.html", movies=all_movies)


@app.route("/edit", methods=["GET", "POST"])
def edit():
    form = RateMovieForm()
    movie_id = request.args.get("id")
    movie = db.get_or_404(Movie, movie_id)
    if form.validate_on_submit():
        movie.rating = float(form.rating.data)
        movie.review = form.review.data
        db.session.commit()
        return redirect(url_for("home"))
    return render_template("edit.html", form=form, movie=movie)

@app.route('/delete')
def delete():
    movie_id = request.args.get("id")
    movie = db.get_or_404(Movie, movie_id)
    db.session.delete(movie)
    db.session.commit()
    return redirect(url_for("home"))



@app.route("/add", methods=["GET", "POST"])
def add():
    form = FindMovieForm()
    if form.validate_on_submit():
        title = form.title.data
        with app.app_context():
            result = db.session.execute(db.select(Movie).where(Movie.title == title)).scalar()
            if result:
                print("Item already exists.")
                return render_template(url_for("add.html", form=form))
            else:
                with app.app_context():
                    new_movie = Movie(title)


    return render_template("add.html", form=form)




    # if request.method == 'POST':
    #     movie_id = request.form["id"]
    #     movie_to_update = db.get_or_404(Movie, movie_id)
    #     movie_to_update.rating = request.form['rating']
    #     # db.session.commit()
    #     movie_to_update.review = request.form['review']
    #     db.session.commit()
    #     return redirect(url_for('home'))
    # movie_id = request.args.get('id')
    # movie_selected = db.get_or_404(Movie, movie_id)
    # return render_template("edit.html", movie=movie_selected, movie_id=movie_id)


if __name__ == '__main__':
    app.run(debug=True)
