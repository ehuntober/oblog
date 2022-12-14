
from flask_blog import app
from flask import request , redirect, url_for, render_template,flash,session

from flask_blog import db
from flask_blog.models import Entry ,db

#decorator for login in
from functools import wraps

def login_required(view):
    @wraps(view)
    def inner(*args,**kwargs):
        if not session.get('logged_in'):
            return redirect(url_for('login'))
        return view(*args,**kwargs)
    return inner



@app.route('/')
@login_required
def show_entries():
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    entries = Entry.query.order_by(Entry.id.desc()).all()
    return render_template('entries/index.html',entries=entries)

@app.route('/entries/new', methods=['GET'])
@login_required
def new_entry():
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    return render_template('entries/new.html')



@app.route('/entries', methods=['POST'])
@login_required
def add_entry():
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    entry = Entry(
        title=request.form['title'],
        text=request.form['text']
    )
    db.session.add(entry)
    db.session.commit()
    flash('A new article has been created.')
    return redirect(url_for('show_entries'))

@app.route('/entries/<int:id>', methods=['GET'])
@login_required
def show_entry(id):
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    entry = Entry.query.get(id)
    return render_template('entries/show.html', entry=entry)

@app.route('/entries/<int:id>/edit', methods=['GET'])
@login_required
def edit_entry(id):
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    entry = Entry.query.get(id)
    return render_template('entries/edit.html', entry=entry)

@app.route('/entries/<int:id>/update', methods=['POST'])
@login_required
def update_entry(id):
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    entry = Entry.query.get(id)
    entry.title = request.form['title']
    entry.text = request.form['text']
    db.session.merge(entry)
    db.session.commit()
    flash('Article Updated.')
    return redirect(url_for('show_entries'))

@app.route('/entries/<int:id>/delete', methods=['POST'])
@login_required
def delete_entry(id):
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    entry = Entry.query.get(id)
    db.session.delete(entry)
    db.session.commit()
    flash('Article Deleted.')
    return redirect(url_for('show_entries'))


@app.route('/login',methods=['GET','POST'])
def login():
    error = None
    if request.method == 'POST':
        if request.form['username'] !=app.config['USERNAME']:
            flash('User name is different')
        elif request.form['password'] != app.config['PASSWORD']:
            flash('Password is different')
        else:
            session['logged_in'] = True
            flash('Login successful')
            return redirect(url_for('show_entries'))
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('logged_in',None)
    flash('Logged Out')
    return redirect(url_for('show_entries'))

@app.errorhandler(404)
def non_existant_route(error):
    return redirect(url_for('login'))
