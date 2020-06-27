from flask import Flask, render_template, url_for, request, redirect, jsonify
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from flask_bootstrap import Bootstrap

app = Flask(__name__)
Bootstrap(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///survey_app.db'
db = SQLAlchemy(app)

class Manager(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    firstname = db.Column(db.String(200), nullable=False)
    lastname = db.Column(db.String(200), nullable=False)
  
   
    date_created  = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return '<Manager %r>' % self.id


class Subordinate(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    firstname = db.Column(db.String(200), nullable=False)
    lastname = db.Column(db.String(200), nullable=False)
    email = db.Column(db.String(200), nullable=False)

    job_title= db.Column(db.String(200), nullable=False)
   
    date_created  = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return '<Subordinate %r>' % self.id





class Survey(db.Model):
    id = db.Column(db.Integer, primary_key=True)
   
    survey_id = db.Column(db.String(200), nullable=False)
  
    subordinate_id = db.Column(db.String(200), nullable=False)

    question = db.Column(db.String(200), nullable=False)
    question_type = db.Column(db.String(200), nullable=False)
    options = db.Column(db.String(200), nullable=False)
    
   
    date_created  = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return '<Survey %r>' % self.id


class Responses(db.Model):
    id = db.Column(db.Integer, primary_key=True)
  
    survey_id = db.Column(db.String(200), nullable=False)
   
   
    subordinate_id = db.Column(db.String(200), nullable=False)
    question = db.Column(db.String(200), nullable=False)
    question_type = db.Column(db.String(200), nullable=False)
    response = db.Column(db.String(200), nullable=False)
    
   
    date_created  = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return '<Responses %r>' % self.id


class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(200), nullable=False)
    date_created  = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return '<Task %r>' % self.id


        
@app.route('/admin', methods=['POST','GET'])
def admin():
    if request.method == 'POST':
        fn = request.form['first_name']
        ln = request.form['last_name']
        email = request.form['email']
        job_title = request.form['job_title']
        new_user = Subordinate(firstname=fn,lastname=ln,email=email,job_title=job_title)

        try:
            db.session.add(new_user)
            db.session.commit()
            return redirect('/admin')

        except:
            'There was an issue adding your user'
    
        
    else:
        subs = Subordinate.query.order_by(Subordinate.date_created).all()
        subs_count = Subordinate.query.filter(Subordinate.id != "").count()

        return render_template('admin.html', subs=subs , subs_count= subs_count)
        
      

@app.route('/', methods=['POST','GET'])
def index():
    if request.method == 'POST':
        task_content = request.form['content']
        new_task = Todo(content=task_content)

        try:
            db.session.add(new_task)
            db.session.commit()
            return redirect('/')

        except:
            'There was an issue adding your task'
    
        
    else:
        tasks = Todo.query.order_by(Todo.date_created).all()
        return render_template('index.html', tasks=tasks)

@app.route('/delete/<int:id>')
def delete(id):
    task_to_delete = Todo.query.get_or_404(id)

    try: 
        db.session.delete(task_to_delete)
        db.session.commit()
        return redirect('/')
    except:
        return 'There was a problem deleting that task'

@app.route('/update/<int:id>', methods=['GET','POST'])
def update(id):
    task = Todo.query.get_or_404(id)
    if request.method == 'POST':
        task.content = request.form['content']
        try:
            db.session.commit()
            return redirect('/')
        except:
            return 'There was an issue updating your task'
    else:
        return render_template('update.html', task=task)

if __name__ == "__main__":
    app.run(debug=True)