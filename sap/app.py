import flask
from flask_mysqldb import MySQL
import base64
from werkzeug.utils import secure_filename
import os
from flask import Flask, render_template, request, jsonify, session


app = flask.Flask(__name__)

# MySQL configurations
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'Admin@123'
app.config['MYSQL_DB'] = 'sap'

app.config['UPLOAD_FOLDER'] = 'static/images'  # Changed path for the upload folder

mysql = MySQL(app)
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# Set secret key for session
app.secret_key = 'your_secret_key'



@app.route('/')
def home():
    return flask.render_template('ll.html')

@app.route('/login', methods=['POST'])
def login():
    username = flask.request.form['username']
    reg_no = flask.request.form['reg_no']

    # Create cursor
    cur = mysql.connection.cursor()

    # Verify user credentials in log_std table
    cur.execute("SELECT * FROM log_std WHERE username = %s AND reg_no = %s", (username, reg_no))
    user_std = cur.fetchone()

    # Verify user credentials in log_fac table
    cur.execute("SELECT * FROM log_fac WHERE username = %s AND pass = %s", (username, reg_no))
    user_fac = cur.fetchone()

    cur.close()

    if user_std:
        # Store username and reg_no in session
        flask.session['username'] = user_std[0]
        flask.session['reg_no'] = user_std[1]
        flask.flash('Login successful as Student!', 'success')
        return flask.redirect(flask.url_for('dashboard1'))
    elif user_fac:
        # Store username and reg_no in session
        flask.session['username'] = user_fac[0]
        flask.session['reg_no'] = user_fac[1]
        flask.flash('Login successful as Faculty!', 'success')
        return flask.redirect(flask.url_for('dashboard2'))
    else:
        flask.flash('Incorrect username or reg_no', 'error')
        return flask.redirect(flask.url_for('home'))

@app.route('/dashboard1')
def dashboard1():
    if 'username' in flask.session and 'reg_no' in flask.session:
        username = flask.session['username']
        reg_no = flask.session['reg_no']

        # Create cursor
        cur = mysql.connection.cursor()

        # Fetch user details from the database
        cur.execute("SELECT * FROM log_std WHERE username = %s AND reg_no = %s", (username, reg_no))
        user_data = cur.fetchone()

        cur.close()

        if user_data:
            # Assuming user_data[3] contains the image data as bytes
            image_data = base64.b64encode(user_data[3]).decode('utf-8') if user_data[3] else None

            user = {
                'username': user_data[0],  # Assuming username is at index 0
                'reg_no': user_data[1],  # Assuming reg_no is at index 1
                'dept': user_data[2],  # Assuming dept is at index 2
                'image_data': image_data
            }
            return flask.render_template('dashboard1.html', user=user)
        else:
            flask.flash('User not found in the database', 'error')
            return flask.redirect(flask.url_for('home'))
    else:
        flask.flash('Please log in first', 'error')
        return flask.redirect(flask.url_for('home'))

@app.route('/dashboard2')
def dashboard2():
    if 'username' in flask.session and 'reg_no' in flask.session:
        username = flask.session['username']
        reg_no = flask.session['reg_no']

        # Fetch user details from the database
        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM log_fac WHERE username = %s AND pass = %s", (username, reg_no))
        user_fac = cur.fetchone()
        cur.close()

        if user_fac:
            user = {
                'username': user_fac[0],
                'class': user_fac[3],
                'dept': user_fac[2],
            }
            # Pass user details to the template
            return flask.render_template('dashboard2.html', user=user)
        else:
            flask.flash('User not found in the database', 'error')
            return flask.redirect(flask.url_for('home'))
    else:
        flask.flash('Please log in first', 'error')
        return flask.redirect(flask.url_for('home'))


