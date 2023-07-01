from lxml import etree
from io import StringIO
import requests
import random

# BBCode
def parse_BBCode(bbcode):
    # TODO parse BBCode to LaTeX
    return bbcode

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

# AOPS COMMUNITY POSTS
def extract_comm_id(res):
    uid = None
    for ln in res.text.split('\n'):
        if 'AoPS.session' in ln:
            inx = ln.find('\"id\":')
            if inx < 0:
                return None
            inx += 4
            uid = ""
            inquotes = False
            while inx < len(ln):
                if ln[inx] == '\"' or ln[inx] == '\'':
                    inquotes = not inquotes
                    if not inquotes:
                        break
                elif inquotes:
                    uid += ln[inx]
                inx += 1
    return uid

def get_comm_contest(contest_id, year):
    # Start up session
    sesh = requests.Session()
    headers = {'user-agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36'} # spoof browser to prevent being blocked
    res = sesh.get('https://artofproblemsolving.com/community/c{0}'.format(contest_id), headers = headers)
    if res.status_code != 200:
        return None
    # Attempt to extract user id
    uid = extract_comm_id(res)
    if uid == None:
        return None

    # Extract contest id's for each year
    data = {'category_id' : str(contest_id), 'a' : 'fetch_category_data', 'aops_session_id' : uid, 'aops_user_id' : '1', 'aops_logged_in' : 'false'}
    res2 = sesh.post('https://artofproblemsolving.com/m/community/ajax.php', headers = headers, data = data)

    # Return matching year
    try:
        for item in res2.json()['response']['category']['items']:
            if int(item['item_score']) == year:
                year_id = item['item_id']
                data = {'category_id' : str(year_id), 'a' : 'fetch_category_data', 'aops_session_id' : uid, 'aops_user_id' : '1', 'aops_logged_in' : 'false'}
                res3 = sesh.post('https://artofproblemsolving.com/m/community/ajax.php', headers = headers, data = data)
                if res3.status_code != 200:
                    return None
                return res3.json()
    except:
        pass
    return None

# Selects problem 'prob' from a contest. 'prob_inx' indicates which matching problem to choose,
# for instance if there are multiple days and problems are labeled 123123. 'mod' helps with other
# irregularities, for instance if problems are labeled 123412 (over 3 days), mod 2 will change this
# to 121212 for easy enumeration.
def parse_comm(json, prob, prob_inx = 0, mod = 1000000):
    curr_inx = 0
    try:
        for item in json['response']['category']['items']:
            try:
                if len(item['item_text']) < 1:
                    continue
                prob_num = int(item['item_text'])
            except:
                try:
                    if len(item['item_text']) < 2:
                        continue
                    prob_num = int(item['item_text'][1:]) # Perhaps like "P1" as with the Chinese TST
                except:
                    continue
            if prob_num % mod == prob % mod:
                if curr_inx == prob_inx:
                    return parse_BBCode(item['post_data']['post_canonical'])
                curr_inx += 1
    except:
        pass
    return None

def count_probs(json):
    curr_cnt = 0
    try:
        for item in json['response']['category']['items']:
            try:
                if len(item['item_text']) < 1:
                    continue
                prob_num = int(item['item_text'])
            except:
                try:
                    if len(item['item_text']) < 2:
                        continue
                    prob_num = int(item['item_text'][1:]) # Perhaps like "P1" as with the Chinese TST
                except:
                    continue
            curr_cnt += 1
    except:
        return 0
    return curr_cnt
