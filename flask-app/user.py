import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
import webbrowser
from selenium import webdriver
import os
import json

# File to store URLs
url_file = "saved_urls.txt"

current_page = 0
urls_per_page = 16  # Adjust as needed
open_urls = set()

# Selenium WebDriver instance
driver = None

def reset_urls():
    with open(url_file, 'w') as file:  # Clear the file
        pass
    open_urls.clear()  # Clear the set of open URLs
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

def open_url_in_browser(url):
    webbrowser.open_new_tab(url)

def open_all_urls():
    try:
        with open(url_file, "r") as file:
            urls = file.readlines()
        for url in urls:
            open_url_in_browser(url.strip())  # Strip to remove leading/trailing whitespace
    except FileNotFoundError:
        pass

def save_url():
    url = url_entry.get().strip()  # Get the URL and remove leading/trailing whitespace
    if url == "":
        return  # Don't save empty URLs

    # Check if the URL already exists in the listbox
    if url in url_list.get(0, tk.END):
        messagebox.showwarning("Duplicate URL", f"The URL '{url}' is already saved.")
        return

    # Save the URL to file
    with open(url_file, "a") as file:
        file.write(url + "\n")
    load_saved_urls()

def delete_url():
    selected_indices = url_list.curselection()
    if selected_indices:
        urls_to_delete = [url_list.get(index).strip() for index in selected_indices]
        with open(url_file, "r") as file:
            urls = file.readlines()
        with open(url_file, "w") as file:
            for url in urls:
                if url.strip() not in urls_to_delete:
                    file.write(url)
        load_saved_urls()
    else:
        messagebox.showwarning("No URL Selected", "Please select a URL to delete.")


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

def close_selected_tabs():
    selected_indices = url_list.curselection()
    if selected_indices:
        global driver
        if not driver:
            driver = webdriver.Chrome()  # Initialize WebDriver if not already
        for index in selected_indices:
            try:
                driver.switch_to.window(driver.window_handles[index])
                driver.close()
            except IndexError:
                print(f"Failed to close tab at index {index}")

def close_all_tabs():
    print("closing all tabs")

def get_tab_information():
    print("testing")

def open_selected_url():
    selected_indices = url_list.curselection()
    if selected_indices:
        for index in selected_indices:
            url_to_open = url_list.get(index)
            open_url_in_browser(url_to_open)
    else:
        url = url_entry.get()
        if url:
            open_url_in_browser(url)

def show_help():
    messagebox.showinfo("Help", "This application allows you to manage and open URLs.\n"
                                "You can enter URLs, open them individually or all at once, save and delete URLs, and manage open tabs.")


# Other function definitions...

def save_active_tab():
    base_dir = ''  # Replace with your desired base directory
    id = "tabs"
    filename = f"{id}.json"
    abs_file = os.path.join(base_dir, filename)

    try:
        with open(abs_file, "r") as f:
            # Perform operations with the opened file
            print(f"Successfully opened {abs_file}")
            # Example: Read contents of the file
            contents = f.read()
            print(f"File contents: {contents}")
    except FileNotFoundError:
        print(f"File {abs_file} not found.")
    except Exception as e:
        print(f"An error occurred: {str(e)}")

def perform_unspecified_action():
    # Placeholder action
    print("hi")

def initialize_root_window():
    root = tk.Tk()
    root.title("URL Manager")
    root.geometry("900x700")
    root.grid_columnconfigure(1, weight=1)
    root.grid_rowconfigure(7, weight=1)
    return root

def create_url_entry(root, font_style):
    label = ttk.Label(root, text="Enter URL:", font=font_style)
    label.grid(row=0, column=0, padx=5, pady=5, sticky="w")
    url_entry = ttk.Entry(root, width=60, font=font_style)
    url_entry.grid(row=0, column=1, padx=5, pady=5, sticky="we")
    return url_entry

