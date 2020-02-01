from flask import Flask,render_template,request,redirect,url_for
from flask_sqlalchemy import SQLAlchemy



app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://username:passwd@127.0.0.1/data?charset=utf8'
app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app)

class Diary(db.Model):
    __tablename__ = 'student_diary'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(32), nullable=False)
    labels = db.Column(db.String(16), )
    source = db.Column(db.String(16), )
    userid = db.Column(db.String(16), )
    url = db.Column(db.String(128), nullable=False)
    realname = db.Column(db.String(16), nullable=False)
    aliasname = db.Column(db.String(16), nullable=False)
    words = db.Column(db.Text, )
    createTime = db.Column(db.String(32), nullable=False)


    def __repr__(self):
        return '<Post %r>' % self.title

@app.route('/')
@app.route('/<int:pg>/')
def index_diary(pg=None):
    if pg is None:
        pg = 1
    diary_list = Diary.query.paginate(page=pg, per_page=10)
    return  render_template('index.html', diary_list=diary_list)

@app.route('/detail/<int:id>/')
def diary_detail(id):
    '''查询id'''
    diary = Diary.query.get(id)
    return  render_template('diary_detail.html',diary=diary)

@app.route('/author/')
def find_by_author_2():
    '''查询name'''
    name=request.args.get("author_name")
    if (name == ''):
        return redirect(url_for('index_diary'))
    return  redirect(url_for('find_by_author', name=name, pg=1))

@app.route('/author/<name>/<int:pg>')
def find_by_author(name=None,pg=None):
    '''查询name'''
    if pg is None:
        pg = 1
    if (name is None):
        return redirect(url_for('index_diary'))
    Diary_temp = Diary.query.filter_by(realname=name)
    number = len(Diary_temp.all())
    diary_list = Diary_temp.paginate(page=pg, per_page=10)
    return  render_template("author.html", diary_list=diary_list, author_name=name, number=number)

if __name__ == '__main__':

    app.run(host='127.0.0.1', port=5000)