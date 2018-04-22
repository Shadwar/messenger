import os

path = os.path.dirname(os.path.abspath(__file__))

smiles_dict = {
    ':)': os.path.join(path, 'Slightly_Smiling_Face_Emoji.png'),
    ':D': os.path.join(path, 'Smiling_Face_with_Tightly_Closed_eyes.png'),
    ':(': os.path.join(path, 'Very_sad_emoji_icon_png.png'),
    ';)': os.path.join(path, 'Wink_Emoji.png')
}
