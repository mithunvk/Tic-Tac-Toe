from flask import Flask, render_template, request, session, redirect, url_for

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'  # Change this to a random secret key

def check_winner(board):
    # Check rows
    for row in board:
        if row[0] == row[1] == row[2] != '':
            return row[0]
    # Check columns
    for col in range(3):
        if board[0][col] == board[1][col] == board[2][col] != '':
            return board[0][col]
    # Check diagonals
    if board[0][0] == board[1][1] == board[2][2] != '':
        return board[0][0]
    if board[0][2] == board[1][1] == board[2][0] != '':
        return board[0][2]
    return None

def is_draw(board):
    return all(cell != '' for row in board for cell in row)

@app.route('/')
def index():
    if 'board' not in session:
        session['board'] = [['', '', ''], ['', '', ''], ['', '', '']]
        session['player'] = 'X'
        session['winner'] = None
        session['draw'] = False
    return render_template('index.html', board=session['board'], winner=session['winner'], draw=session['draw'], player=session['player'])

@app.route('/play/<int:row>/<int:col>', methods=['POST'])
def play(row, col):
    board = session['board']
    if board[row][col] == '' and not session['winner'] and not session['draw']:
        board[row][col] = session['player']
        winner = check_winner(board)
        if winner:
            session['winner'] = winner
        elif is_draw(board):
            session['draw'] = True
        else:
            session['player'] = 'O' if session['player'] == 'X' else 'X'
    return redirect(url_for('index'))

@app.route('/reset', methods=['POST'])
def reset():
    session.clear()
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)