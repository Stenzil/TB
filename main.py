from werkzeug.routing import Rule
from flask import Flask, render_template, session, request, url_for, redirect, jsonify
from flask_pymongo import PyMongo
import bcrypt
import pymongo
import datetime
from bson.objectid import ObjectId

rightData = [{'loc': 'Trending in India',
              'title': '#TunishaSharm',
              'count': '10kTweets'
              }, {'loc': 'Sports.Cricket',
                  'title': '#KohliInTest',
                  'count': '2,934 Tweets'
                  }, {'loc': 'Trending',
                      'title': '#RamSetu',
                      'count': '1111 Tweets'
                      }, {'loc': 'Trending',
                          'title': '#KarishmaTanna',
                          'count': '3k Tweets'
                          }, {'loc': 'Trending in India',
                              'title': '#BharatJodo',
                              'count': '123k Tweets'
                              },]


app = Flask(__name__)
app.config['SESSION_TYPE'] = 'filesystem'
app.secret_key = 'secretivekey'
app.config['MONGO_DBNAME'] = 'TwitterBlack'
app.config['MONGO_URI'] = 'mongodb+srv://stenzil:woodfelder@tb.jqlktc8.mongodb.net/TwitterBlack?retryWrites=true&w=majority'
mongo = PyMongo(app)
print(mongo.db.list_collection_names())


@app.route('/follow', methods=["POST"])
def follow():
    print("hi from follow")

    print(str(request.data.decode('ascii')))
    if 'username' in session:
        f = mongo.db.followings
        f.insert_one({'uid': session['username'],
                     'follows': request.data.decode('ascii')})
        resp = jsonify(success=True)

    return resp


@app.route('/')
def index():
    if 'username' in session:
        return redirect(url_for('home'))
    return render_template("index.html")


@app.route('/home', methods=["GET"])
def home():
    if 'username' in session:
        Userpost = mongo.db.posts.find(
            {'author': {'$ne': session['name']}}).sort('added_on', -1)

        return render_template('home.html', posts=Userpost, right=rightData)
    else:
        return redirect(url_for('index'))


@app.route('/result', methods=["POST"])
def result():
    print('####################')
    if 'username' in session:
        want = request.form['searchfor']
        res = mongo.db.posts.find({'author': {'$regex': '^'+want}})

        return render_template('home.html', posts=res)
        # return render_template('result.html', userList=res)
    return redirect(url_for('/'))


@app.route('/profile', methods=["GET", "POST"])
def profile():
    if 'username' in session:
        res = mongo.db.users.find({'_id': ObjectId(request.args.get('user'))})
        respost = mongo.db.posts.find(
            {'authorID': str(ObjectId(request.args.get('user')))}).sort('added_on', -1)

        resfol = mongo.db.followings.find(

            {'uid': session['username'], 'follows': str(ObjectId(request.args.get('user')))})

        if (resfol.count() > 0):
            return render_template('profile.html', user=res, datas=respost, right=rightData,  follow=True)
        else:
            return render_template('profile.html', user=res, datas=respost, right=rightData, follow=False)


@ app.route('/logout', methods=["GET"])
def logout():

    session.clear()
    return redirect(url_for('index'))


@ app.route('/postUpdate', methods=["POST"])
def postUpdate():
    if 'username' in session:
        posts = mongo.db.posts
        posts.insert_one(
            {'content': request.form['postContent'], 'added_on': datetime.datetime.now(), 'author': session['name'], 'authorID': session['uid']})

    return redirect(url_for('index'))


@ app.route('/login', methods=["POST"])
def login():
    users = mongo.db.users

    login_user = users.find_one({'emailID': request.form['username']})

    if login_user:
        if bcrypt.hashpw(request.form['pass'].encode('utf-8'), login_user['password']) == login_user['password']:
            session['username'] = request.form['username']
            session['uid'] = str(login_user['_id'])
            session['name'] = login_user['name']

            return redirect(url_for("index"))
    return 'Invalid Username and/or Password'


@ app.route('/register', methods=['POST', 'GET'])
def register():
    if request.method == 'POST':
        users = mongo.db.users
        existing_user = users.find_one({'name': request.form['username']})

        if existing_user is None:
            hashpass = bcrypt.hashpw(
                request.form['pass'].encode('utf-8'), bcrypt.gensalt())
            _id = users.insert_one(
                {'emailID': request.form['username'], 'name': request.form['fname']+' '+request.form['lname'], 'yob': request.form['yob'], 'password': hashpass})
            session['username'] = request.form['username']
            session['uid'] = str(_id.inserted_id)
            session['name'] = request.form['fname']+' '+request.form['lname']

            return redirect(url_for("index"))
        return 'Email-ID Already registered.'

    return render_template('register.html')


@ app.endpoint("catch_all")
def _404(_404):
    return render_template('error.html')


app.url_map.add(Rule("/", defaults={"_404": ""}, endpoint="catch_all"))
app.url_map.add(Rule("/<path:_404>", endpoint="catch_all"))

if __name__ == "__main__":
    app.run(port=8080, debug=True)