@app.route('/fac_verify', methods=['POST'])
def fac_verify():
    if 'username' in flask.session and 'reg_no' in flask.session:
        # Assuming the faculty member is logged in and their details are in session
        username = flask.session['username']
        reg_no = flask.session['reg_no']

        student_reg_no = flask.request.form.get('reg_no')



        cur = mysql.connection.cursor()

        cur.execute("SELECT * FROM log_std WHERE reg_no = %s", (student_reg_no,))
        student_data = cur.fetchone()

        cur.execute("SELECT * FROM paper WHERE username = %s AND reg_no = %s", (student_data[0], student_data[1]))
        paper_data = cur.fetchall()

        cur.execute("SELECT * FROM membership WHERE username = %s AND reg_no = %s", (student_data[0], student_data[1]))
        member_data = cur.fetchall()

        cur.execute("SELECT * FROM enterp WHERE username = %s AND reg_no = %s", (student_data[0], student_data[1]))
        enterp_data = cur.fetchall()

        cur.execute("SELECT * FROM social WHERE username = %s AND reg_no = %s", (student_data[0], student_data[1]))
        social_data = cur.fetchall()

        cur.execute("SELECT * FROM ipt WHERE username = %s AND reg_no = %s", (student_data[0], student_data[1]))
        ipt_data = cur.fetchall()

        cur.execute("SELECT * FROM gate WHERE username = %s AND reg_no = %s", (student_data[0], student_data[1]))
        gate_data = cur.fetchall()

        cur.execute("SELECT * FROM leader WHERE username = %s AND reg_no = %s", (student_data[0], student_data[1]))
        leader_data = cur.fetchall()

        cur.execute("SELECT * FROM online WHERE username = %s AND reg_no = %s", (student_data[0], student_data[1]))
        online_data = cur.fetchall()

        cur.execute("SELECT * FROM techno WHERE username = %s AND reg_no = %s", (student_data[0], student_data[1]))
        techno_data = cur.fetchall()

        cur.execute("SELECT * FROM project WHERE username = %s AND reg_no = %s", (student_data[0], student_data[1]))
        project_data = cur.fetchall()

        cur.execute("SELECT * FROM ppp WHERE username = %s AND reg_no = %s", (student_data[0], student_data[1]))
        ppp_data = cur.fetchall()

        cur.execute("SELECT * FROM games WHERE username = %s AND reg_no = %s", (student_data[0], student_data[1]))
        game_data = cur.fetchall()

        cur.close()

        if student_data:
            image_data = base64.b64encode(student_data[3]).decode('utf-8') if student_data[3] else None

            # Student found in the database, pass student and paper details to the template
            student = {
                'username': student_data[0],  # Assuming username is at index 0
                'reg_no': student_data[1],  # Assuming reg_no is at index 1
                'dept': student_data[2],  # Assuming dept is at index 2
                'image_data': image_data

            }


            # Pass paper details to the template
            papers = []  # Initialize an empty list for papers
            for paper in paper_data:
                papers.append({
                    'name_clg': paper[2],
                    'event': paper[3],
                    'date': paper[7],
                    'loc': paper[4],
                    'prize': paper[6],
                    'price':paper[8],
                    'proof': paper[5].decode('utf-8')  # Decode proof filename
                })
            ppps = []  # Initialize an empty list for papers
            for paper in ppp_data:
                ppps.append({
                    'name_clg': paper[2],
                    'event': paper[3],
                    'date': paper[4],
                    'loc': paper[5],
                    'act': paper[6],
                    'prize': paper[7],
                    'proof': paper[8].decode('utf-8')  # Decode proof filename
                })
            gamess = []  # Initialize an empty list for papers
            for paper in game_data:
                gamess.append({
                    'name_clg': paper[2],
                    'event': paper[3],
                    'date': paper[4],
                    'loc': paper[5],
                    'act': paper[6],
                    'prize': paper[7],
                    'proof': paper[8].decode('utf-8')  # Decode proof filename
                })
            technos = []  # Initialize an empty list for papers
            for paper in techno_data:
                technos.append({
                    'name_clg': paper[2],
                    'event': paper[3],
                    'date': paper[4],
                    'loc': paper[5],
                    'prize': paper[6],
                    'price':paper[7],
                    'proof': paper[8].decode('utf-8')  # Decode proof filename
                })
            projects = []  # Initialize an empty list for papers
            for paper in project_data:
                projects.append({
                    'name_clg': paper[2],
                    'event': paper[3],
                    'date': paper[4],
                    'loc': paper[5],
                    'prize': paper[6],
                    'price':paper[7],
                    'proof': paper[8].decode('utf-8')  # Decode proof filename
                })
            members = []  # Initialize an empty list for memberships
            for member in member_data:
                members.append({
                    'member': member[2],
                    'proof_n': member[3].decode('utf-8'),  # Decode proof filename
                    'proof_p': member[4].decode('utf-8'),  # Decode proof filename
                    'proof_c': member[5].decode('utf-8'),  # Decode proof filename
                    'prp': member[6],
                    'pr': member[7]
                })
            enterps = []  # Initialize an empty list for memberships
            for member in enterp_data:
                enterps.append({
                    'works': member[2],
                    'works_c': member[3],
                    'proof_w': member[4].decode('utf-8'),  # Decode proof filename
                    'release': member[5],
                    'release_c': member[6],
                    'proof_r': member[7].decode('utf-8'),  # Decode proof filename
                    'startup': member[8],
                    'stratup_c': member[9],
                    'proof_s': member[10].decode('utf-8'),  # Decode proof filename
                    'price': member[11]
                })
            socials = []  # Initialize an empty list for memberships
            for member in social_data:
                socials.append({
                    'bd': member[2],
                    'b_c': member[3],
                    'p_c': member[4].decode('utf-8'),  # Decode proof filename
                    'camp1': member[5],
                    'camp1_c': member[6],
                    'proof_camp1': member[7].decode('utf-8'),  # Decode proof filename
                    'camp2': member[8],
                    'camp2_c': member[9],
                    'proof_camp2': member[10].decode('utf-8'),  # Decode proof filename
                })
            ipts = []  # Initialize an empty list for papers
            for paper in ipt_data:
                ipts.append({
                    'written': paper[2],
                    'written_c': paper[3],
                    'proof': paper[4].decode('utf-8'),  # Decode proof filename
                    'place': paper[5]
                })
            gates = []  # Initialize an empty list for memberships
            for member in gate_data:
                gates.append({
                    'bd': member[2],
                    'b_c': member[3],
                    'p_c': member[4].decode('utf-8'),  # Decode proof filename
                    'camp1': member[5],
                    'camp1_c': member[6],
                    'proof_camp1': member[7].decode('utf-8'),  # Decode proof filename
                    'camp2': member[8],
                })
            leaders = []  # Initialize an empty list for memberships
            for member in leader_data:
                leaders.append({
                    'bd': member[2],
                    'b_c': member[3],
                    'p_c': member[4].decode('utf-8'),  # Decode proof filename
                    'camp1': member[5],
                    'camp1_c': member[6],
                    'proof_camp1': member[7].decode('utf-8'),  # Decode proof filename
                    'camp2': member[8],
                    'camp2_c': member[9],
                    'proof_camp2': member[10].decode('utf-8'),  # Decode proof filename
                    'camp3': member[11],
                    'camp3_c': member[12],
                    'proof_camp3': member[13].decode('utf-8'),  # Decode proof filename
                })

            onlines = []  # Initialize an empty list for memberships
            for member in online_data:
                onlines.append({
                    'bd': member[2],
                    'b_c': member[3],
                    'p_c': member[4].decode('utf-8'),  # Decode proof filename
                    'camp1': member[5],
                    'camp1_c': member[6],
                    'proof_camp1': member[7].decode('utf-8'),  # Decode proof filename
                    'camp2': member[8],
                    'camp2_c': member[9],
                    'proof_camp2': member[10].decode('utf-8'),  # Decode proof filename
                    'camp3': member[11],
                    'camp3_c': member[12],
                    'proof_camp3': member[13].decode('utf-8'),  # Decode proof filename
                })


            return flask.render_template('fac_verify.html', user=student, projects=projects, papers=papers, members=members, enterps=enterps, socials=socials, ipts=ipts, gates=gates, leaders=leaders, onlines=onlines, ppps=ppps, technos=technos, gamess=gamess)
        else:
            flask.flash('Student not found in the database', 'error')
            return flask.redirect(flask.url_for('dashboard2'))
    else:
        flask.flash('Please log in first', 'error')
        return flask.redirect(flask.url_for('home'))

