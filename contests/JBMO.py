from .generic_AOPS import *

def random_problem(difficulty):
    if difficulty < 3.5 or difficulty > 7:
        return None
    year = random.randint(1998, 2023)
    if difficulty > 6:
        prob = 4
    elif difficulty > 4.5:
        prob = 2 + random.randint(0, 1)
    else:
        prob = 1
    source = 'Junior Balkan MO {0}, Problem {1}'.format(year, prob)
    json = get_comm_contest(3227, year)
    if json == None:
        return None
    return (source, parse_comm(json, prob))
