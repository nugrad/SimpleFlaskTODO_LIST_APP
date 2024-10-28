from flask import Flask,render_template,redirect,request,url_for
from flask_sqlalchemy import SQLAlchemy


app=Flask(__name__,template_folder='templates',static_folder='static',static_url_path='/')
app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///todo.db'
db=SQLAlchemy(app)

class TODO(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    text=db.Column(db.String(1000))
    complete=db.Column(db.Boolean)

    def __repr__(self):
        return self.text




@app.route('/')
def index():
    # return "<h1>Welcome to TODOLIST PROJECT</h1>"
    incomplete=TODO.query.filter_by(complete=False).all()
    complete=TODO.query.filter_by(complete=True).all()

    return render_template('index.html',complete=complete,incomplete=incomplete)

@app.route('/add',methods=['POST'])
def add():
    todo=TODO(text=request.form['todoitem'],complete=False)
    db.session.add(todo)
    db.session.commit()

    return redirect(url_for('index'))

@app.route('/complete<id>')
def complete(id):
    todo=TODO.query.filter_by(id=int(id)).first()
    todo.complete=True
    db.session.commit()

    return redirect(url_for('index'))






if __name__ =='__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)