@app.route('/process_data', methods=['POST','GET'])
def process_data():

    reg_no = flask.request.form.get('reg_n')


    checked_items = {}

    for id in range(1,13):
        checked_items[id] = flask.request.form.getlist(f'checkbox_{id}')

    #paper
    date_values = []
    prize_values = []
    for string_value in checked_items[1]:
        # Split the string into date and prize parts based on the "|" character
        split_values = string_value.split("|")
        # Append date and prize values to their respective lists
        date_values.append(split_values[0])
        prize_values.append(split_values[1])
    lep =len(date_values)
    for i in range(lep):
        cur = mysql.connection.cursor()
        cur.execute("UPDATE paper set verified = 1 where reg_no = %s AND date = %s AND prize = %s",(reg_no,date_values[i],prize_values[i]))
        mysql.connection.commit()
        cur.close()
    #project
    date_val = []
    prize_val = []
    for string_value in checked_items[2]:
        # Split the string into date and prize parts based on the "|" character
        split_values = string_value.split("|")
        # Append date and prize values to their respective lists
        date_val.append(split_values[0])
        prize_val.append(split_values[1])
    lepp =len(date_val)
    for i in range(lepp):
        cur = mysql.connection.cursor()
        cur.execute("UPDATE project set verified = 1 where reg_no = %s AND date = %s AND prize = %s",(reg_no,date_val[i],prize_val[i]))
        mysql.connection.commit()
        cur.close()
    #techno
    date_va = []
    prize_va = []
    for string_value in checked_items[3]:
        # Split the string into date and prize parts based on the "|" character
        split_values = string_value.split("|")
        # Append date and prize values to their respective lists
        date_va.append(split_values[0])
        prize_va.append(split_values[1])
    leth =len(date_va)
    for i in range(leth):
        cur = mysql.connection.cursor()
        cur.execute("UPDATE techno set verified = 1 where reg_no = %s AND date = %s AND prize = %s",(reg_no,date_va[i],prize_va[i]))
        mysql.connection.commit()
        cur.close()
    #games
    date_v = []
    prize_v = []
    for string_value in checked_items[4]:
        # Split the string into date and prize parts based on the "|" character
        split_values = string_value.split("|")
        # Append date and prize values to their respective lists
        date_v.append(split_values[0])
        prize_v.append(split_values[1])
    leg =len(date_v)
    for i in range(leg):
        cur = mysql.connection.cursor()
        cur.execute("UPDATE games set verified = 1 where reg_no = %s AND date = %s AND prize = %s",(reg_no,date_v[i],prize_v[i]))
        mysql.connection.commit()
        cur.close()
    #member
    """data_m =[]
    for string_value in checked_items[5]:
        split_values = split_values.split("")
        data_m.append(split_values[0])
    lem = len(data_m)
    for i in range(lem):
        cur = mysql.connection.cursor()
        cur.execute("UPDATE membership set verified = 1 where reg_no = %s AND member = %s",(reg_no,data_m[i]))
        mysql.connection.commit()
        cur.close()"""






    return render_template('total.html', student_reg_no=reg_no,pv=checked_items)

