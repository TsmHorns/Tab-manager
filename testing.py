import tkinter as tk
from tkinter import ttk
import webbrowser

# File to store URLs
url_file = "saved_urls.txt"

current_page = 0
urls_per_page = 16  # Adjust as needed

urls_to_preload = [
    "https://www.example.com",
    "https://www.google.com",
    "https://www.github.com",
    "https://www.stackoverflow.com",
    "https://www.reddit.com",
    "https://www.wikipedia.org",
    "https://www.twitter.com",
    "https://www.facebook.com",
    "https://www.instagram.com",
    "https://www.linkedin.com",
    "https://www.youtube.com",
    "https://www.amazon.com",
    "https://www.ebay.com",
    "https://www.netflix.com",
    "https://www.spotify.com",
    "https://www.nytimes.com",
    "https://www.cnn.com",
    "https://www.bbc.com",
    "https://www.theguardian.com",
    "https://www.foxnews.com",
    "https://www.nationalgeographic.com",
    "https://www.medium.com",
    "https://www.quora.com",
    "https://www.github.io"
]

def reset_urls():
    open(url_file, 'w').close()  # Clear the file
    load_saved_urls()  # Reload the URL list

def next_page():
    global current_page
    current_page += 1
    if not check_page_validity():
        current_page -= 1  # Revert if the next page is empty
    load_saved_urls()

def previous_page():
    global current_page
    current_page = max(0, current_page - 1)  # Prevent negative pages
    load_saved_urls()

def check_page_validity():
    try:
        with open(url_file, "r") as file:
            urls = file.readlines()
        start = current_page * urls_per_page
        end = start + urls_per_page
        return len(urls[start:end]) > 0
    except FileNotFoundError:
        return False
    
def pre_loaded(urls_to_preload, url_file):
    with open(url_file, "w") as file:
        for url in urls_to_preload:
            file.write(url + "\n")
    print("URLs preloaded successfully.")

def open_all_urls():
    try:
        with open(url_file, "r") as file:
            urls = file.readlines()
        for url in urls:
            webbrowser.open_new_tab(url.strip())
    except FileNotFoundError:
        pass

def save_open_tabs():
    # Get all open tabs and save them to the file
    open_tabs = webbrowser.get().windows()
    with open(url_file, "w") as file:
        for tab in open_tabs:
            file.write(tab.url + "\n")
    load_saved_urls()

def close_all_tabs():
    # Close all open tabs
    webbrowser.get().open("about:blank")
    load_saved_urls()

def close_selected_tabs():
    selected_indices = url_list.curselection()
    if selected_indices:
        selected_urls = [url_list.get(index) for index in selected_indices]
        open_tabs = webbrowser.get().windows()
        for tab in open_tabs:
            if tab.url in selected_urls:
                tab.close()
        load_saved_urls()

def open_selected_url():
    selected_indices = url_list.curselection()
    if selected_indices:
        for index in selected_indices:
            url_to_open = url_list.get(index)
            webbrowser.open_new_tab(url_to_open)
    else:
        url = url_entry.get()
        if url:
            webbrowser.open_new_tab(url)

def save_url():
    url = url_entry.get()
    with open(url_file, "a") as file:
        file.write(url + "\n")
    load_saved_urls()

def delete_url():
    selected_indices = url_list.curselection()
    if selected_indices:
        urls_to_delete = [url_list.get(index).strip() for index in selected_indices]  # Strip URLs for consistency
        with open(url_file, "r") as file:
            urls = file.readlines()
        with open(url_file, "w") as file:
            for url in urls:
                if url.strip() not in urls_to_delete:
                    file.write(url)
        load_saved_urls()

def load_saved_urls():
    url_list.delete(0, tk.END)
    try:
        with open(url_file, "r") as file:
            urls = file.readlines()
        start = current_page * urls_per_page
        end = start + urls_per_page
        for url in urls[start:end]:
            url_list.insert(tk.END, url.strip())
    except FileNotFoundError:
        pass

pre_loaded(urls_to_preload, url_file)
root = tk.Tk()
root.title("URL Opener and Saver")
root.geometry("900x700")  # Adjusted size for better readability

font_style = ('Helvetica', 12)  # Larger font for readability

label = ttk.Label(root, text="Enter URL:", font=font_style)
label.grid(row=0, column=0, padx=5, pady=5, sticky="w")

url_entry = ttk.Entry(root, width=60, font=font_style)
url_entry.grid(row=0, column=1, padx=5, pady=5, sticky="we")

open_button = ttk.Button(root, text="Open URL", command=open_selected_url, style="TButton")
open_button.grid(row=1, column=0, columnspan=2, padx=5, pady=5, sticky="ew")

open_all_button = ttk.Button(root, text="Open All URLs", command=open_all_urls, style="TButton")
open_all_button.grid(row=2, column=0, columnspan=2, padx=5, pady=5, sticky="ew")

save_button = ttk.Button(root, text="Save URL", command=save_url, style="TButton")
save_button.grid(row=3, column=0, columnspan=2, padx=5, pady=5, sticky="ew")

delete_button = ttk.Button(root, text="Delete URL", command=delete_url, style="TButton")
delete_button.grid(row=4, column=0, columnspan=2, padx=5, pady=5, sticky="ew")

reset_button = ttk.Button(root, text="Reset All", command=reset_urls, style="TButton")
reset_button.grid(row=5, column=0, columnspan=2, padx=5, pady=5, sticky="ew")

url_list_label = ttk.Label(root, text="Saved URLs:", font=font_style)
url_list_label.grid(row=6, column=0, padx=5, pady=5, sticky="w")

scrollbar = tk.Scrollbar(root)
scrollbar.grid(row=7, column=2, rowspan=10, padx=5, pady=5, sticky="ns")

url_list = tk.Listbox(root, width=70, height=15, yscrollcommand=scrollbar.set, font=font_style, selectmode=tk.EXTENDED)
url_list.grid(row=7, column=0, columnspan=2, padx=5, pady=5, sticky="nsew")

scrollbar.config(command=url_list.yview)

# Make the grid expand with the window
root.grid_columnconfigure(1, weight=1)
root.grid_rowconfigure(7, weight=1)

# Section for next and previous buttons
navigation_frame = ttk.Frame(root)
navigation_frame.grid(row=8, column=0, columnspan=2, pady=5)

previous_button = ttk.Button(navigation_frame, text="<<", command=previous_page, style="TButton", width=5)
previous_button.grid(row=0, column=0, padx=5)

next_button = ttk.Button(navigation_frame, text=">>", command=next_page, style="TButton", width=5)
next_button.grid(row=0, column=1, padx=5)

# Additional buttons for managing open tabs
save_open_button = ttk.Button(root, text="Save Open Tabs", command=save_open_tabs, style="TButton")
save_open_button.grid(row=9, column=0, columnspan=2, padx=5, pady=5, sticky="ew")

close_all_button = ttk.Button(root, text="Close All Tabs", command=close_all_tabs, style="TButton")
close_all_button.grid(row=10, column=0, columnspan=2, padx=5, pady=5, sticky="ew")

close_selected_button = ttk.Button(root, text="Close Selected Tabs", command=close_selected_tabs, style="TButton")
close_selected_button.grid(row=11, column=0, columnspan=2, padx=5, pady=5, sticky="ew")

# Load the first page of URLs initially
load_saved_urls()

root.mainloop()
