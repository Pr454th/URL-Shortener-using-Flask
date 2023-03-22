from flask import render_template, request, redirect, url_for, flash, abort,session,jsonify, Blueprint
import json
import os.path
from werkzeug.utils import secure_filename

bp=Blueprint('urlshort',__name__)

@bp.route('/')
def home():
    return render_template('home.html',snames=session.keys())

@bp.route('/user')
def user():
    return 'User'

@bp.route('/shorten',methods=['GET','POST'])
def shorten():
    if request.method=='POST':
        urls={}
        if os.path.exists('urls.json'):
            with open('urls.json') as f:
                urls=json.load(f)
        if request.form['sname'] in urls.keys():
            flash('Short name already taken')
            return redirect(url_for('urlshort.home'))
        if 'url' in request.form.keys():
            urls[request.form['sname']]={'url':request.form['url']}
        else:
            f=request.files['file']
            full_name=request.form['sname']+secure_filename(f.filename)
            f.save('urlshort/static/user_files/'+full_name)
            urls[request.form['sname']]={'file':full_name}
        with open('urls.json','w') as f:
            json.dump(urls,f)
            session[request.form['sname']]=True
        # return render_template('shorten.html',sname=request.form['sname'])
    else:
        return redirect(url_for('urlshort.home'))
    return redirect(url_for('urlshort.home'))

@bp.route('/<string:sname>')
def redirect_to_url(sname):
    if os.path.exists('urls.json'):
        with open('urls.json') as f:
            urls=json.load(f)
            if sname in urls.keys():
                if 'url' in urls[sname].keys():
                    return redirect(urls[sname]['url'])
                else:
                    return redirect(url_for('static',filename='/user_files/'+urls[sname]['file']))
    return abort(404)

@bp.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@bp.route('/api')
def session_api():
    return jsonify(list(session.keys()))

if __name__ == '__main__':
    bp.run()