@app.route('/data' , methods=['POST'])
def data():
    return 'aa'






@app.route('/paper', methods=['POST','GET'])  # Changed method to methods
def paper():
    if 'username' in flask.session:
        username = flask.session['username']
        reg_no = flask.session['reg_no']
        if flask.request.method == 'POST':
            # Get form data from the request
            name_clg = flask.request.form.get('clg_name')
            event = flask.request.form.get('event')
            date = flask.request.form.get('date')
            loc = flask.request.form.get('location')
            prize = flask.request.form.get('prize')
            price = flask.request.form.get('price')
            proof = flask.request.files['proof']
            temp =0

            # Check if the file is empty
            if proof.filename == '':
                flask.flash('No file selected', 'error')
                return flask.redirect(flask.url_for('dashboard1'))  # Changed to dashboard1

            # Save the uploaded file to the 'UPLOAD_FOLDER' directory
            filename = secure_filename(proof.filename)
            proof.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

            # Open a cursor to perform database operations
            cur = mysql.connection.cursor()

            # Insert form data into the database
            cur.execute("INSERT INTO paper (username, reg_no, name_clg, event, date, loc, proof, prize, price,verified) VALUES (%s, %s, %s, %s, %s, %s, %s,%s,%s,%s)",
                        (username, reg_no, name_clg, event, date, loc, filename, prize, price,temp))

            # Commit changes to the database
            mysql.connection.commit()
            cur.close()

            flask.flash('Sap record submitted successfully!', 'success')
            return flask.redirect(flask.url_for('next_page'))
        return flask.render_template('paper.html')
    else:
        # User is not logged in, redirect to the home page
        flask.flash('You must login first', 'error')
        return flask.redirect(flask.url_for('login'))

@app.route('/ppp', methods=['POST','GET'])  # Changed method to methods
def ppp():
    if 'username' in flask.session:
        username = flask.session['username']
        reg_no = flask.session['reg_no']
        if flask.request.method == 'POST':
            # Get form data from the request
            name_clg = flask.request.form.get('clg_name')
            event = flask.request.form.get('event')
            date = flask.request.form.get('date')
            loc = flask.request.form.get('radio')
            act = flask.request.form.get('radio3')
            prize = flask.request.form.get('radio1')
            proof = flask.request.files['proof']
            temp=0

            # Check if the file is empty
            if proof.filename == '':
                flask.flash('No file selected', 'error')
                return flask.redirect(flask.url_for('dashboard1'))  # Changed to dashboard1

            # Save the uploaded file to the 'UPLOAD_FOLDER' directory
            filename = secure_filename(proof.filename)
            proof.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

            # Open a cursor to perform database operations
            cur = mysql.connection.cursor()

            # Insert form data into the database
            cur.execute("INSERT INTO ppp (username, reg_no, name_clg, event, date, loc, act, proof, prize,verified) VALUES (%s, %s, %s, %s, %s, %s, %s,%s,%s,%s)",
                        (username, reg_no, name_clg, event, date, loc, act, filename, prize,temp))

            # Commit changes to the database
            mysql.connection.commit()
            cur.close()

            flask.flash('Sap record submitted successfully!', 'success')
            return flask.redirect(flask.url_for('next_page'))
        return flask.render_template('ppp.html')
    else:
        # User is not logged in, redirect to the home page
        flask.flash('You must login first', 'error')
        return flask.redirect(flask.url_for('login'))

@app.route('/games', methods=['POST','GET'])  # Changed method to methods
def games():
    if 'username' in flask.session:
        username = flask.session['username']
        reg_no = flask.session['reg_no']
        if flask.request.method == 'POST':
            # Get form data from the request
            name_clg = flask.request.form.get('clg_name')
            event = flask.request.form.get('event')
            date = flask.request.form.get('date')
            loc = flask.request.form.get('radio')
            act = flask.request.form.get('radio3')
            prize = flask.request.form.get('radio1')
            proof = flask.request.files['proof']
            temp=0

            # Check if the file is empty
            if proof.filename == '':
                flask.flash('No file selected', 'error')
                return flask.redirect(flask.url_for('dashboard1'))  # Changed to dashboard1

            # Save the uploaded file to the 'UPLOAD_FOLDER' directory
            filename = secure_filename(proof.filename)
            proof.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

            # Open a cursor to perform database operations
            cur = mysql.connection.cursor()

            # Insert form data into the database
            cur.execute("INSERT INTO games (username, reg_no, name_clg, event, date, loc, act, proof, prize,verified) VALUES (%s,%s, %s, %s, %s, %s, %s, %s,%s,%s)",
                        (username, reg_no, name_clg, event, date, loc, act, filename, prize,temp))

            # Commit changes to the database
            mysql.connection.commit()
            cur.close()

            flask.flash('Sap record submitted successfully!', 'success')
            return flask.redirect(flask.url_for('next_page'))
        return flask.render_template('games.html')
    else:
        # User is not logged in, redirect to the home page
        flask.flash('You must login first', 'error')
        return flask.redirect(flask.url_for('login'))

