from flask import Flask, render_template, request, redirect , url_for
import pandas as pd
import random
import requests
import os
import io
from PIL import Image

app = Flask(__name__)

# Load the dataset
data = pd.read_csv('FashionDataset.csv')

# Hugging Face API URL and token
API_URL = "https://api-inference.huggingface.co/models/MohamedRashad/diffusion_fashion"
API_TOKEN = "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"  # Replace with your actual API token

# Define a directory to save the images
IMAGE_SAVE_DIR = 'static'

# Ensure the image directory exists
if not os.path.exists(IMAGE_SAVE_DIR):
    os.makedirs(IMAGE_SAVE_DIR)

# Function to query the Hugging Face model, save the image, and return the saved image URL
def query_huggingface(payload):
    headers = {"Authorization": f"Bearer {API_TOKEN}"}
    response = requests.post(API_URL, headers=headers, json=payload)
    
    # Generate a unique filename for the saved image
    image_filename = os.path.join(IMAGE_SAVE_DIR, f'bhavishya.jpg')
    
    # Save the image to the specified file
    with open(image_filename, 'wb') as image_file:
        image_file.write(response.content)
    
    # Return the URL of the saved image
    #print('/'+ image_filename)
    print(image_filename)
    return '/' + image_filename

@app.route('/', methods=['GET', 'POST'])
def index():
    image_url = None

    if request.method == 'POST':
        input_category = request.form['input_category']
        filtered_df = data[data['Category'] == input_category].copy()
        filtered_df.reset_index(drop=True, inplace=True)
        num_rows = filtered_df.shape[0]
        
        if num_rows > 0:
            random_index = random.randint(0, num_rows - 1)
            random_detail = filtered_df.loc[random_index, 'Deatils']
            
            # Query the Hugging Face model and get the saved image URL
            image_url = query_huggingface({
                "inputs": random_detail,
            })
    # image_page_html = f"""
    #         <!DOCTYPE html>
    #         <html>
    #         <head>
    #             <title>Fashion Image</title>
    #         </head>
    #         <body>
    #             <h1>Fashion Image</h1>
                
    #             <img src="bhavishya.jpg" alt="Fashion Image">
                
    #         </body>
    #         </html>
            # """
            return render_template('image_page.html')
    return render_template('index.html', image_url=image_url)
    
@app.route('/image')
def image_page():
    return send('/image_page.html')

if __name__ == '__main__':
    app.run(debug=True)

