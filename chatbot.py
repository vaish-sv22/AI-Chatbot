import tkinter as tk
from tkinter import scrolledtext
from tkinter import messagebox
import asyncio
import aiohttp
import json
import time

API_KEY = "AIzaSyAxxc5thmNS2Z4wdsqkcIQsRcr2LU5XqTM"

API_URL = "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent"

# A global variable to hold the asyncio event loop
loop = None

# A simple flag to prevent multiple API calls at once
is_sending = False

def update_gui(text, tag=None):
    """A helper function to update the chat history from any function."""
    chat_history.config(state=tk.NORMAL)
    if tag:
        chat_history.insert(tk.END, text, tag)
    else:
        chat_history.insert(tk.END, text)
    chat_history.config(state=tk.DISABLED)
    chat_history.see(tk.END)

async def get_bot_response_async(user_input):
    """
    Makes an asynchronous API call to the language model to get a response.
    """

    # Show a loading indicator in the chat window
    update_gui("Bot: Thinking...\n")

    try:
        # Prepare the payload for the API call
        payload = {
            "contents": [
                {
                    "role": "user",
                    "parts": [{"text": user_input}]
                }
            ]
        }
        
        # Use exponential backoff for retries in case of transient errors
        retries = 3
        delay = 1

        # Use ClientSession for HTTP requests
        timeout = aiohttp.ClientTimeout(total=30)
        async with aiohttp.ClientSession(timeout=timeout) as session:
            
              for i in range(retries):
                try:
                    full_url = f"{API_URL}?key={API_KEY}"
                    async with session.post(full_url, json=payload, timeout=30) as response:
                        #response.raise_for_status() # Raise an exception for bad status codes
                        #result = await response.json()
                        if response.status != 200:
                            error = await response.text()
                            print("API Error:", error)
                            return "API Error. Check the terminal."
                        result = await response.json()

                        if result.get("candidates") and result["candidates"][0].get("content") and result["candidates"][0]["content"].get("parts"):
                            bot_response = result["candidates"][0]["content"]["parts"][0]["text"]
                            return bot_response
                        else:
                            # Handle cases where the API response structure is unexpected
                            print("API response structure is invalid:", result)
                            return "Error: Could not get a valid response from the model."
                except aiohttp.ClientError as e:
                    print(f"API call failed on attempt {i+1}: {e}")
                    if i < retries - 1:
                        await asyncio.sleep(delay)
                        delay *= 2
                    else:
                        raise # Re-raise the exception after all retries fail

    except Exception as e:
        print(f"An error occurred: {e}")
        return "Sorry, I am having trouble connecting right now. Please try again later."
    finally:
        # Remove the loading indicator
        chat_history.config(state=tk.NORMAL)
        start_of_thinking = chat_history.search("Thinking...", "1.0", stopindex=tk.END, backwards=True)
        if start_of_thinking:
            chat_history.delete(start_of_thinking, tk.END)
        chat_history.config(state=tk.DISABLED)

async def send_message(event=None):
    """
    This function is called when the user sends a message.
    It retrieves the user's input, updates the chat history,
    and then starts the async process to get the bot's response.
    """
    global is_sending
    user_input = user_entry.get()

    if user_input.strip() == "" or is_sending:
        return

    is_sending = True
    
    # Insert user's message into the chat history area
    update_gui(f"You: {user_input}\n", "user")
    user_entry.delete(0, tk.END)  # Clear the input box

    # Get bot's response and insert it into the chat history
    bot_response = await get_bot_response_async(user_input)
    update_gui(f"Bot: {bot_response}\n", "bot")
    
    is_sending = False
    chat_history.see(tk.END)

def on_send_button_click():
    """Wrapper function to run the async send_message coroutine."""
    # This function is the entry point from the Tkinter event loop
    asyncio.run_coroutine_threadsafe(send_message(), loop)

def run_async_in_tkinter(root, loop):
    """
    This function periodically runs the asyncio event loop.
    It's scheduled with root.after to integrate with Tkinter's main loop.
    """
    loop.run_until_complete(asyncio.sleep(0))
    root.after(10, lambda: run_async_in_tkinter(root, loop))


# --- Main Application Window Setup ---

def start_gui_and_loop():
    """Sets up the GUI and the asyncio event loop."""
    global loop, chat_history, user_entry

    root = tk.Tk()
    root.title("Cloud Institution_Chatbot")
    root.geometry("400x500")
    root.resizable(True, True)

    # Set up color scheme and fonts
    bg_color = "#000000"
    input_bg_color = "#f0f0f0"  
    send_btn_color = "#4CAF50"
    font_family = "Helvetica"
    font_size = 11

    root.configure(bg=bg_color)

    # Create a frame to hold the chat history and input widgets
    main_frame = tk.Frame(root, bg=bg_color, padx=10, pady=10)
    main_frame.pack(fill=tk.BOTH, expand=True)

    # Create the chat history display area with a scrollbar
    chat_history = scrolledtext.ScrolledText(
        main_frame,
        wrap=tk.WORD,
        state=tk.DISABLED,  # Initially disabled so users can't type here
        font=(font_family, font_size),
        bg=input_bg_color,
        fg="#333333",
        relief=tk.FLAT,
        bd=5,
        pady=5,
        padx=5
    )
    chat_history.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

    # Configure tags for different message styles
    chat_history.tag_configure("user", foreground="#007bff", justify="right")
    chat_history.tag_configure("bot", foreground="#333333", justify="left")

    # Create a frame for the user input and send button
    input_frame = tk.Frame(main_frame, bg=bg_color)
    input_frame.pack(fill=tk.X, pady=(0, 5))

    # Create the user input entry box
    user_entry = tk.Entry(
        input_frame,
        font=(font_family, font_size),
        bg=input_bg_color,
        fg="#333333",
        relief=tk.FLAT,
        bd=2,
        insertwidth=2
    )
    user_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 5))
    user_entry.bind("<Return>", lambda event: on_send_button_click()) # Bind Enter key

    # Create the send button
    send_button = tk.Button(
        input_frame,
        text="Send",
        command=on_send_button_click,
        bg=send_btn_color,
        fg="#ffffff",
        font=(font_family, font_size, "bold"),
        relief=tk.FLAT,
        bd=2
    )
    send_button.pack(side=tk.RIGHT)

    # Initialize the asyncio loop in a new thread
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    
    # Start the event loop in a new thread
    import threading
    threading.Thread(target=loop.run_forever, daemon=True).start()

    # Start the Tkinter main loop
    root.mainloop()

if __name__ == "__main__":
    start_gui_and_loop()