@app.route('/member', methods=['POST', 'GET'])
def member():
    if 'username' in flask.session:
        username = flask.session['username']
        reg_no = flask.session['reg_no']
        if flask.request.method == 'POST':
            member = flask.request.form.getlist('member')
            proof_n = flask.request.files['proof_n']
            proof_p = flask.request.files['proof_professional_society']
            proof_c = flask.request.files['proof_clubs']
            prp = flask.request.form.get('prp')
            pr = flask.request.form.get('proof_club')
            temp=0


            if proof_n.filename == '' and proof_p.filename == '' and proof_c.filename == '':
                flask.flash('No file selected', 'error')
                return flask.redirect(flask.url_for('dashboard1'))

            filename1 = secure_filename(proof_n.filename)
            proof_n.save(os.path.join(app.config['UPLOAD_FOLDER'], filename1))
            filename2 = secure_filename(proof_p.filename)
            proof_p.save(os.path.join(app.config['UPLOAD_FOLDER'], filename2))
            filename3 = secure_filename(proof_c.filename)
            proof_c.save(os.path.join(app.config['UPLOAD_FOLDER'], filename3))

            cur = mysql.connection.cursor()

            cur.execute("INSERT INTO membership (username, reg_no, member, proof_n, proof_p, proof_c, prp,pr,verified) VALUES (%s,%s, %s, %s, %s, %s, %s, %s,%s)",
                        (username, reg_no, ', '.join(member), filename1, filename2, filename3, prp,pr,temp))

            # Commit changes to the database
            mysql.connection.commit()
            cur.close()

            flask.flash('Sap record submitted successfully!', 'success')
            return flask.redirect(flask.url_for('next_page'))
        return flask.render_template('member.html')
    else:
        flask.flash('You must login first', 'error')
        return flask.redirect(flask.url_for('login'))


@app.route('/enterp', methods=['POST', 'GET'])
def enterp():
    if 'username' in flask.session:
        username = flask.session['username']
        reg_no = flask.session['reg_no']
        if flask.request.method == 'POST':
            # Retrieve form data using correct methods
            work_att = flask.request.form.getlist('checkbox1')
            w_c = flask.request.form.get('workshop_attended')  # Corrected method from request.form.get[]
            proof_w = flask.request.files['myfile1']
            startup = flask.request.form.getlist('checkbox2')
            R_c = flask.request.form.get('registered_for_start_up')  # Corrected method from request.form.get[]
            proof_s = flask.request.files['myfile2']
            release_p = flask.request.form.getlist('checkbox3')
            p_c = flask.request.form.get('released_product')  # Corrected method from request.form.get[]
            proof_pr = flask.request.files['myfile3']
            price_money = flask.request.form.get('price')  # Corrected method from request.form.get[]
            temp=0


            if proof_w.filename == '' or proof_s.filename == '' or proof_pr.filename == '':
                flask.flash('Please upload all required files', 'error')
                return flask.redirect(flask.url_for('enterp'))  # Redirect to the same page if files are missing

            # Save uploaded files to the UPLOAD_FOLDER directory
            filename1 = secure_filename(proof_w.filename)
            proof_w.save(os.path.join(app.config['UPLOAD_FOLDER'], filename1))
            filename2 = secure_filename(proof_s.filename)
            proof_s.save(os.path.join(app.config['UPLOAD_FOLDER'], filename2))
            filename3 = secure_filename(proof_pr.filename)
            proof_pr.save(os.path.join(app.config['UPLOAD_FOLDER'], filename3))

            cur = mysql.connection.cursor()

            # Insert form data into the database
            cur.execute("INSERT INTO enterp (username, reg_no, workshop, workshop_count, proof_workshop, release_pro, wrelease_pro_count, proof_release_pro, startups, startup_count, proof_startup, price_money,verified) VALUES (%s,%s, %s, %s, %s, %s, %s, %s,%s,%s, %s, %s, %s)",
                        (username, reg_no, ','.join(work_att), w_c, filename1, ','.join(release_p), p_c, filename3, ','.join(startup), R_c, filename2, price_money,temp))

            # Commit changes to the database
            mysql.connection.commit()
            cur.close()

            flask.flash('Sap record submitted successfully!', 'success')
            return flask.redirect(flask.url_for('next_page'))
        return flask.render_template('enterp.html')
    else:
        flask.flash('You must log in first', 'error')
        return flask.redirect(flask.url_for('login'))

