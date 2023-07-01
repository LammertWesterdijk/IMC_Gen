from .generic_AOPS import *

def random_problem(difficulty):
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
    source = 'IMO {0}, Problem {1}'.format(year, prob)
    return (source, get_problem(page))
