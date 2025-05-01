from flask import Flask, render_template, request, redirect, url_for, flash
from D_Lite_Backend_Model import *
from db import *
app = Flask(__name__)

app.secret_key = 'wekvjkbkns1233450lsdnkk'

# VALID_USERNAME = 'captain@gmail.com'
#
# VALID_PASSWORD = 'anchor123'

@app.route('/', methods = ['GET',  'POST'])
def home_page():
    return render_template('Home.html')

@app.route('/aquanav/register', methods = ['GET', 'POST'])
def sign_up():

    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']

        success = register_user(username, email, password)

        if success:
            flash('Registration Successfully', 'success')
            return redirect(url_for('login'))
        else:
            flash('Email already exists', 'warning')
            return redirect(url_for('sign_up'))
    flash('Welcome To AquaNav', 'success')
    return render_template('sign_up.html')

@app.route('/aquanav/login', methods = ['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        success_login = validate_login(username, password)

        if success_login:
            flash('Welcome Aboard Captain', 'success')
            return redirect(url_for('ship_route'))

        else:
            flash('Invalid username or password', 'danger')
            return redirect(url_for('login'))
    return render_template('login.html')

@app.route('/aquanav/index', methods=['GET', 'POST'])
def ship_route():
    ports = list(ALL_LOCATIONS.keys())
    route_info = None
    folium_map_html = None

    if request.method == 'POST':
        start_port = request.form['start']
        end_port = request.form['end']

        if start_port and end_port and start_port != end_port:
            G = create_ocean_graph()
            path = find_shortest_path(G, start_port, end_port)
            route_stats = calculate_route_stats(G, path)
            route_map = plot_route_on_map(G, path, start_port, end_port)

            if route_map:
                folium_map_html = route_map._repr_html_()
                route_info = {
                    'path': path,
                    'distance': f"{route_stats['total_distance']:.2f}",
                    'duration': f"{route_stats['sailing_days']} days {route_stats['sailing_hours']} hours",
                }
                return render_template('route.html', route_info=route_info, map_html=folium_map_html)
    flash('Welcome Aboard Captain', 'success')
    return render_template('index.html', ports=ports, route_info=route_info, map_html=folium_map_html)

@app.route('/aquanav/route', methods = ['GET', 'POST'])
def route():
    return render_template('route.html')
if __name__ == '__main__':
    app.run(debug=True)