@app.route('/social', methods=['POST', 'GET'])
def social():
    if 'username' in flask.session:
        username = flask.session['username']
        reg_no = flask.session['reg_no']
        if flask.request.method == 'POST':
            # Retrieve form data using correct methods
            blood = flask.request.form.getlist('checkbox1')
            blood_c = flask.request.form.get('blood_donation')  # Corrected method from request.form.get[]
            proof_blood = flask.request.files['myfile1']
            camp1 = flask.request.form.getlist('checkbox2')
            camp1_c = flask.request.form.get('NSS/NCC_1camp')  # Corrected method from request.form.get[]
            proof_camp1 = flask.request.files['myfile2']
            camp2 = flask.request.form.getlist('checkbox3')
            camp2_c = flask.request.form.get('NSS/NCC_2Camp')  # Corrected method from request.form.get[]
            proof_camp2 = flask.request.files['myfile3']
            temp=0


            if proof_blood.filename == '' or proof_camp1.filename == '' or proof_camp2.filename == '':
                flask.flash('Please upload all required files', 'error')
                return flask.redirect(flask.url_for('social'))  # Redirect to the same page if files are missing

            # Save uploaded files to the UPLOAD_FOLDER directory
            filename1 = secure_filename(proof_blood.filename)
            proof_blood.save(os.path.join(app.config['UPLOAD_FOLDER'], filename1))
            filename2 = secure_filename(proof_camp1.filename)
            proof_camp1.save(os.path.join(app.config['UPLOAD_FOLDER'], filename2))
            filename3 = secure_filename(proof_camp2.filename)
            proof_camp2.save(os.path.join(app.config['UPLOAD_FOLDER'], filename3))

            cur = mysql.connection.cursor()

            # Insert form data into the database
            cur.execute("INSERT INTO social (username, reg_no, blood_donation, blood_c, proof_b, camp1, camp1_c, proof_camp1, camp2, camp2_c, proof_camp2,verified) VALUES (%s,%s, %s, %s, %s, %s, %s, %s,%s,%s, %s, %s)",
                        (username, reg_no, ','.join(blood), blood_c, filename1, ','.join(camp1), camp1_c, filename2, ','.join(camp2), camp2_c, filename3,temp))

            # Commit changes to the database
            mysql.connection.commit()
            cur.close()

            flask.flash('Sap record submitted successfully!', 'success')
            return flask.redirect(flask.url_for('next_page'))
        return flask.render_template('social.html')
    else:
        flask.flash('You must log in first', 'error')
        return flask.redirect(flask.url_for('login'))

@app.route('/ipt', methods=['POST','GET'])  # Changed method to methods
def ipt():
    if 'username' in flask.session:
        username = flask.session['username']
        reg_no = flask.session['reg_no']
        if flask.request.method == 'POST':
            # Get form data from the request
            written = flask.request.form.getlist('checkbox1')
            written_c = flask.request.form.get('blood_donation')  # Corrected method from request.form.get[]
            proof_written = flask.request.files['myfile1']
            place = flask.request.form.get('radio1')
            temp=0


            # Check if the file is empty
            if proof_written.filename == '':
                flask.flash('No file selected', 'error')
                return flask.redirect(flask.url_for('dashboard1'))  # Changed to dashboard1

            # Save the uploaded file to the 'UPLOAD_FOLDER' directory
            filename = secure_filename(proof_written.filename)
            proof_written.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

            # Open a cursor to perform database operations
            cur = mysql.connection.cursor()

            # Insert form data into the database
            cur.execute("INSERT INTO ipt (username, reg_no, written, written_c, proof_written, place,verified) VALUES (%s, %s,%s, %s, %s, %s, %s)",
                        (username, reg_no, written, written_c, filename, place,temp))

            # Commit changes to the database
            mysql.connection.commit()
            cur.close()

            flask.flash('Sap record submitted successfully!', 'success')
            return flask.redirect(flask.url_for('next_page'))
        return flask.render_template('ipt.html')
    else:
        # User is not logged in, redirect to the home page
        flask.flash('You must login first', 'error')
        return flask.redirect(flask.url_for('login'))

@app.route('/gate', methods=['POST', 'GET'])
def gate():
    if 'username' in flask.session:
        username = flask.session['username']
        reg_no = flask.session['reg_no']
        if flask.request.method == 'POST':
            # Retrieve form data using correct methods
            appeared = flask.request.form.getlist('checkbox1')
            appeared_c = flask.request.form.get('appeared')  # Corrected method from request.form.get[]
            appeared_proof = flask.request.files['myfile1']
            Qualified = flask.request.form.getlist('checkbox2')
            Qualified_c = flask.request.form.get('NSS/NCC_1camp')  # Corrected method from request.form.get[]
            proof_Qualified = flask.request.files['myfile2']
            camp20 = flask.request.form.getlist('checkbox3')
            temp=0



            if appeared_proof.filename == '' or proof_Qualified.filename == '':
                flask.flash('Please upload all required files', 'error')
                return flask.redirect(flask.url_for('gate'))  # Redirect to the same page if files are missing

            # Save uploaded files to the UPLOAD_FOLDER directory
            filename1 = secure_filename(appeared_proof.filename)
            appeared_proof.save(os.path.join(app.config['UPLOAD_FOLDER'], filename1))
            filename2 = secure_filename(proof_Qualified.filename)
            proof_Qualified.save(os.path.join(app.config['UPLOAD_FOLDER'], filename2))


            cur = mysql.connection.cursor()

            # Insert form data into the database
            cur.execute("INSERT INTO gate (username, reg_no, appeared, appeared_c, appeared_proof, Qualified, Qualified_c, proof_Qualified, camp20,verified) VALUES (%s, %s, %s, %s,%s, %s, %s, %s,%s,%s)",
                        (username, reg_no, ','.join(appeared), appeared_c, filename1, ','.join(Qualified), Qualified_c, filename2, ','.join(camp20),temp))

            # Commit changes to the database
            mysql.connection.commit()
            cur.close()

            flask.flash('Sap record submitted successfully!', 'success')
            return flask.redirect(flask.url_for('next_page'))
        return flask.render_template('gate.html')
    else:
        flask.flash('You must log in first', 'error')
        return flask.redirect(flask.url_for('login'))

