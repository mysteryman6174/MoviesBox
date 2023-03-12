from flask import Flask, render_template, redirect, url_for, request
import requests, json

app = Flask(__name__)
TDMDB_API_KEY = "f2236fdd46f491451e73b291ac28ad51"
sort_method = "popularity"
adult = False
current_page = 1

@app.route("/")
def root_html():
    return redirect(url_for("index_html", sort_by=sort_method, page=1))

@app.route("/<sort_by>/<page>")
def index_html(sort_by, page, ptype="index_html"):
    response = requests.get(f"https://api.themoviedb.org/3/discover/movie?api_key={TDMDB_API_KEY}&language=en-US&sort_by={sort_by}.desc&include_adult={adult}&include_video=true&page={page}&with_watch_monetization_types=flatrate&m=7b62f33201c17a8fe92438b6cb0b0c13").json()
    movie_list = response['results']
    return render_template("index.html", movie_list=movie_list, sort_by=sort_by, page=int(page), ptype=ptype)

@app.route("/search")
def movie_search(page=1,sort_by=sort_method, ptype="movie_search"):
    data = request.args
    response = requests.get(f"https://api.themoviedb.org/3/search/movie?api_key={TDMDB_API_KEY}&language=en-US&query={data['movie_name']}&page={page}&include_adult=false").json()
    return render_template("index.html", movie_list=response['results'],sort_by=sort_method, page=page, ptype=ptype)

@app.route("/<movie_id>")
def movie_html(movie_id):
    response = requests.get(f"https://api.themoviedb.org/3/movie/{movie_id}?api_key={TDMDB_API_KEY}&language=en-US").json()
    return render_template("movie.html", movie=response)

@app.route("/about.html")
def about_html():
    return render_template("about.html")

if __name__ == "__main__":
    app.run(debug=True)