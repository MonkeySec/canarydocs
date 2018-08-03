from flask import Flask
from flask import request
from flask_mail import Mail, Message
import requests

application = Flask(__name__)

application.config['MAIL_SERVER'] = ''
application.config['MAIL_PORT'] = 
application.config['MAIL_USERNAME'] = ''
application.config['MAIL_PASSWORD'] = ''
mail = Mail(application)

@application.route("/")
def hello():
        return "Hello Earth!"

@application.errorhandler(404)
def handleCanaryDoc(e):
        if "/some_unique_path" in request.path:
                headers = ""

                for i, (k,v) in enumerate(request.headers):
                        headers += "%s:%s\n" % (k, v)

                headers += "URI Path: %s\n" % request.path

		msg = Message('', sender = '', recipients = [''])
		msg.body = headers
		print mail.send(msg)
		print msg

                return " "
        else:
                return e

if __name__ == "__main__":
        application.run('0.0.0.0')
