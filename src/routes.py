from flask import Flask, request, render_template, redirect, url_for, session, Markup
import forms as f
import config as c
import hashlib
import hasher
import wikipedia

app = Flask("server")
app.config['SECRET_KEY'] = "knowway-secret"
app.use_reloader=False

@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html', title='KnowWay!')

@app.route('/login', methods=['GET','POST'])
def login():
    error = ""
    if(session.get('auth')):
        return redirect(url_for('main'))

    form = f.LoginForm()
    if request.method == 'POST':
        print(request.form['username'],"    ",request.form['password']," = ", hasher.hash(request.form['password']))
        auth = SERVER.scanLogin(request.form['username'], hasher.hash(request.form['password'])).getAuthCode()
        if auth is None:
            error = 'Invalid Credentials.'
        else:
            session['auth'] = auth
            return redirect(url_for('main'))

    return render_template('login.html', title='KnowWay!',form=form,error=error)

@app.route('/register', methods=['GET','POST'])
def register():
    error = ""
    if(session.get('auth')):
        return redirect(url_for('main'))

    form = f.RegisterForm()
    if request.method == 'POST':

        user = SERVER.scanUsername(request.form['username'])
        correctPassword = (hasher.hash(request.form['password']) == hasher.hash(request.form['password2']))

        if user is None and correctPassword == True:
            uid = SERVER.registerNewUser(request.form['username'], hasher.hash(request.form['password']))
            session['auth'] = SERVER.getUser(uid).getAuthCode()
            return redirect(url_for('main'))
        else:
            if(correctPassword==False):
                error = "Repeat password correctly."
            if(user is not None):
                error = "Account with this username already exists!"

    return render_template('register.html', title='KnowWay!',form=form,error=error)

@app.route('/logout')
def logout():
    session.pop('auth')
    return redirect(url_for('index'))


@app.route('/wiki')
def wiki():
    if(session.get('auth') is None):
        return redirect(url_for('login'))
    
    title = request.values.get('title')
    if(title is not None):
        w = wikipedia.WikipediaPage(title)
    else:
        return redirect(url_for('wiki', **{'title':wikipedia.random()}))
    #w="<br><br><br>YO!"
    username = SERVER.scanAuth(session['auth']).getUsername()
    return render_template('wiki.html', title='KnowWay!', username=username, sourceHTML = Markup(w.html()))

@app.route('/wiki/<title>')
def wiki_redirect(title):
    return redirect(url_for('wiki', **{'title':title}))


@app.route('/main', methods=['GET','POST'])
def main():
    error = ''
    if(session.get('auth') is None):
        return redirect(url_for('login'))

    #Find wikipedia page with a title:
    if(request.method=='POST'):
        findtitle = request.form['searchWiki']
        try:
            w = wikipedia.WikipediaPage(findtitle)
        except:
            error='Not found...'
        else:
            return redirect(url_for('wiki', **{'title':w.title}))

    return render_template('main.html', title='KnowWay!', auth=session['auth'], formFindWikipedia=f.FindWikipedia(), error=error)

@app.route('/addPoints', methods=['GET','POST'])
def addPoints():
    if request.method == 'POST':
        link = request.values.get('link')
        time = request.values.get('time')
        #print(session.get('auth'),"   sent   ",link,"   ",time)
        user = SERVER.scanAuth(session.get('auth'))
        
        points = SERVER.addPointsForUser(user.getId(), session.get('auth'), link, float(time))
        SERVER.addComment(user.getId(), "Superowe!",link)

        return str(int(points[0])) + "/" +str(points[1]) 
    else:
        return "0/0"