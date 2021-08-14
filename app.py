from flask import Flask, request, render_template, jsonify, session
from boggle import Boggle

app = Flask(__name__)
app.config["SECRET_KEY"] = "shhh-so-secret"

boggle_game = Boggle()

@app.route("/")
def homepage():
    """Display the board"""

    board = boggle_game.make_board()
    session["board"] = board
    highscore = session.get("highscore", 0)
    plays = session.get("plays", 0)

    return render_template("index.html", board=board, highscore=highscore, plays=plays)

@app.route("/check-word")
def check_word():
    """Check if the word is in the dictionary"""

    word = request.args["word"]
    board = session["board"]
    response = boggle_game.check_valid_word(board, word)

    return jsonify({'result': response})

@app.route("/post-score", methods=["POST"])
def post_score():
    """Receive score, update number of plays, and update high score if applicable"""

    score = request.json["score"]
    highscore = session.get("highscore", 0)
    plays = session.get("plays", 0)

    session["plays"] = plays + 1
    session["highscore"] = max(score, highscore)

    return jsonify(brokeRecord=score > highscore)