@app.route('/leader', methods=['POST', 'GET'])
def leader():
    if 'username' in flask.session:
        username = flask.session['username']
        reg_no = flask.session['reg_no']
        if flask.request.method == 'POST':
            # Retrieve form data using correct methods
            blood = flask.request.form.getlist('checkbox1')
            blood_c = flask.request.form.get('high_position')  # Corrected method from request.form.get[]
            proof_blood = flask.request.files['myfile1']
            camp1 = flask.request.form.getlist('checkbox2')
            camp1_c = flask.request.form.get('2nd_high_position')  # Corrected method from request.form.get[]
            proof_camp1 = flask.request.files['myfile2']
            camp2 = flask.request.form.getlist('checkbox3')
            camp2_c = flask.request.form.get('executive_member')  # Corrected method from request.form.get[]
            proof_camp2 = flask.request.files['myfile3']
            camp3 = flask.request.form.getlist('checkbox3')
            camp3_c = flask.request.form.get('coordinators')  # Corrected method from request.form.get[]
            proof_camp3 = flask.request.files['myfile4']
            temp=0



            if proof_blood.filename == '' or proof_camp1.filename == '' or proof_camp2.filename == '' or proof_camp3.filename == '':
                flask.flash('Please upload all required files', 'error')
                return flask.redirect(flask.url_for('leader'))  # Redirect to the same page if files are missing

            # Save uploaded files to the UPLOAD_FOLDER directory
            filename1 = secure_filename(proof_blood.filename)
            proof_blood.save(os.path.join(app.config['UPLOAD_FOLDER'], filename1))
            filename2 = secure_filename(proof_camp1.filename)
            proof_camp1.save(os.path.join(app.config['UPLOAD_FOLDER'], filename2))
            filename3 = secure_filename(proof_camp2.filename)
            proof_camp2.save(os.path.join(app.config['UPLOAD_FOLDER'], filename3))
            filename4 = secure_filename(proof_camp2.filename)
            proof_camp2.save(os.path.join(app.config['UPLOAD_FOLDER'], filename4))

            cur = mysql.connection.cursor()

            # Insert form data into the database
            cur.execute("INSERT INTO leader (username, reg_no, high_position, high_c, proof_h, camp10, camp10_c, proof_camp10, camp21, camp21_c, proof_camp21, camp22, camp22_c, proof_camp22,verified) VALUES (%s, %s, %s,%s, %s, %s, %s, %s,%s,%s, %s, %s,%s, %s, %s)",
                        (username, reg_no, ','.join(blood), blood_c, filename1, ','.join(camp1), camp1_c, filename2, ','.join(camp2), camp2_c, filename3, ','.join(camp3), camp3_c, filename4,temp))

            # Commit changes to the database
            mysql.connection.commit()
            cur.close()

            flask.flash('Sap record submitted successfully!', 'success')
            return flask.redirect(flask.url_for('next_page'))
        return flask.render_template('leader.html')
    else:
        flask.flash('You must log in first', 'error')
        return flask.redirect(flask.url_for('login'))

@app.route('/online', methods=['POST', 'GET'])
def online():
    if 'username' in flask.session:
        username = flask.session['username']
        reg_no = flask.session['reg_no']
        if flask.request.method == 'POST':
            # Retrieve form data using correct methods
            blood = flask.request.form.getlist('vac')
            blood_c = flask.request.form.get('vac1')  # Corrected method from request.form.get[]
            proof_blood = flask.request.files['myfile1']
            camp1 = flask.request.form.getlist('one_credit')
            camp1_c = flask.request.form.get('one_credit1')  # Corrected method from request.form.get[]
            proof_camp1 = flask.request.files['myfile2']
            camp2 = flask.request.form.getlist('two_credit')
            camp2_c = flask.request.form.get('two_credit2')  # Corrected method from request.form.get[]
            proof_camp2 = flask.request.files['myfile3']
            camp3 = flask.request.form.getlist('three_credits')
            camp3_c = flask.request.form.get('three_credits3')  # Corrected method from request.form.get[]
            proof_camp3 = flask.request.files['myfile4']
            temp=0


            if proof_blood.filename == '' or proof_camp1.filename == '' or proof_camp2.filename == '' or proof_camp3.filename == '':
                flask.flash('Please upload all required files', 'error')
                return flask.redirect(flask.url_for('leader'))  # Redirect to the same page if files are missing

            # Save uploaded files to the UPLOAD_FOLDER directory
            filename1 = secure_filename(proof_blood.filename)
            proof_blood.save(os.path.join(app.config['UPLOAD_FOLDER'], filename1))
            filename2 = secure_filename(proof_camp1.filename)
            proof_camp1.save(os.path.join(app.config['UPLOAD_FOLDER'], filename2))
            filename3 = secure_filename(proof_camp2.filename)
            proof_camp2.save(os.path.join(app.config['UPLOAD_FOLDER'], filename3))
            filename4 = secure_filename(proof_camp2.filename)
            proof_camp2.save(os.path.join(app.config['UPLOAD_FOLDER'], filename4))

            cur = mysql.connection.cursor()

            # Insert form data into the database
            cur.execute("INSERT INTO online (username, reg_no, Value, Value_c, proof_Value, camp15, camp15_c, proof_camp15, camp25, camp25_c, proof_camp25, camp23, camp23_c, proof_camp23,verified) VALUES (%s, %s, %s, %s,%s, %s, %s, %s,%s,%s, %s, %s,%s, %s, %s)",
                        (username, reg_no, ','.join(blood), blood_c, filename1, ','.join(camp1), camp1_c, filename2, ','.join(camp2), camp2_c, filename3, ','.join(camp3), camp3_c, filename4,temp))

            # Commit changes to the database
            mysql.connection.commit()
            cur.close()

            flask.flash('Sap record submitted successfully!', 'success')
            return flask.redirect(flask.url_for('next_page'))
        return flask.render_template('online.html')
    else:
        flask.flash('You must log in first', 'error')
        return flask.redirect(flask.url_for('login'))

