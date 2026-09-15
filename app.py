import os
from flask import Flask, render_template, request, flash, redirect, url_for 
from flask_mail import Mail, Message

app = Flask(__name__)
app.secret_key = "house_of_rayoor_super_secret_key_123"  # Replace with
IMAGE_DIR = os.path.join(app.static_folder, 'images')

# EDITABLE PRODUCTS CATALOG (Categorized without hardcoded price tags)
PRODUCTS_CATALOG = [
    {"filename": "Beaded Skirt&blouse.jpg", "title": "Beaded Skirt & Blouse", "category": "Traditional"},
    {"filename": "Soso 3step beaded&aplic embroidery lace gown.jpg", "title": "Soso 3step Beaded & Aplic Embroidery Lace Gown", "category": "Dresses & Gowns"},
    {"filename": "Princess Gown.jpg", "title": "Princess Gown", "category": "Dresses & Gowns"},
    {"filename": "Vintage kaftan with pocket.jpg", "title": "Vintage Kaftan with Pocket", "category": "Kaftans"},
    {"filename": "Complete set brides attire.jpg", "title": "Complete Set Brides Attire", "category": "Bespoke"},
    {"filename": "Mimi Dress with waist corset.jpg", "title": "Mimi Dress with Waist Corset", "category": "Dresses & Gowns"},
    {"filename": "2piece Adire kimono jacket &trouser.jpg", "title": "2piece Adire Kimono Jacket & Trouser", "category": "Ankara Wear"},
    {"filename": "Ankara kaftan mix with lace&beads.jpg", "title": "Ankara Kaftan Mix with Lace & Beads", "category": "Kaftans"},
    {"filename": "Ankara kimono jacket and trouser mix with aso-oke.jpg", "title": "Ankara Kimono Jacket & Trouser Mix with Aso-Oke", "category": "Ankara Wear"},
    {"filename": "Arewa vintage gown.jpg", "title": "Arewa Vintage Gown", "category": "Dresses & Gowns"},
    {"filename": "Mimi Adire carebian skirt.jpg", "title": "Mimi Adire Caribbean Skirt", "category": "Ankara Wear"},
    {"filename": "Vintage 2piece.jpg", "title": "Vintage 2piece", "category": "Ankara Wear"},
    {"filename": "Celebrant princess Ball dress.jpg", "title": "Celebrant Princess Ball Dress", "category": "Dresses & Gowns"},
    {"filename": "Damask bubu.jpg", "title": "Damask Bubu", "category": "Kaftans"},
    {"filename": "Agbada lace mix with aso-oke.jpg", "title": "Agbada Lace Mix with Aso-Oke", "category": "Agbada & Sets"},
    {"filename": "Iro&blouse.jpg", "title": "Iro & Blouse", "category": "Traditional"},
    {"filename": "Adire kaftan.jpg", "title": "Adire Kaftan", "category": "Kaftans"},
    {"filename": "Ankara Kaftan mix with cheek.jpg", "title": "Ankara Kaftan Mix with Cheek", "category": "Kaftans"},
    {"filename": "Momo dress mix with sample net.jpg", "title": "Momo Dress Mix with Sample Net", "category": "Dresses & Gowns"},
    {"filename": "Ankara bubu 35k.jpg", "title": "Ankara Bubu (Classic)", "category": "Kaftans"},
    {"filename": "Ankara bubu 45k.jpg", "title": "Ankara Bubu (Deluxe)", "category": "Kaftans"},
    {"filename": "Ankara bubu 50k.jpg", "title": "Ankara Bubu (Premium)", "category": "Kaftans"},
    {"filename": "Princess kid dress.jpg", "title": "Princess Kid Dress", "category": "Kiddies"}
]

import os
from flask_mail import Mail, Message

# 1. Add these configurations near the top where your app = Flask(__name__) is defined
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = 'belloayoola71@gmail.com'
# Use an App Password generated from your Google Account settings
app.config['MAIL_PASSWORD'] = os.environ.get('MAIL_PASSWORD', 'your_gmail_app_password')

mail = Mail(app)

# 2. Update ONLY the contact route function
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

def format_title(filename):
    name_without_ext = os.path.splitext(filename)[0]
    return name_without_ext.replace('_', ' ').replace('-', ' ').title()

def get_all_catalog_items():
    items = []
    catalog_lookup = {item["filename"].lower(): item for item in PRODUCTS_CATALOG}

    if not os.path.exists(IMAGE_DIR):
        return items

    valid_extensions = ('.jpg', '.jpeg', '.png', '.webp')
    files = sorted([f for f in os.listdir(IMAGE_DIR) if f.lower().endswith(valid_extensions)])

    for index, filename in enumerate(files):
        lower_name = filename.lower()
        if lower_name.startswith('slide'):
            continue

        if lower_name in catalog_lookup:
            matched = catalog_lookup[lower_name]
            title = matched["title"]
            category = matched["category"]
        else:
            title = format_title(filename)
            category = 'New Arrival'

        items.append({
            'id': index + 1,
            'title': title,
            'category': category,
            'image': f'images/{filename}',
            'filename': filename
        })

    return items

def get_hero_slides():
    slides = []
    if os.path.exists(IMAGE_DIR):
        files = sorted([f for f in os.listdir(IMAGE_DIR) if f.lower().startswith('slide')])
        for f in files:
            slides.append({
                'title': format_title(f),
                'image': f'images/{f}'
            })

    if not slides:
        catalog = get_all_catalog_items()
        for item in catalog[:3]:
            slides.append({
                'title': item['title'],
                'image': item['image']
            })

    return slides

@app.route('/')
def home():
    query = request.args.get('q', '').strip().lower()
    all_items = get_all_catalog_items()
    slides = get_hero_slides()

    if query:
        filtered_items = [
            item for item in all_items
            if query in item['title'].lower() or query in item['category'].lower()
        ]
    else:
        filtered_items = all_items

    return render_template('index.html', items=filtered_items, slides=slides, search_query=query)

@app.route('/collection')
def collection():
    query = request.args.get('q', '').strip().lower()
    all_items = get_all_catalog_items()

    if query:
        filtered_items = [
            item for item in all_items
            if query in item['title'].lower() or query in item['category'].lower()
        ]
    else:
        filtered_items = all_items

    return render_template('collection.html', items=filtered_items, search_query=query)

@app.route('/bespoke')
def bespoke():
    all_items = get_all_catalog_items()
    return render_template('bespoke.html', items=all_items)

if __name__ == '__main__':
    app.run(debug=True)