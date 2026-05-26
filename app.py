from flask import Flask, render_template, request
import mysql.connector

app = Flask(__name__)

# Database configuration
db_config = {
    'user': 'root',
    'password': 'your_password',
    'host': 'localhost',
    'database': 'bus'
}

def get_db_connection():
    conn = mysql.connector.connect(**db_config)
    return conn

@app.route('/', methods=['GET', 'POST'])
def index():
    routes = []
    timings = []
    selected_route = None

    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT routename FROM bus_route")
    routes = [row[0] for row in cursor.fetchall()]

    if request.method == 'POST':
        selected_route = request.form.get('route')
        if selected_route:
            cursor.execute("""
                SELECT bd.busno, bd.busname, bt.time
                FROM bus_details AS bd
                JOIN bus_timing AS bt ON bd.busno = bt.busno
                JOIN bus_route AS br ON bt.routeno = br.routeno
                WHERE br.routename = %s
                ORDER BY bt.time
            """, (selected_route,))
            timings = cursor.fetchall()

    cursor.close()
    conn.close()

    return render_template('index.html', routes=routes, timings=timings, selected_route=selected_route)

if __name__ == '__main__':
    app.run(debug=True)