@app.route('/techno', methods=['POST','GET'])  # Changed method to methods
def techno():
    if 'username' in flask.session:
        username = flask.session['username']
        reg_no = flask.session['reg_no']
        if flask.request.method == 'POST':
            # Get form data from the request
            name_clg = flask.request.form.get('clg_name')
            event = flask.request.form.get('event')
            date = flask.request.form.get('date')
            loc = flask.request.form.get('location')
            prize = flask.request.form.get('prize')
            price = flask.request.form.get('price')
            proof = flask.request.files['proof']
            temp=0



            # Check if the file is empty
            if proof.filename == '':
                flask.flash('No file selected', 'error')
                return flask.redirect(flask.url_for('dashboard1'))  # Changed to dashboard1

            # Save the uploaded file to the 'UPLOAD_FOLDER' directory
            filename = secure_filename(proof.filename)
            proof.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

            # Open a cursor to perform database operations
            cur = mysql.connection.cursor()

            # Insert form data into the database
            cur.execute("INSERT INTO techno (username, reg_no, name_clg, event, date, loc, proof, prize, price,verified) VALUES (%s, %s, %s, %s, %s, %s,%s, %s,%s,%s)",
                        (username, reg_no, name_clg, event, date, loc, filename, prize, price,temp))

            # Commit changes to the database
            mysql.connection.commit()
            cur.close()

            flask.flash('Sap record submitted successfully!', 'success')
            return flask.redirect(flask.url_for('next_page'))
        return flask.render_template('techno.html')
    else:
        # User is not logged in, redirect to the home page
        flask.flash('You must login first', 'error')
        return flask.redirect(flask.url_for('login'))

@app.route('/project', methods=['POST','GET'])  # Changed method to methods
def project():
    if 'username' in flask.session:
        username = flask.session['username']
        reg_no = flask.session['reg_no']
        if flask.request.method == 'POST':
            # Get form data from the request
            name_clg = flask.request.form.get('clg_name')
            event = flask.request.form.get('event')
            date = flask.request.form.get('date')
            loc = flask.request.form.get('location')
            prize = flask.request.form.get('prize')
            price = flask.request.form.get('price')
            proof = flask.request.files['proof']
            temp=0



            # Check if the file is empty
            if proof.filename == '':
                flask.flash('No file selected', 'error')
                return flask.redirect(flask.url_for('dashboard1'))  # Changed to dashboard1

            # Save the uploaded file to the 'UPLOAD_FOLDER' directory
            filename = secure_filename(proof.filename)
            proof.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

            # Open a cursor to perform database operations
            cur = mysql.connection.cursor()

            # Insert form data into the database
            cur.execute("INSERT INTO project (username, reg_no, name_clg, event, date, loc, proof, prize, price,verified) VALUES (%s, %s, %s, %s, %s, %s, %s,%s,%s,%s)",
                        (username, reg_no, name_clg, event, date, loc, filename, prize, price,temp))

            # Commit changes to the database
            mysql.connection.commit()
            cur.close()

            flask.flash('Sap record submitted successfully!', 'success')
            return flask.redirect(flask.url_for('next_page'))
        return flask.render_template('project.html')
    else:
        # User is not logged in, redirect to the home page
        flask.flash('You must login first', 'error')
        return flask.redirect(flask.url_for('login'))


@app.route('/next_page', methods=['GET'])
def next_page():
    # Check if data was stored successfully
    stored_successfully = flask.session.get('stored_successfully', True)

    # Clear the session variable to prevent showing the message again on page refresh
    flask.session.pop('stored_successfully', None)

    # Render the next_page template with the appropriate message
    return flask.render_template('next_page.html', stored_successfully=stored_successfully)



@app.route('/logout')
def logout():
    # Clear session data
    flask.session.clear()
    flask.flash('You have been logged out', 'info')
    return flask.redirect(flask.url_for('home'))



if __name__ == '__main__':
    app.run(debug=True)
