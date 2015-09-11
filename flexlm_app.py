import os
from datetime import datetime
from flask import Flask, render_template, session, redirect, url_for
from flask.ext.script import Manager
from flask.ext.bootstrap import Bootstrap
from flask.ext.moment import Moment
from flask.ext.wtf import Form
from wtforms import StringField, FileField, SubmitField, IntegerField
from wtforms.validators import Required
from flask.ext.sqlalchemy import SQLAlchemy
from wtforms import ValidationError
from werkzeug.exceptions import HTTPException, NotFound
import flexlm_parser

basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)
app.config['SECRET_KEY'] = 'hard to guess string'
app.config['SQLALCHEMY_DATABASE_URI'] =\
    'sqlite:///' + os.path.join(basedir, 'data.sqlite')
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True
app.debug = True

manager = Manager(app)
bootstrap = Bootstrap(app)
db = SQLAlchemy(app)
moment = Moment(app)

class Server(db.Model):
    __tablename__ = 'servers'
    id = db.Column(db.Integer, primary_key=True)
    vendor = db.Column(db.String(50), unique=True)
    server = db.Column(db.String(64))
    port = db.Column(db.Integer)
    software = db.Column(db.String(50))
    rrdfile = db.Column(db.String(255))

    def __repr__(self):
        return '<Server %r>' % self.vendor

class AddServerForm(Form):
    vendor = StringField('Vendor', validators=[Required()])
    port = IntegerField('Port Number', validators=[Required()])
    server = StringField('License Server Name', validators=[Required()])
    software_feature = StringField('Software To Monitor')
    rrd_file = StringField('Full Path To RRD Usage Database')
    submit = SubmitField('Add Server')

    def validate_vendor(self, field):
        if Server.query.filter_by(vendor=field.data).first():
            raise ValidationError('Vendor name already used')

    def validate_rrd_file(self, field):
        if os.path.isfile(field.data) is False:
            raise ValidationError('File does not exist')
        if field.data[-3:] != 'rrd':
            raise ValueError('File is not a RRD database')

@app.route('/')
def index():
    servers = Server.query.all()
    return render_template('index.html', servers=servers)

@app.route('/servers/<vendor>/usage')
def usage(vendor):
    return render_template('usage.html', vendor=vendor)


@app.route('/servers/<vendor>/users')
def users(vendor):
    settings = Server.query.filter_by(vendor=vendor).first() 
    if settings is None:
        raise(NotFound)
    server = str(settings.port) +'@'+ settings.server
    users = flexlm_parser.get_licenses(server, settings.software)
    return render_template('users.html', vendor=vendor, users=users, 
                           current_time=datetime.utcnow())
    
    
    return render_template('users.html', vendor=vendor)

@app.route('/servers/config', methods=['GET', 'POST'])
def config():
    form = AddServerForm()
    if form.validate_on_submit():
        session['vendor'] = form.vendor.data
        session['port'] = form.port.data
        session['server'] = form.server.data
        session['software_feature'] = form.software_feature.data
        session['rrd_file'] = form.rrd_file.data
        print(session.get('rrd_file'))
        record = Server(vendor=session.get('vendor'), 
                        port=session.get('port'),
                        server=session.get('server'),
                        software=session.get('software_feature'),
                       rrdfile=session.get('rrd_file'))
        db.session.add(record)
        db.session.commit()
        return redirect(url_for('config'))
    return render_template('config.html', form=form, 
                           vendor=session.get('vendor'))

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@app.errorhandler(500)
def page_not_found(e):
    return render_template('500.html'), 500

if __name__ == '__main__':
    manager.run()
