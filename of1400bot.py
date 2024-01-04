import asyncio
import requests
from bs4 import BeautifulSoup
from telegram import Bot

# Replace with your actual bot token and chat ID
telegram_token = "6901584899:AAG05QPi8F2chGZ65XayDniDT8rF8E0Doy4"
chat_id = "990284196"

# eBay Kleinanzeigen search URL with the specified keywords
search_url = "https://www.kleinanzeigen.de/s-festool-of-1400/k0"

# Previous state of the search results
previous_state = set()

async def check_product():
    global previous_state

    # Fetch the current state of the eBay Kleinanzeigen search results
    response = requests.get(search_url)
    soup = BeautifulSoup(response.text, 'html.parser')
    
    # Extract product titles from the search results
    current_state = {listing.text.strip() for listing in soup.select('.text-module-begin h2.text-module-begin')}
    
    # Check for new products
    new_products = current_state - previous_state
    
    if new_products:
        # Send a Telegram message for each new product
        bot = Bot(token=telegram_token)
        for product in new_products:
            message = f"New product uploaded: {product}"
            bot.send_message(chat_id=chat_id, text=message)

    # Update previous state
    previous_state = current_state

# Run the asynchronous function in the event loop
loop = asyncio.get_event_loop()
loop.run_until_complete(check_product())
