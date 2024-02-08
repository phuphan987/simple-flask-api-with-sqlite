from flask import Flask, request, jsonify
import sqlite3

app = Flask(__name__)

DATABASE = 'movies.sqlite'

# def init_database():
#     with sqlite3.connect(DATABASE) as conn:
#         cursor = conn.cursor()
#         cursor.execute('CREATE TABLE IF NOT EXISTS movies (id INTEGER PRIMARY KEY, title TEXT, release_year INTEGER)')
#         conn.commit()
# init_database()

def execute_query(query, params=()):
    with sqlite3.connect(DATABASE) as conn:
        cursor = conn.cursor()
        try:
            cursor.execute(query, params)
            conn.commit()
            return cursor
        except sqlite3.Error as e:
            conn.rollback()
            raise e

@app.route('/')
def main_page():
    return jsonify({"message": "welcome"}), 200

@app.route('/movies', methods=['GET', 'POST'])
def get_post_movies():
    if request.method == 'GET':
        rows = execute_query('SELECT * FROM movies').fetchall()
        movies_list = [{'id': row[0], 'title': row[1], 'release_year': row[2]} for row in rows]
        return jsonify({"message": movies_list}), 200
    
    elif request.method == 'POST':
        body = request.json
        execute_query('INSERT INTO movies VALUES (?, ?, ?)', (body['id'], body['title'], body['release_year']))
        return jsonify({"message": "The movie has been added", "body": body}), 201
    
@app.route('/movies/<int:movie_id>', methods=['PUT', 'DELETE'])
def put_delete_movies(movie_id):
    if request.method == 'PUT':
        body = request.json
        execute_query('UPDATE movies SET id = ?, title = ?, release_year = ? WHERE id = ?', (body['id'], body['title'], body['release_year'], movie_id))
        return jsonify({"message": "The movie has been updated"}), 200
    
    elif request.method == 'DELETE':
        execute_query('DELETE FROM movies WHERE id = ?', (movie_id,))
        return jsonify({"message": "The movie has been deleted"}), 200
    
if __name__ == '__main__':
    app.run(debug=True)