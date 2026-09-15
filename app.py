import os
from flask import Flask, render_template, request, flash, redirect, url_for
from flask_mail import Mail, Message

app = Flask(__name__)

# Secret key required for Flask session & flash messages
app.secret_key = os.environ.get('SECRET_KEY', 'house_of_rayoor_super_secret_key_123')

# Flask-Mail SMTP Configuration
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = 'belloayoola71@gmail.com'
app.config['MAIL_PASSWORD'] = os.environ.get('MAIL_PASSWORD', 'your_gmail_app_password')

mail = Mail(app)

IMAGE_DIR = os.path.join(app.static_folder, 'images')

# Sample catalog data
PRODUCTS_CATALOG = [
    {"filename": "Beaded Skirt&blouse.jpg", "title": "Beaded Skirt & Blouse", "category": "Bespoke"},
    {"filename": "Soso 3step beaded&aplic embroidery lace gown.jpg", "title": "Soso 3-Step Lace Gown", "category": "Dresses"},
    {"filename": "Princess Gown.jpg", "title": "Princess Gown", "category": "Dresses"},
    {"filename": "Vintage kaftan with pocket.jpg", "title": "Vintage Kaftan with Pocket", "category": "Kaftan"},
    {"filename": "Complete set brides attire.jpg", "title": "Complete Set Brides Attire", "category": "Bridal"},
    {"filename": "Mimi Dress with waist corset.jpg", "title": "Mimi Dress with Corset", "category": "Dresses"},
    {"filename": "2piece Adire kimono jacket &trouser.jpg", "title": "2-Piece Adire Kimono Set", "category": "Adire"},
    {"filename": "Ankara Kaftan mix with lace&beads.jpg", "title": "Ankara Kaftan Mix", "category": "Kaftan"}
]

def format_title(filename):
    name_without_ext = os.path.splitext(filename)[0]
    return name_without_ext.replace('_', ' ').replace('-', ' ').title()

@app.route('/')
def home():
    return render_template('index.html', products=PRODUCTS_CATALOG[:4])

@app.route('/collection')
def collection():
    return render_template('collection.html', products=PRODUCTS_CATALOG)

@app.route('/bespoke')
def bespoke():
    return render_template('bespoke.html')

@app.route('/contact', methods=['GET', 'POST'])
def contact():
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        phone = request.form.get('phone')
        message_body = request.form.get('message')

        try:
            msg = Message(
                subject=f"New Contact Inquiry from {name}",
                sender=app.config['MAIL_USERNAME'],
                recipients=['belloayoola71@gmail.com']
            )
            
            msg.body = f"""
New Inquiry Received from House of Rayoor Website:

Full Name: {name}
Email Address: {email}
Phone / WhatsApp: {phone}

Message:
{message_body}
"""
            mail.send(msg)
            flash("Thank you! Your message has been sent successfully.", "success")
        except Exception as e:
            flash("There was an issue sending your message. Please try again later.", "danger")
            print(f"Mail Error: {e}")

        return redirect(url_for('contact'))

    return render_template('contact.html')

if __name__ == '__main__':
    app.run(debug=True)