import requests
import random

def request_putnam(year):
    headers = {'user-agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36'} # spoof browser to prevent being blocked
    res = requests.get('https://kskedlaya.org/putnam-archive/{0}.tex'.format(year), headers = headers)
    if res.status_code == 200:
        return res.text
    return None

def parse_putnam(tex, prob):
    res = ""
    if prob > 6:
        mtch1 = '\\item[B{0}]'.format(prob - 6)
        mtch2 = '\\item[B--{0}]'.format(prob - 6)
    else:
        mtch1 = '\\item[A{0}]'.format(prob)
        mtch2 = '\\item[A--{0}]'.format(prob)
    lines = tex.split('\n')
    seenitem = False
    enumdepth = 0
    for ln in lines:
        if seenitem and '\\begin{itemize}' in ln or '\\begin{enumerate}' in ln:
            enumdepth += 1
        elif seenitem and '\\end{itemize}' in ln or '\\end{enumerate}' in ln:
            enumdepth -= 1
            if enumdepth < 0:
                break
        if seenitem and '\\item' in ln and enumdepth == 0:
            break
        if seenitem:
            res += ln + '\n'
        if mtch1 in ln or mtch2 in ln:
            seenitem = True
    if res == "":
        return None
    return res

def random_problem(difficulty):
    if difficulty < 6:
        return None
    if difficulty > 9:
        year = random.randint(2000, 2022)
    else:
        year = random.randint(1985, 2022)
    scaled_difficulty = (2022 - year) / 50 + difficulty
    if scaled_difficulty > 9:
        prob = 6
    elif scaled_difficulty > 8.5:
        prob = 4 + random.randint(0, 1)
    elif scaled_difficulty > 7.5:
        prob = 2 + random.randint(0, 1)
    else:
        prob = 1
    prob += random.randint(0, 1) * 6
    source = 'Putnam {0}, Problem {1}'.format(year, prob)
    tex = request_putnam(year)
    if tex == None:
        return None
    return (source, parse_putnam(tex, prob))
