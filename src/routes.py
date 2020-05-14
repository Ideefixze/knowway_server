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


@app.route('/wiki', methods=['GET','POST'])
def wiki():
    #If not logged in, return
    if(session.get('auth') is None):
        return redirect(url_for('login'))

    #If posting a comment using form, add it first
    if request.method == 'POST':
        content = request.form['content']
        title = request.values.get('title')
        SERVER.addComment(SERVER.scanAuth(session.get('auth')).getId(), content, request.base_url+"?title="+request.values.get('title'))
    
    #Get title of wiki article and check if it is valid, if not random a page
    title = request.values.get('title')
    if(title is not None):
        w = wikipedia.WikipediaPage(title)
    else:
        return redirect(url_for('wiki', **{'title':wikipedia.random()}))

    #Get username so it will be displayed on <div> in app    
    username = SERVER.scanAuth(session['auth']).getUsername()

    #Try to get comments, if no resource exist, return empty
    try:
        comments=SERVER.rdb.getResource(1, title).getComments()
    except:
        comments=[]

    #Create new list of [[username,content]...] that will be displayed in list on page
    finalcommentlist=SERVER.getResourceFinalCommentList(comments)
    
    return render_template('wiki.html', title='KnowWay!', username=username, comments=finalcommentlist, sourceHTML = Markup(w.html()), formAddComment=f.AddCommentForm())

#Because links in wikipedia pages are in format /wiki/<title> and we are using /wiki?title=, redirect them to meet our expectations
@app.route('/wiki/<title>')
def wiki_redirect(title):
    return redirect(url_for('wiki', **{'title':title}))

@app.route('/user/<username>')
def user_profile(username):
    print(SERVER.scanUsername(username).getResourcePointsDict())
    return render_template('user.html', title='KnowWay!', user=SERVER.scanUsername(username))


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

    username = SERVER.scanAuth(session.get('auth')).getUsername()
    return render_template('main.html', title='KnowWay!', username=username, formFindWikipedia=f.FindWikipediaForm(), error=error)

@app.route('/addPoints', methods=['GET','POST'])
def addPoints():
    if request.method == 'POST':
        link = request.values.get('link')
        time = request.values.get('time')
        user = SERVER.scanAuth(session.get('auth'))
        
        points = SERVER.addPointsForUser(user.getId(), session.get('auth'), link, float(time))

        return str(int(points[0])) + "/" +str(points[1]) 
    else:
        return "0/0"
