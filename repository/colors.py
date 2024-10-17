# colors for light mode
colors = {
    "black" : "#000000",
    "white" : "#ffffff",
    "fcffff": "#fcffff",
    "fafafa": "#fafafa",
    "f6f7f8": "#f6f7f8",
    "f8fafc": "#f8fafc",
    "d6d6d6": "#d6d6d6",
    "9a6e32": "#1c452f",
    "ae8948": "#30654c",
    "ebebeb": "#ebebeb",
    "c09451": "#4a8867",
    "c7ac65": "#66a581",
    "4d4d4d": "#4d4d4d",
    "a6a6a6": "#a6a6a6"
}

# colors for dark mode
colors_dark = {
    "black" : "#ffffff",
    "white" : "#1c1c1c",
    "fcffff": "#0d0d0d",
    "fafafa": "#101010",
    "f6f7f8": "#121212",
    "f8fafc": "#0f0f0f",
    "d6d6d6": "#404040",
    "9a6e32": "#3a7750",
    "ae8948": "#4d9a67",
    "ebebeb": "#2a2a2a",
    "c09451": "#26563a",
    "c7ac65": "#173726",
    "4d4d4d": "#999999",
    "a6a6a6": "#7a7a7a"
}

# get colors for the selected theme
def get_colors(dark_mode: bool):
    return colors_dark if dark_mode else colors