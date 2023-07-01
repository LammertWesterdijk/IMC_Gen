from .generic_AOPS import *

def random_problem(difficulty):
    if difficulty < 5.5 or difficulty > 8.5:
        return None
    if difficulty > 8:
        year = random.randint(2000, 2023)
    else:
        year = random.randint(1984, 2023)
    scaled_difficulty = (2022 - year) / 100 + difficulty
    if scaled_difficulty > 8:
        prob = 4
    elif scaled_difficulty > 7.5:
        prob = 3
    elif scaled_difficulty > 6.5:
        prob = 2
    else:
        prob = 1
    source = 'Balkan MO {0}, Problem {1}'.format(year, prob)
    json = get_comm_contest(3225, year)
    if json == None:
        return None
    return (source, parse_comm(json, prob))
