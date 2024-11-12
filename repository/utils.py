from io import BytesIO
import base64
import random
import string
import flet as ft
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad

key: str = None

# convert a given image byte to base64
def convert_to_base64(file: BytesIO):
    base64_content = base64.b64encode(file.getvalue()).decode('utf-8')
    
    return base64_content

# generate a random 8 string unique code
def generate_unique_code():
    res = ''.join(random.choices(
        string.ascii_letters +
        string.digits
        , k=8))
    
    return str(res)

def generate_random_name():
    characters = 'abcdef0123456789'
    
    # Generate the random message
    return ''.join(random.choice(characters) for _ in range(32))

# accepted month keywords
accepted_months = [
    "January", "February", "March", "April",
    "May", "June", "July", "August",
    "September", "October", "November", "December",
    
    "Jan", "Feb", "Mar", "Apr", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"
]

# the accepted currencies
currency_symbols = {
    "PHP": "₱",
    "USD": "$",
    "EU" : "€"
}

def generate_greeting():
    greetings = [
        "Hello", "Hi", "Hey", 
        "Greetings", "Howdy", "Welcome", 
        "My Salutations", "Yo", "Ahoy", 
        "Bonjour", "Hola", "Namaste",
        "Konnichiwa", "Kumusta", "Nihao",
        "Salaam", "Cheers", "Howzit", 
        "Sup", "Ciao", "Howdy-do", 
        "Heya", "G'day", "Peace", 
        "Shalom", "Hallo", "Let's do this", 
        "Good times", "Blessings be yours", "Aloha", 
        "Heyo", "Hiya", "Fun day's ahead", 
        "Hola mi amigo", "Warm greetings", 
        "Many welcomes to you", "Kind regards", 
        "Hi my friend", "Hey my buddy", "Yo mate", 
        "Glad tidings", "Hello there", "Hey there", 
        "Big welcome", "Much greetings", "High five", 
        "Heartfelt hello", "Mighty greetings", "Infinite welcomes", 
        "Vast hellos", "Cheers", "Good to see you", 
        "Warm regards", "Felicitations", "Best wishes",
        "Pleased to see you", "Pleased to have you", "Annyeonghaseyo",
    ]

    return random.choice(greetings)

def encrypt(data: str):
    if key:
        cipher = AES.new(key, AES.MODE_ECB)
        padded_text = pad(data.encode(), AES.block_size)
        ciphertext = cipher.encrypt(padded_text)

        return ciphertext.hex()

def decrypt(ciphertext: str):
    if key:
        ciphertext = bytes.fromhex(ciphertext)
        cipher = AES.new(key, AES.MODE_ECB)
        decrypted_text = unpad(cipher.decrypt(ciphertext), AES.block_size)
        
        return decrypted_text.decode()

def set_key(_key):
    global key
    key = _key

def initialize_settings(page: ft.Page):
    if page.client_storage.get("currency") is None:
        page.client_storage.set("currency", "PHP")
    if page.client_storage.get("dark_mode") is None:
        page.client_storage.set("dark_mode", False)

    if bool(page.client_storage.get("dark_mode")):
        page.theme_mode = ft.ThemeMode.DARK
    else:
        page.theme_mode = ft.ThemeMode.LIGHT

    if page.client_storage.get("accent_color") is None:
        page.client_storage.set("accent_color", "#8C161E")