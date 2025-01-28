import os
import requests
from flask import Flask
from flask_mail import Mail, Message
import jinja2
from dotenv import load_dotenv


load_dotenv()

DOMAIN= os.getenv( "MAILGUN_DOMAIN" )
template_loader= jinja2.FileSystemLoader( "template" )
template_env= jinja2.Environment( loader= template_loader )


def render_template( template_filename, **context ):
   
  return template_env.get_template( template_filename ).render( **context )



def send_email( subject, body, to, sender='no-reply@localhost.com', html= None ):
  app = Flask(__name__)
  
  # Flask-Mail configuration
  app.config['MAIL_SERVER'] = 'localhost'  # Update if using a different SMTP server
  app.config['MAIL_PORT'] = 1025           # Change if necessary
  app.config['MAIL_USE_TLS'] = False
  app.config['MAIL_USE_SSL'] = False
  app.config['MAIL_USERNAME'] = None       # Set if your SMTP server requires authentication
  app.config['MAIL_PASSWORD'] = None
  app.config['MAIL_DEFAULT_SENDER'] = sender

  mail = Mail( app )

  with app.app_context():
    try:
        msg = Message( subject= subject, recipients= to, body= body, html= html )
        mail.send( msg )
        print( "Email sent successfully!" )
        return "Email sent successfully!"
    except Exception as e:
        print(  f"Failed to send email: {e}" )
        return f"Failed to send email: {e}"



def send_user_registration_email( to, username ):

  return send_email(
      to= to,
      subject= "Successfully signed up",
      body= f"Hello, { username }! You have successfully signed up to the Stores REST API!",      
      html= render_template( "email.action.html", username= username )
    )