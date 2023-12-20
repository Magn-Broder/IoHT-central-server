from flask import Flask, flash, redirect, url_for, render_template, request, session
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure
import models
import base64
import io

app = Flask(__name__)
app.secret_key = "r@nd0mSk_1"
DATABASE = 'database.db'

#######################################################################################################
@app.route("/")
def index():
    return redirect(url_for('login'))
#######################################################################################################
@app.route('/login', methods=["POST", "GET"])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        if models.check_user(username, password):
            session['username'] = username
            return redirect(url_for('home'))
        else:
            flash('Invalid username or password', 'error')
            return redirect(url_for('login'))

    return render_template('login.html')
#######################################################################################################
@app.route('/home', methods=['POST', "GET"])
def home():
    if 'username' in session:
        falls = models.query_fall_data()
        return render_template('home.html', falls=falls)
    else:
        return redirect(url_for('login'))
    
#######################################################################################################
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        first_name = request.form.get('firstname')
        last_name = request.form.get('lastname')
        username = request.form.get('username')
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')

        if models.register_user_to_db(first_name, last_name, username, password, confirm_password):
            flash('Registration successful', 'success')
            return redirect(url_for('login'))

    return render_template('register.html')
#######################################################################################################  
@app.route('/graph')
def graph():
    if 'username' in session:
        data = models.query_heart_data()

        timestamps = [row[0] for row in data]
        bpm_values = [row[1] for row in data]

        num_data_points = len(timestamps)
        responsive_percentage = 225*num_data_points

        fig = Figure(figsize=(responsive_percentage / 100, 6), dpi=100)
        ax = fig.add_subplot(111)

        ax.plot(timestamps, bpm_values, marker='o', linestyle='-', color='b')
        for i, (timestamp, bpm) in enumerate(zip(timestamps, bpm_values)):
            ax.text(timestamp, bpm, f'{bpm} BPM', ha='right', va='bottom', rotation=45, color='red')
        ax.set_title('Heart Data')
        ax.set_xlabel('Timestamp')
        ax.set_ylabel('BPM')
        ax.grid(True)

        img = io.BytesIO()
        FigureCanvas(fig).print_png(img)
        img.seek(0)

        graph_url = base64.b64encode(img.getvalue()).decode()

        return render_template('graph.html', graph=f'<img src="data:image/png;base64,{graph_url}" alt="Heart Data Graph">')
    else:
        return redirect(url_for('login'))

#######################################################################################################
@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))
#######################################################################################################

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80, debug=True)