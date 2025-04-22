from flask import Flask, request, jsonify, render_template
import copy

app = Flask(__name__)

def check_winner(board):
    for i in range(3):
        if board[i][0] != "" and all(board[i][j] == board[i][0] for j in range(3)):
            return board[i][0]
        if board[0][i] != "" and all(board[j][i] == board[0][i] for j in range(3)):
            return board[0][i]
    if board[0][0] != "" and all(board[i][i] == board[0][0] for i in range(3)):
        return board[0][0]
    if board[0][2] != "" and all(board[i][2 - i] == board[0][2] for i in range(3)):
        return board[0][2]
    return None

def is_full(board):
    return all(cell != "" for row in board for cell in row)

def minimax(board, is_maximizing):
    winner = check_winner(board)
    if winner == "X":
        return 1
    elif winner == "O":
        return -1
    elif is_full(board):
        return 0

    if is_maximizing:
        best_score = -float('inf')
        for i in range(3):
            for j in range(3):
                if board[i][j] == "":
                    board[i][j] = "X"
                    score = minimax(board, False)
                    board[i][j] = ""
                    best_score = max(score, best_score)
        return best_score
    else:
        best_score = float('inf')
        for i in range(3):
            for j in range(3):
                if board[i][j] == "":
                    board[i][j] = "O"
                    score = minimax(board, True)
                    board[i][j] = ""
                    best_score = min(score, best_score)
        return best_score

def best_move(board):
    best_score = -float('inf')
    move = None
    for i in range(3):
        for j in range(3):
            if board[i][j] == "":
                board[i][j] = "X"
                score = minimax(board, False)
                board[i][j] = ""
                if score > best_score:
                    best_score = score
                    move = (i, j)
    return move

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/move", methods=["POST"])
def move():
    data = request.json
    board = data["board"]

    if check_winner(board) or is_full(board):
        return jsonify({"board": board, "winner": check_winner(board) or "draw"})

    move = best_move(copy.deepcopy(board))
    if move:
        i, j = move
        board[i][j] = "X"

    winner = check_winner(board)
    if winner:
        return jsonify({"board": board, "winner": winner})
    elif is_full(board):
        return jsonify({"board": board, "winner": "draw"})

    return jsonify({"board": board})

@app.route("/check", methods=["POST"])
def check():
    board = request.json["board"]
    winner = check_winner(board)
    if winner:
        return jsonify({"winner": winner})
    elif is_full(board):
        return jsonify({"winner": "draw"})
    return jsonify({"winner": None})

if __name__ == "__main__":
    app.run(debug=True)
