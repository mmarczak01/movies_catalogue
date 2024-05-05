from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def homepage():
    movies = []
    for i in range (0,8):
        movies.append(i)
    return render_template("homepage.html", movies=movies)

if __name__ == '__main__':
    app.run(debug=True)