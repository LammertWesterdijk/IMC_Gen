from .generic_AOPS import *

def random_problem(difficulty):
    new = random.randint(0, 1)
    if new == 1:
        return random_USAMO_problem(difficulty)
    else:
        return random_old_USAMO_problem(difficulty)

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
    source = 'USAMO {0}, Problem {1}'.format(year, prob)
    return (source, get_problem(page))

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
    source = 'USAMO {0}, Problem {1}'.format(year, prob)
    return (source, get_problem(page))
