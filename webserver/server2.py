
import os
from sqlalchemy import *
from sqlalchemy.pool import NullPool
from flask import Flask, request, render_template, g, redirect, Response
import functools

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from werkzeug.security import check_password_hash, generate_password_hash

tmpl_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'templates')
app = Flask(__name__, template_folder=tmpl_dir)


DB_USER = "xz2737"
DB_PASSWORD = "8oq53lu0"
DB_SERVER = "w4111.cisxo09blonu.us-east-1.rds.amazonaws.com"
DATABASEURI = "postgresql://"+DB_USER+":"+DB_PASSWORD+"@"+DB_SERVER+"/w4111"
engine = create_engine(DATABASEURI)


engine.execute("""DROP TABLE IF EXISTS user1;""")
engine.execute("""CREATE TABLE IF NOT EXISTS user1 (
  id int,
  username text,
  password text
);""")
engine.execute("""INSERT INTO user1(id,username) VALUES (1,'qq'), (2,'ww'), (3,'ee');""")







@app.before_request
def before_request():

  try:
    g.conn = engine.connect()
  except:
    print "uh oh, problem connecting to database"
    import traceback; traceback.print_exc()
    g.conn = None

@app.teardown_request
def teardown_request(exception):
 
  try:
    g.conn.close()
  except Exception as e:
    pass




@app.route('/return3')
def return3():
  return redirect('/')
@app.route('/return2')
def return2():
  return redirect('/indexlogin')

@app.route('/numberhelp')
def numberhelp():
  cursor = g.conn.execute("SELECT count(number) FROM Photo")
  return render_template("numberhelp.html", data = cursor)


@app.route('/loginpage')
def loginpage():
  return render_template("login.html")
@app.route('/registerpage')
def registerpage():
  return render_template("register.html")
@app.route('/addphotopage')
def addphotopage():
  return render_template("addphoto.html")
@app.route('/createatlaspage')
def createatlaspage():
  return render_template("createatlas.html")




@app.route('/<aname>/atlas', methods=('GET', 'POST'))
def atlas(aname):
  cmd = 'select * from photo where aname = (:name1)';
  w1 = g.conn.execute(text(cmd) ,name1 = aname);
  return render_template('user.html', data=w1)


@app.route('/hotatlas', methods=('GET', 'POST'))
def hotatlas():
  cmd = 'select * from photo where aname = (select aname from photo group by aname order by count(number) desc limit 1)';
  w1 = g.conn.execute(text(cmd));
  return render_template('hotatlas.html', data=w1)


@app.route('/add', methods=['POST'])
def add():
  name = request.form['name']
  number = request.form['number']
  cmd = 'INSERT INTO user1(id,username) VALUES (:numbers,:name1)';
  g.conn.execute(text(cmd),numbers = number,name1 = name);
  return redirect('/')

@app.route('/')
def index():
  cursor = g.conn.execute("SELECT * FROM Photo order by number desc")
  return render_template("index.html", data = cursor)

@app.route('/indexlogin')
def indexlogin():
  cursor = g.conn.execute("SELECT * FROM Photo order by number desc")
  return render_template("indexlogin.html", data = cursor)

@app.route('/<nickname>/user', methods=('GET', 'POST'))
def user(nickname):
  cmd = 'select * from photo inner join users on photo.nickname = users.nickname where photo.nickname = (:name1)';
  w1 = g.conn.execute(text(cmd) ,name1 = nickname);
  return render_template('user.html', data=w1)

@app.route('/<nickname>/user2', methods=('GET', 'POST'))
def userlogin(nickname):
  cmd = 'select * from photo inner join users on photo.nickname = users.nickname where photo.nickname = (:name1)';
  w1 = g.conn.execute(text(cmd) ,name1 = nickname);
  return render_template('userlogin.html', data=w1)

@app.route('/<nickname>/photo', methods=('GET', 'POST'))
def detail(nickname):
  cmd = 'select * from photo where number = (:name1)';
  w1 = g.conn.execute(text(cmd) ,name1 = nickname);
  return render_template('photos.html', data=w1)

@app.route('/<nickname>/photo2', methods=('GET', 'POST'))
def detaillogin(nickname):
  cmd = 'select * from photo where number = (:name1)';
  w1 = g.conn.execute(text(cmd) ,name1 = nickname);
  return render_template('photoslogin.html', data=w1)

@app.route('/search', methods=['POST'])
def search():
  search = request.form['search']
  cmd = 'select * from user1 where username = search';
  g.conn.execute(text(cmd));
  return redirect('/')

@app.route('/hello')
def hello():
  return 'Hello, World!'



@app.route('/login', methods=['POST'])
def login():
  username = request.form['name']
  password = request.form['number']
  cmd = 'select * from users where nickname = (:name1)';
  user = g.conn.execute(text(cmd) ,name1 = username);
  for i in user:
    if i['password'] == password:
      return redirect('/indexlogin')
  return render_template("login name.html") 

