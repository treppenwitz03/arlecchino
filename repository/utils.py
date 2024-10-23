from io import BytesIO
import base64
import random
import string

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