from app import app,db
from app.form import RegistrationForm
from flask_login import current_user, login_user, logout_user, login_required
from app.models import Registration, FurduModel
from flask import render_template,flash, redirect, url_for, request
from werkzeug.urls import url_parse
from datetime import datetime, date, time, timezone

@app.route("/",methods=['GET','POST'])
@app.route('/index', methods=['GET', 'POST'])
def index():
	form = RegistrationForm()
	if current_user.is_authenticated:
		return redirect(url_for('room'))
	if form.validate_on_submit():
		user = Registration.query.filter_by(username=form.username.data).first()
		if user is None or not user.check_password(form.password.data):
			flash('Invalid username or password')
			return redirect(url_for('index'))
		else:
			login_user(user, remember=form.remember_me.data)
			next_page = request.args.get('next')
			if not next_page or url_parse(next_page).netloc != '':
				flash(f'Welcome, {current_user}!')
				next_page = url_for('room')
			return redirect(next_page)
	return render_template('home.html', title='FurDU Room Counter Sign In', form=form)

@login_required
@app.route('/room',methods=['GET', 'POST'])
def room():
	if current_user.is_authenticated:
                data = db.session.query(FurduModel).filter(FurduModel.name == str(current_user))
		return render_template('room.html', title='FurDU Room Counter', roomslist=data)
                #do more stuff later
	else:
		return redirect(url_for('index'))

@app.route('/logout',methods=['GET', 'POST'])
def logout():
	logout_user()
	flash(f'Successfully logged out.')
	return redirect(url_for('index'))

@login_required
@app.route('/down/<roomname>',methods=['GET', 'POST'])
def down(roomname):
	if request.method == "POST":
		if request.form.get(f"userInput_{roomname}") == "True":
			room = db.session.query(FurduModel).filter(FurduModel.name == roomname).first()
			outsInt = room.outs += 1
			regform = FurduModel(name=f'{roomname}', ins=room.ins, outs=outsInt)
			db.session.delete(room)
			db.session.commit()
			db.session.add(regform)
			db.session.commit()
			flash(f'{roomname} - One person removed.')
			return redirect(url_for('room'))
		else:
			flash(f'{roomname} - Selection cancelled.')
			return redirect(url_for('room'))
	else:
		flash('Error. Input handling here. Code x002')
		return redirect(url_for('room'))

@login_required
@app.route('/up/<roomname>',methods=['GET', 'POST'])
def up(roomname):
	if request.method == "POST":
		if request.form.get(f"userInput_{roomname}") == "True":
			room = db.session.query(FurduModel).filter(FurduModel.name == roomname).first()
			insInt = room.ins += 1
			regform = FurduModel(name=f'{roomname}', ins=insInt, outs=room.outs)
			db.session.delete(room)
			db.session.commit()
			db.session.add(regform)
			db.session.commit()
			flash(f'{roomname} - One person added.')
			return redirect(url_for('room'))
		else:
			flash(f'{roomname} - Selection cancelled.')
			return redirect(url_for('room'))
	else:
		flash('Error. Input handling here. Code x004')
		return redirect(url_for('room'))

@login_required
@app.route('/reset/<roomname>',methods=['GET', 'POST'])
def up(roomname):
	if request.method == "POST":
		if request.form.get(f"userInput_{roomname}") == "True":
			room = db.session.query(FurduModel).filter(FurduModel.name == roomname).first()
			regform = FurduModel(name=f'{roomname}', ins=0, outs=0)
			db.session.delete(room)
			db.session.commit()
			db.session.add(regform)
			db.session.commit()
			flash(f'{roomname} - Data reset.')
			return redirect(url_for('room'))
		else:
			flash(f'{roomname} - Selection cancelled.')
			return redirect(url_for('room'))
	else:
		flash('Error. Input handling here. Code x006')
		return redirect(url_for('room'))
