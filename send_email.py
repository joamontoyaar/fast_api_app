from flask import Flask
from flask_mail import Mail, Message

def send_email( subject, body, to, sender='no-reply@localhost.com', html= None):
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
