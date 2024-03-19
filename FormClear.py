# working.py
import gemToken # Import gemtoken.py to obtain eBay access token
from tkinter import Tk, Label, Button, Canvas
from tkinter import filedialog
import tkinter as tk
from PIL import Image, ImageTk
import requests
import pandas as pd
import facebook
import config


# Initialize Facebook Graph API with your access token
graph = facebook.GraphAPI(access_token=config.facebook_access_token, version='3.1')

# Define global variables
df = None
label = None
selected_index = None
page_id = config.page_id  # Get page_id from config


# Function definitions

def get_search_results():
    global df
    query = input_entry.get()
    category_id = category_entry.get()
    headers = {
        "Authorization": f"Bearer {config.ebay_bearer_token}",
        "Content-Type": "application/json",
        "Accept": "application/json",
        "Content-Language": "en-GB",
        "X-EBAY-C-MARKETPLACE-ID": "EBAY_GB"
    }
    url = f"https://api.ebay.com/buy/browse/v1/item_summary/search?q={query}&category_ids={category_id}&limit=20&filter=buyingOptions%3A%7BAUCTION%7CFIXED_PRICE%7CCLASSIFIED_AD%7D"
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        json_response = response.json()
        data = {
            'title': [],
            'thumbnailImages': [],
            'itemWebUrl': []
        }
        for item in json_response['itemSummaries']:
            data['title'].append(item.get('title', 'N/A'))
            thumbnail_images = item.get('thumbnailImages', [])
            if thumbnail_images:
                data['thumbnailImages'].append(thumbnail_images[0].get('imageUrl', 'N/A'))
            else:
                data['thumbnailImages'].append('N/A')
            item_web_url = item.get('itemWebUrl', '').split('?')[0]
            item_web_url += "?mkcid=1&mkrid=710-53481-19255-0&siteid=3&campid=5337535757&customid=clearForm&toolid=10001&mkevt=1"
            data['itemWebUrl'].append(item_web_url)
        df = pd.DataFrame(data)
        update_listbox()
    else:
        print("Error:", response.status_code)

def update_listbox():
    listbox.delete(0, tk.END)
    for idx, row in df.iterrows():
        listbox.insert(tk.END, f"{idx + 1}. {row['title']}")

def on_select(event):
    global selected_index
    selected_index = listbox.curselection()[0]

def show_image():
    global selected_index
    if selected_index is not None:
        image_url = df.at[selected_index, 'thumbnailImages']
        image = Image.open(requests.get(image_url, stream=True).raw)
        image = image.resize((300, 300))
        photo = ImageTk.PhotoImage(image)
        label.config(image=photo)
        label.image = photo
    else:
        #label.config(image=None)  # Clear the image not working
        #label.photo = None # Clear reference to photo not working
        label.config(text="Please select an item first.")

def clear_fields():
    input_entry.delete(0, tk.END)
    category_entry.delete(0, tk.END)
    description_entry.delete("1.0", tk.END)
    status_label.config(text="")
    # label.config(image=None)  # Clear the image not working
    listbox.delete(0, tk.END)  # Clear the search results

def remove_success_message():
    status_label.config(text="")

def post_to_facebook():
    global selected_index
    if selected_index is not None:
        title = df.loc[selected_index, 'title']
        title += " #ad"
        image_url = df.loc[selected_index, 'thumbnailImages']
        item_url = df.loc[selected_index, 'itemWebUrl']
        description = description_entry.get("1.0", tk.END).strip()
        message = f"{title}\n{item_url}\n{description}"  # Description placed below the link
        image_data = requests.get(image_url).content
        with open('image.jpg', 'wb') as f:
            f.write(image_data)
        graph.put_photo(image=open('image.jpg', 'rb'), message=message, page_id=page_id)
                
        # Clear fields upon successful posting
        clear_fields()

        # Display success message
        status_label.config(text="Item successfully posted to Facebook!")

        # Remove success message after 5 seconds
        window.after(5000, remove_success_message)
    else:
        label.config(text="Please select an item first.")

def exit_program():
    window.destroy()

# Create Tkinter window
window = tk.Tk()
window.title("Display eBay Images")

# Create widgets
query_label = tk.Label(window, text="Enter the query:")
query_label.pack(pady=5)
input_entry = tk.Entry(window, width=50)
input_entry.pack(pady=5)

category_label = tk.Label(window, text="Enter the category ID:")
category_label.pack(pady=5)
category_entry = tk.Entry(window, width=50)
category_entry.pack(pady=5)

search_button = tk.Button(window, text="Search", command=get_search_results)
search_button.pack(pady=5)

listbox = tk.Listbox(window, width=50, height=10)
listbox.pack(pady=5)

listbox.bind("<<ListboxSelect>>", on_select)

show_image_button = tk.Button(window, text="Show Image", command=show_image)
show_image_button.pack(pady=5)

description_label = tk.Label(window, text="Enter your own description for the item:")
description_label.pack(pady=5)
description_entry = tk.Text(window, height=5, width=50)
description_entry.pack(pady=5)

post_button = tk.Button(window, text="Post to Facebook", command=post_to_facebook)
post_button.pack(pady=5)

label = tk.Label(window)
label.pack(pady=10)

# Add Exit button
exit_button = tk.Button(window, text="Exit", command=exit_program)
exit_button.pack(pady=10)

# Create status label
status_label = tk.Label(window, text="")
status_label.pack(pady=5)


window.mainloop()
