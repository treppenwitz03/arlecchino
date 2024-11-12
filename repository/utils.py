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

def generate_greeting(lang: str):
    en_greetings = [
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

    tag_greetings = [
        "Kamusta", "Hoy", "Pagbati", "Mabuhay", "Maligayang araw", 
        "Aking Pagbati", "Oy", "Ahoy", "Magandang araw", "Ano na", 
        "Ayos lang?", "Hoy-hoy", "Kamusta ka", "Mapag-palang araw", "Tara na", 
        "Magandang buhay", "Pagpapala sa iyo", "Hoy-hoy", "Kumusta na", 
        "Anunaga", "Mainit na pagbati", "Malugod na pagbati", 
        "Kumusta buhay buhay", "Masayang pagbati", "Kumusta", 
        "Kumusta kaibigan", "Oy mate", "Magandang araw", "Kumusta ka", 
        "Andyan ka pala", "Maligayang pagbati", "Masayang pagbati", "High five", 
        "Ako sayo'y bumabati", "Hanunah", "Walang hanggang pagbati", 
        "Gudmorning", "Gudday", "Mainit na pagbati", 
        "Maligayang bati", "Gudmorneng",
        "Bonjour", "Hola", "Namaste", "Konnichiwa", "Nihao", 
        "Salaam", "Ciao", "Shalom", "Hallo", "Aloha", "Hola mi amigo", "Annyeonghaseyo"
    ]

    ceb_greetings = [
        "Kumusta", "Hoy", "Pagpanimbaya", "Mabuhi", "Maayong adlaw", 
        "Akong Pagpanimbaya", "Oy", "Ahoy", "Maayong adlaw", "Unsa na", 
        "Okay ra?", "Hoy-hoy", "Kumusta ka", "Mapanalangin nga adlaw", "Tara na", 
        "Maayong kinabuhi", "Panlanginan ka", "Hoy-hoy", "Kumusta na", 
        "Unsa ba", "Mainit nga pagpanimbaya", "Malipayon nga pagpanimbaya", 
        "Kumusta ang kinabuhi", "Malipayong pagpanimbaya", 
        "Kumusta amigo", "Oy mate", "Maayong adlaw", "Kumusta ka", 
        "Ania ra ka diay", "Malipayong pagpanimbaya", "Malipayong pagpanimbaya", "High five", 
        "Nagpanimbaya ko kanimo", "Unsa ba kaha", "Walay katapusang pagpanimbaya", 
        "Maayong buntag", "Maayong adlaw", "Mainit nga pagpanimbaya", 
        "Malipayong pagpanimbaya", "Maayong buntag",
        "Bonjour", "Hola", "Namaste", "Konnichiwa",  "Nihao", 
        "Salaam", "Ciao", "Shalom", "Hallo", "Aloha", "Hola mi amigo", "Annyeonghaseyo"
    ]

    esp_greetings = [
        "¿Cómo estás?", "Hola", "Saludos", "Viva", "Feliz día", 
        "Mis saludos", "Oye", "Ahoy", "Buen día", "¿Qué pasa?", 
        "¿Todo bien?", "Hola-hola", "¿Cómo te va?", "Día bendecido", "Vamos", 
        "Buena vida", "Bendiciones para ti", "Hola-hola", "¿Cómo va todo?", 
        "¿Qué hay?", "Saludos calurosos", "Saludos cordiales", 
        "¿Cómo va la vida?", "Saludos alegres", "¿Qué tal?", 
        "¿Cómo estás amigo?", "Oye amigo", "Buen día", "¿Cómo estás?", 
        "¡Ah, ahí estás!", "Saludos felices", "Saludos felices", "Choca esos cinco", 
        "Te saludo", "¿Qué será?", "Saludos infinitos", 
        "Buenos días", "Buen día", "Saludos calurosos", 
        "Felicitaciones", "Buenos días",
        "Bonjour", "Hola", "Namaste", "Konnichiwa", "Kumusta", "Nihao", 
        "Salaam", "Ciao", "Shalom", "Hallo", "Aloha", "Hola mi amigo", "Annyeonghaseyo"
    ]

    jp_greetings = [
        "こんにちは", "やあ", "おっす", "ご挨拶", "元気ですか？", 
        "ようこそ", "ご挨拶申し上げます", "ヨー", "アホイ", "乾杯", 
        "調子はどう?", "どうしたの？", "どうだい？", "やっほー", "おはよう", 
        "平和", "やろう", "良い時を", "あなたに祝福を", "ヘイヨー", 
        "こんにちは", "楽しい日が待っている", "温かいご挨拶", "あなたへの多くの歓迎", 
        "よろしく", "こんにちは友達", "やあ、友達", "ヨー、仲間", "良い知らせ", 
        "そこにこんにちは", "やあ、そこに", "大きな歓迎", "たくさんの挨拶", "ハイファイブ", 
        "心からの挨拶", "力強い挨拶", "無限の歓迎", "広大な挨拶", "乾杯", 
        "会えて嬉しい", "温かいご挨拶", "おめでとう", "最良の願い", "会えて嬉しい", 
        "お会いできて嬉しい", 
        # Non-English Greetings
        "ボンジュール", "オラ", "ナマステ", "こんにちは", "クムスタ", "ニーハオ", 
        "サラーム", "チャオ", "シャローム", "ハロー", "アロハ", "こんにちは、私の友達", 
        "アンニョンハセヨ"
    ]

    match lang:
        case "en":
            return random.choice(en_greetings)
        case "tag":
            return random.choice(tag_greetings)
        case "ceb":
            return random.choice(ceb_greetings)
        case "esp":
            return random.choice(esp_greetings)
        case "jp":
            return random.choice(jp_greetings)

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