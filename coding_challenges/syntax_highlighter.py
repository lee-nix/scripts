'''
Your MyRobot-specific (esoteric) scripting language called RoboScript only ever contains the following characters: F, L, R, the digits 0-9 and brackets (( and )). Your goal is to write a function highlight which accepts 1 required argument code which is the RoboScript program passed in as a string and returns the script with syntax highlighting. The following commands/characters should have the following colors:

F - Wrap this command around <span style="color: pink"> and </span> tags so that it is highlighted pink in our editor
L - Wrap this command around <span style="color: red"> and </span> tags so that it is highlighted red in our editor
R - Wrap this command around <span style="color: green"> and </span> tags so that it is highlighted green in our editor
Digits from 0 through 9 - Wrap these around <span style="color: orange"> and </span> tags so that they are highlighted orange in our editor
Round Brackets - Do not apply any syntax highlighting to these characters
'''


def highlight(code):
    from itertools import groupby
    colors = {'F': 'pink', 'L': 'red', 'R': 'green', 1: 'orange', 'P': 'P'}
    wrap_chars = lambda chars, color: f'<span style="color: {color}">{chars}</span>' if not color == 'P' else chars
    highlighted = ''
    for key, group in groupby(code, key=lambda i: 1 if i.isdigit() else 'P' if i in '()' else i):
        highlighted += wrap_chars(''.join(list(group)), colors[key])
    return highlighted


print(highlight('FFL((RR)LF)112(FFF)'))