@app.route('/login2', methods=['POST'])
def login2():
  username = request.form['name']
  password = request.form['number']
  age = request.form['age']
  gender = request.form['gender']
  uname = request.form['uname']
  nationnality = request.form['nationnality']
  cmd = 'select password from users where nickname =  (:name1)';
  user = g.conn.execute(text(cmd),name1 = username).fetchone();
  if user is not None:
    return render_template("register wrong.html")
  else:
    cmd = 'INSERT INTO users(nickname,password,age,gender,uname,nationnality) VALUES (:a,:b,:c,:d,:e,:f)';
    g.conn.execute(text(cmd),a = username,b = password,c=age,d=gender,e=uname,f=nationnality);
    return render_template("login.html") 

  return redirect('/')

@app.route('/createatlas', methods=['POST'])
def createatlas():
  username = request.form['aname']
  password = request.form['nickname']
  age = request.form['catagory']
  gender = request.form['introduction']

  cmd = 'select aname from atlas where nickname =  (:name1)';
  cc = g.conn.execute(text(cmd),name1 = password).fetchone();
  cmd = 'select password from users where nickname =  (:name1)';
  zz = g.conn.execute(text(cmd),name1 = password).fetchone();
  cmd = 'select nickname from atlas where aname =  (:name1)';
  gg = g.conn.execute(text(cmd),name1 = username).fetchone();
  if gg is not None:
    return render_template("createatlas2.html")
  if zz is not None:
    if cc is not None:
      return render_template("createatlasnickname1.html")
    else:
      cmd = 'INSERT INTO atlas(aname,nickname,catagory,introduction) VALUES (:a,:b,:c,:d)';
      g.conn.execute(text(cmd),a = username,b = password,c=age,d=gender);
      return redirect('/indexlogin')
  else:
    return render_template("createatlasnickname2.html")

@app.route('/addphoto', methods=['POST'])
def addphoto():
  number = request.form['number']
  character = request.form['character']
  theme = request.form['theme']
  location = request.form['location']
  formats = request.form['format']
  size = request.form['size']
  copyright = request.form['copyright']
  aperture = request.form['aperture']
  iso = request.form['iso']
  foca_length_use = request.form['foca_length_use']
  shuttle_time_use = request.form['shuttle_time_use']
  model = request.form['model']
  nickname = request.form['nickname']
  aname = request.form['aname']
  types = request.form['type']
  path = request.form['path']
  color_temperature =  request.form['color_temperature']
  if number.isdigit():
    aa = True
  else:
    aa = False
  if aa == False:
    return render_template("addphoto.html")
  cmd = 'select company from camera where model =  (:name1)';
  ca = g.conn.execute(text(cmd),name1 = model).fetchone();
  cmd = 'select aperture from lens where type =  (:name1)';
  le = g.conn.execute(text(cmd),name1 = types).fetchone();
  cmd = 'select nickname from photo where number =  (:name1)';
  cc = g.conn.execute(text(cmd),name1 = number).fetchone();
  cmd = 'select password from users where nickname =  (:name1)';
  gg = g.conn.execute(text(cmd),name1 = nickname).fetchone();
  if gg is None:
    return render_template("addphoto2.html")
  if cc is not None:
    return render_template("addphoto5.html")
  if ca is None:
    return render_template("addphoto3.html")
  if le is None:
    return render_template("addphoto4.html")
  
  cmd = 'INSERT INTO photo(number,character,theme,location,format,size,copyright,aperture,iso,foca_length_use,shuttle_time_use,model,nickname,aname,type,path,color_temperature) VALUES (:a,:b,:c,:d,:e,:f,:g,:h,:i,:j,:k,:l,:m,:n,:o,:p,:q)';
  g.conn.execute(text(cmd),a = number,b = character,c=theme,d=location,e=formats,f=size,g=copyright,h=aperture,i=iso,j=foca_length_use,k=shuttle_time_use,l=model,m=nickname,n=aname,o=types,p=path,q=color_temperature);
  return redirect('/indexlogin')



@app.route('/register', methods=['POST'])
def register():
  nickname = request.form['nickname']
  password = request.form['number']
  age = request.form['age']
  gender = request.form['gender']
  uname = request.form['uname']
  nationnality = request.form['nationnality']
  cmd = 'select * from users where nickname = (:name1)';
  user = g.conn.execute(text(cmd) ,name1 = nickname);
  for i in user:
    if i['nickname'] == nickname:
      return redirect('/')

  return render_template("register.html") 



if __name__ == "__main__":
  import click

  @click.command()
  @click.option('--debug', is_flag=True)
  @click.option('--threaded', is_flag=True)
  @click.argument('HOST', default='0.0.0.0')
  @click.argument('PORT', default=8111, type=int)
  def run(debug, threaded, host, port):


    HOST, PORT = host, port
    print "running on %s:%d" % (HOST, PORT)
    app.run(host=HOST, port=PORT, debug=debug, threaded=threaded)


  run()
