from lxml import etree
from io import StringIO
import requests
import random
import subprocess
import os

# IMC hates euclidean geometry
def has_eucl(tex):
    return 'ABC' in tex

# AOPS
def request_page(page):
    parser = etree.HTMLParser()

    headers = {'user-agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36'} # spoof browser to prevent being blocked
    res = requests.get(page, headers = headers)
    html = res.content.decode("UTF-8")
    tree = etree.parse(StringIO(html), parser=parser)
    return tree

def parse_p_tex(element):
    res = "" 
    raw = etree.tostring(element, encoding = 'unicode')
    in_tag = False
    in_text = False
    match = "alt="
    seen_alt = False
    mtch_inx = 0
    done_alt = False
    for c in raw:
        if c == '<' and not in_text:
            seen_alt = False
            mtch_inx = 0
            done_alt = False
            in_tag = True
        elif c == '>' and not in_text:
            in_tag = False
        elif c == '"':
            in_text = not in_text
            if not in_text and seen_alt:
                done_alt = True
        elif not in_tag:
            res += c
        elif in_text and seen_alt and not done_alt:
            res += c
        elif in_tag and c == match[mtch_inx] and not seen_alt:
            mtch_inx += 1
            if mtch_inx > 3:
                seen_alt = True
                mtch_inx = 0
        elif in_tag and c != match[mtch_inx]:
            mtch_inx = 0
    res = res.replace('&lt;', '<')
    res = res.replace('&gt;', '>')
    res = res.replace('&amp;', '&')
    res = res.replace('&quot;', '\"')
    return res

def get_problem(page):
    try:
        html_tree = request_page(page)
        for element in html_tree.iter():
            if element.get('class') == 'mw-parser-output':
                res = ""
                elements = element.getchildren()
                atproblem = False
                for e in elements:
                    try:
                        if e.tag[0] != 'h' and atproblem:
                           res += parse_p_tex(e) + '\n'
                        elif len(e.getchildren()) > 0 and ("Problem" in e.getchildren()[0].get('id') or "problem" in e.getchildren()[0].get('id')) and not atproblem:
                            atproblem = True
                        elif atproblem:
                            atproblem = False
                            break
                    except:
                        continue
                if res == "":
                    return None
                return res
        return None
    except:
        return None

def random_USAMO_problem(difficulty):
    if difficulty > 9.5 or difficulty < 6.5:
        return None
    year = random.randint(1996, 2023)
    if difficulty > 8.5:
        prob = 3
    elif difficulty > 7.5:
        prob = 2
    else:
        prob = 1
    prob += random.randint(0, 1) * 3
    page = 'https://artofproblemsolving.com/wiki/index.php/{0}_USAMO_Problems/Problem_{1}'.format(year, prob)
    return (page, get_problem(page))

def random_old_USAMO_problem(difficulty):
    if difficulty > 8.5 or difficulty < 6:
        return None
    year = random.randint(1972, 1995)
    if difficulty > 8:
        prob = 5
    elif difficulty > 7.25:
        prob = 4
    elif difficulty > 6.8:
        prob = 3
    elif difficulty > 6.5:
        prob = 2
    else:
        prob = 1
    page = 'https://artofproblemsolving.com/wiki/index.php/{0}_USAMO_Problems/Problem_{1}'.format(year, prob)
    return (page, get_problem(page))

def random_USAJMO_problem(difficulty):
    if difficulty > 7.9 or difficulty < 5:
        return None
    year = random.randint(2010, 2022)
    if difficulty > 7.2:
        prob = 3
    elif difficulty > 6.5:
        prob = 2
    else:
        prob = 1
    prob += random.randint(0, 1) * 3
    if year == 2020:
        page = 'https://artofproblemsolving.com/wiki/index.php/{0}_USOJMO_Problems/Problem_{1}'.format(year, prob)
    else:
        page = 'https://artofproblemsolving.com/wiki/index.php/{0}_USAJMO_Problems/Problem_{1}'.format(year, prob)
    return (page, get_problem(page))

