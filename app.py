import os
from flask import Flask, render_template, request

app = Flask(__name__)

IMAGE_DIR = os.path.join(app.static_folder, 'images')

# EDITABLE PRICES DICTIONARY
# Add or modify specific image filenames and their prices here:
PRICES = {
    'sample_bespoke1.jpg': '₦120,000',
    'sample_kaftan1.jpg': '₦65,000',
    'sample_agbada1.jpg': '₦150,000',
    # Default price for any image not listed above will be ₦85,000
}

DEFAULT_PRICE = '₦85,000'

def format_title(filename):
    """Generates a clean product title from the image file name."""
    name_without_ext = os.path.splitext(filename)[0]
    clean_name = name_without_ext.replace('_', ' ').replace('-', ' ')
    return clean_name.title()

def get_all_catalog_items():
    """Dynamically reads images inside static/images/ and assigns categories and prices."""
    items = []
    if not os.path.exists(IMAGE_DIR):
        return items

    valid_extensions = ('.jpg', '.jpeg', '.png', '.webp')
    files = sorted([f for f in os.listdir(IMAGE_DIR) if f.lower().endswith(valid_extensions)])

    for index, filename in enumerate(files):
        lower_name = filename.lower()
        
        # Skip slide images from regular catalog listings
        if lower_name.startswith('slide'):
            continue

        # Dynamic Category Tagging
        if 'bespoke' in lower_name:
            category = 'Bespoke'
        elif 'kaftan' in lower_name:
            category = 'Kaftan'
        elif 'ankara' in lower_name:
            category = 'Ankara Wear'
        elif 'gown' in lower_name or 'dress' in lower_name:
            category = 'Dresses & Gowns'
        elif 'agbada' in lower_name:
            category = 'Agbada & Sets'
        elif 'kiddies' in lower_name:
            category = 'Kiddies'
        else:
            category = 'Traditional'

        # Fetch editable price or assign default
        item_price = PRICES.get(filename, DEFAULT_PRICE)

        items.append({
            'id': index + 1,
            'title': format_title(filename),
            'category': category,
            'price': item_price,
            'image': f'images/{filename}',
            'filename': filename
        })

    return items

def get_hero_slides():
    """Loads carousel images starting with 'slide' or falls back to default images."""
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
            if query in item['title'].lower() or query in item['category'].lower() or query in item['filename'].lower()
        ]
    else:
        filtered_items = all_items

    return render_template('collection.html', items=filtered_items, search_query=query)

@app.route('/bespoke')
def bespoke():
    all_items = get_all_catalog_items()
    bespoke_items = [
        item for item in all_items 
        if 'bespoke' in item['category'].lower() or 'bespoke' in item['filename'].lower()
    ]
    return render_template('bespoke.html', items=bespoke_items)

@app.route('/contact', methods=['GET', 'POST'])
def contact():
    return render_template('contact.html')

if __name__ == '__main__':
    app.run(debug=True)