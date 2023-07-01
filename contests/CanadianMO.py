from .generic_AOPS import *

def random_problem(difficulty):
    if difficulty < 4.5 or difficulty > 8.5:
        return None
    if difficulty > 7.5:
        year = random.randint(2000, 2023)
    else:
        year = random.randint(1980, 2023)
    scaled_difficulty = (2022 - year) / 100 + difficulty
    if scaled_difficulty > 8:
        prob = 5
    elif scaled_difficulty > 7.5:
        prob = 4
    elif scaled_difficulty > 6.5:
        prob = 3 + random.randint(0, 1)
    elif scaled_difficulty > 6:
        prob = 2 + random.randint(0, 1)
    else:
        prob = 1
    source = 'Canadian MO {0}, Problem {1}'.format(year, prob)
    json = get_comm_contest(3277, year)
    if json == None:
        return None
    return (source, parse_comm(json, prob))

