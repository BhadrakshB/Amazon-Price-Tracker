import requests
from bs4 import BeautifulSoup
import tkinter as tk
from tkinter import *
import webbrowser
import time

product_url = input("Enter the Url of the of the Amazon product: ") # Asking for the product url
headers = {
    "User-Agent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.79 Safari/537.36'
}

# Headers needed for parsing


def getter_price(): # Function for returning the price of product
    page = requests.get(product_url, headers=headers) # Getting page data by using requests

    soup = BeautifulSoup(page.content, 'lxml') # Parsing the data in BeautifulSoup

    product_price = soup.find_all('span', class_='a-offscreen')[0].text[1:] #Getting the product_price from the parser,
                                                                            # and removing the currency sign using slicing

    final_price = '' # Empty string. Will be explained in next comment

    for i in product_price:             # Looping through each character in product price
        if i != ',':                    # If character is NOT A comma (,), then append character to the above empty string
            final_price += i            # appending

    return float(final_price)           # converting to decimal and returning


def price_drop(current_price): # Function to check whether the price is increased from the current value. Current value is parameter
    new_price = getter_price()
    if new_price < current_price:
        return True                 # Returns True if there is a price drop
    else:
        return False                # Returns False in all other cases


def initialise_window():        # Used for notifying the price drop and ok button takes you to the page
    root = tk.Tk()
    root.geometry("650x400")
    text = Label(root, text='Price Dropped!!', font=('Algerian Regular', 40)).place(x=35, y=90)
    ok_button = tk.Button(root, text="OK", font=("Arial"), relief=RAISED, command= lambda : webbrowser.open(product_url))
    ok_button.pack(side='bottom')
    ok_button.flash()
    root.mainloop()

    
current_price = getter_price()    
while True:
    if price_drop(current_price):
        initialise_window()
        quit()
    else:
        current_price = getter_price()
        time.sleep(60*60*24)
