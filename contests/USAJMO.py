from .generic_AOPS import *

def random_problem(difficulty):
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
    source = 'USAJMO {0}, Problem {1}'.format(year, prob)
    return (source, get_problem(page))