def random_IMO_problem(difficulty):
    if difficulty < 6:
        return None
    if difficulty > 9:
        year = random.randint(2000, 2022)
    else:
        year = random.randint(1980, 2022) # no really old IMO problems
    scaled_difficulty = (2022 - year) / 50 + difficulty
    if scaled_difficulty > 9.5:
        prob = 3
    elif scaled_difficulty > 8:
        prob = 2
    else:
        prob = 1
    prob += random.randint(0, 1) * 3
    page = 'https://artofproblemsolving.com/wiki/index.php/{0}_IMO_Problems/Problem_{1}'.format(year, prob)
    return (page, get_problem(page))

def random_AIME_problem(difficulty):
    if difficulty > 6.5:
        return None
    if difficulty > 5.5:
        prob = random.randint(12,15)
    elif difficulty > 4.5:
        prob = random.randint(10,12)
    elif difficulty > 3.5:
        prob = random.randint(6,9)
    else:
        prob = random.randint(1,5)
    year = random.randint(1983, 2023)
    if year < 2000:
        page = 'https://artofproblemsolving.com/wiki/index.php/{0}_AIME_Problems/Problem_{1}'.format(year, prob)
    else:
        irt = random.randint(0,1)
        if irt == 0:
            page = 'https://artofproblemsolving.com/wiki/index.php/{0}_AIME_I_Problems/Problem_{1}'.format(year, prob)
        else:
            page = 'https://artofproblemsolving.com/wiki/index.php/{0}_AIME_II_Problems/Problem_{1}'.format(year, prob)
    return (page, get_problem(page))

# PUTNAM
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

def random_Putnam_problem(difficulty):
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

def random_problem(difficulty):
    while True:
        contest = random.randint(0, 7)
        if contest == 0:
            res = random_USAMO_problem(difficulty)
        elif contest == 1:
            res = random_old_USAMO_problem(difficulty)
        elif contest == 2:
            res = random_USAJMO_problem(difficulty)
        elif contest == 3 or contest == 4:
            res = random_IMO_problem(difficulty)
        elif contest == 5:
            res = random_AIME_problem(difficulty)
        elif contest == 6 or contest == 7:
            res = random_Putnam_problem(difficulty)
        if res != None and res[1] != None:
            return res

def generate_problems(mindif, maxdif, n, seed):
    problems = []
    i = 0
    log = ""
    while i < n:
        diff = mindif + (i / (n - 1)) * (maxdif - mindif)
        source, prob = random_problem(diff)
        if prob != None and not has_eucl(prob):
            problems.append(prob)
            log += source + '\n'
            i += 1
    res = ""
    for problem in problems:
        res += "\\begin{opg}\n"
        res += problem
        res += "\\end{opg}\n"
    return (log, res)

def generate_test(mindif, maxdif, n, seed):
    random.seed(seed)
    if not os.path.exists('./tests/IMC_{0}/'.format(seed)):
        os.mkdir('./tests/IMC_{0}/'.format(seed))
    with open('./tests/template.tex', 'r', encoding="utf-8") as t, open('./tests/IMC_{0}/IMC_{0}.tex'.format(seed), 'w', encoding="utf-8") as fw, open('./tests/IMC_{0}/IMC_{0}_Sources.txt'.format(seed), 'w', encoding="utf-8") as fl:
        template = t.read()
        log, problems = generate_problems(mindif, maxdif, n, seed)
        fw.write((template.replace('SEED', str(seed))).replace('PROBLEMS', problems))
        fl.write(log)
    subprocess.check_call('pdflatex -output-directory tests/IMC_{0}/ ./tests/IMC_{0}/IMC_{0}.tex'.format(seed))

def main():
    generate_test(8, 11, 5, random.randint(0, 1000000))
    
if __name__ == '__main__':
    main()
    #pass