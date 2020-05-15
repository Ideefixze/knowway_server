from flask import Flask, request, render_template, redirect, url_for, session, Markup
import forms as f
import config as c
import hashlib
import hasher
import wikipedia
import polona as PolonaAPI
import time as te


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
        try:
            w = wikipedia.WikipediaPage(title)
        except:
            return redirect(url_for('wiki', **{'title':wikipedia.random()}))
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


@app.route('/polona', methods=['GET','POST'])
def polona():
    #If not logged in, return
    if(session.get('auth') is None):
        return redirect(url_for('login'))

    #If posting a comment using form, add it first
    if request.method == 'POST':
        content = request.form['content']
        title = request.values.get('title')
        SERVER.addComment(SERVER.scanAuth(session.get('auth')).getId(), content, request.base_url+"?title="+request.values.get('title'))
    
    #Get title of polona scan and check if it is valid, if not return to main page
    title = request.values.get('title')
    renderpagesrc = ""
    try:
        if(title is not None):
            slug = PolonaAPI.PolonaSlug(title)
            if(slug!=title):
                return redirect(url_for('polona', **{'title':slug,'page':0}))

            if(PolonaAPI.PolonaScanIsPublic(title)==False):
                return redirect(url_for('no_resource'))

            scanlist = PolonaAPI.PolonaScan(title)
            page = request.values.get('page')
            if(page is not None and (int(page) >=0 and int(page) < len(scanlist))):
                renderpagesrc = scanlist[int(page)]
            else:
                return redirect(url_for('polona', **{'title':slug,'page':0}))
            renderpagesrc=renderpagesrc.replace("_alto","_fullJPG")
        else:
            return redirect(url_for('main'))
    except:
        return redirect(url_for('main'))

    #Get username so it will be displayed on <div> in app    
    username = SERVER.scanAuth(session['auth']).getUsername()

    #Try to get comments, if no resource exist, return empty
    try:
        comments=SERVER.rdb.getResource(2, title).getComments()
    except:
        comments=[]

    #Create new list of [[username,content]...] that will be displayed in list on page
    finalcommentlist=SERVER.getResourceFinalCommentList(comments)
    url = url_for('polona')+"?title="+slug
    return render_template('polona.html', title='KnowWay!', username=username, comments=finalcommentlist, imgsrc=renderpagesrc, pages=len(scanlist), url=url, prevpage=str(int(page)-1),nextpage=str(int(page)+1), formAddComment=f.AddCommentForm())

#Because links in wikipedia pages are in format /wiki/<title> and we are using /wiki?title=, redirect them to meet our expectations
@app.route('/wiki/<title>')
def wiki_redirect(title):
    return redirect(url_for('wiki', **{'title':title}))

@app.route('/user/<username>')
def user_profile(username):
    return render_template('user.html', title='KnowWay!', user=SERVER.scanUsername(username))


@app.route('/main', methods=['GET','POST'])
def main():
    error = ''
    if(session.get('auth') is None):
        return redirect(url_for('login'))

    #Find wikipedia/polona resource
    if(request.method=='POST'):
        try:
            findtitle = request.form['searchWiki']
            w = wikipedia.WikipediaPage(findtitle)
        except:
            error='Not found...'
        else:
            return redirect(url_for('wiki', **{'title':w.title}))
        
        try:
            findtitle = request.form['searchPolona']
            PolonaAPI.PolonaSlug(findtitle)
        except:
            error='Not found...'
        else:
            if(findtitle is not None):
                return redirect(url_for('polona', **{'title':findtitle}))

    username = SERVER.scanAuth(session.get('auth')).getUsername()
    return render_template('main.html', title='KnowWay!', username=username, formFindWikipedia=f.FindWikipediaForm(), formFindPolona=f.FindPolonaForm(), error=error)

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

@app.route('/no_resource')
def no_resource():
    return render_template('nores.html')