def create_buttons(root, font_style):
    open_button = ttk.Button(root, text="Open URL", command=open_selected_url, width=20)
    open_button.grid(row=1, column=0, columnspan=2, padx=5, pady=5)
    open_all_button = ttk.Button(root, text="Open All URLs", command=open_all_urls, width=20)
    open_all_button.grid(row=2, column=0, columnspan=2, padx=5, pady=5)
    save_button = ttk.Button(root, text="Save URL", command=save_url, width=20)
    save_button.grid(row=3, column=0, columnspan=2, padx=5, pady=5)
    delete_button = ttk.Button(root, text="Delete URL", command=delete_url, width=20)
    delete_button.grid(row=4, column=0, columnspan=2, padx=5, pady=5)
    reset_button = ttk.Button(root, text="Reset All", command=reset_urls, width=20)
    reset_button.grid(row=5, column=0, columnspan=2, padx=5, pady=5)
    close_selected_button = ttk.Button(root, text="Close Selected Tabs", command=close_selected_tabs, width=20)
    close_selected_button.grid(row=10, column=0, columnspan=2, padx=5, pady=5)
    close_all_button = ttk.Button(root, text="Close All Tabs", command=close_all_tabs, width=20)
    close_all_button.grid(row=11, column=0, columnspan=2, padx=5, pady=5)
    get_info_button = ttk.Button(root, text="Get Open Tabs Info", command=get_tab_information, width=20)
    get_info_button.grid(row=12, column=0, columnspan=2, padx=5, pady=5)
    save_active_tab_button = ttk.Button(root, text="Save Active Tab", command=save_active_tab, width=20)
    save_active_tab_button.grid(row=13, column=0, columnspan=2, padx=5, pady=5)
    unspecified_action_button = ttk.Button(root, text="Unspecified Action", command=perform_unspecified_action, width=20)
    unspecified_action_button.grid(row=14, column=0, columnspan=2, padx=5, pady=5)

def create_url_list_display(root, font_style):
    url_list_label = ttk.Label(root, text="Saved URLs:", font=font_style)
    url_list_label.grid(row=6, column=0, padx=5, pady=5, sticky="w")
    scrollbar = tk.Scrollbar(root)
    scrollbar.grid(row=7, column=2, rowspan=10, padx=5, pady=5, sticky="ns")
    url_list = tk.Listbox(root, width=70, height=15, yscrollcommand=scrollbar.set, font=font_style, selectmode=tk.EXTENDED)
    url_list.grid(row=7, column=0, columnspan=2, padx=5, pady=5, sticky="nsew")
    scrollbar.config(command=url_list.yview)
    return url_list

def create_navigation_frame(root):
    navigation_frame = ttk.Frame(root)
    navigation_frame.grid(row=8, column=0, columnspan=2, pady=5)
    previous_button = ttk.Button(navigation_frame, text="<<", command=previous_page, width=20)
    previous_button.grid(row=0, column=0, padx=5)
    next_button = ttk.Button(navigation_frame, text=">>", command=next_page, width=20)
    next_button.grid(row=0, column=1, padx=5)

def create_menu(root):
    menu_bar = tk.Menu(root)
    root.config(menu=menu_bar)
    file_menu = tk.Menu(menu_bar, tearoff=0)
    menu_bar.add_cascade(label="File", menu=file_menu)
    file_menu.add_command(label="Reset All URLs", command=reset_urls)
    file_menu.add_separator()
    file_menu.add_command(label="Exit", command=root.quit())
    help_menu = tk.Menu(menu_bar, tearoff=0)
    menu_bar.add_cascade(label="Help", menu=help_menu)
    help_menu.add_command(label="Show Help", command=show_help)

def main():
    global url_entry, url_list

    root = initialize_root_window()

    font_style = ('Arial', 12)

    url_entry = create_url_entry(root, font_style)

    create_buttons(root, font_style)

    url_list = create_url_list_display(root, font_style)

    create_navigation_frame(root)

    create_menu(root)

    load_saved_urls()

    root.mainloop()

if __name__ == "__main__":
    main()
