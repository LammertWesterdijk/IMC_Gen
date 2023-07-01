from .generic_AOPS import *

def random_problem(difficulty):
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
        source = 'AIME {0}, Problem {1}'.format(year, prob)
    else:
        irt = random.randint(0,1)
        if irt == 0:
            page = 'https://artofproblemsolving.com/wiki/index.php/{0}_AIME_I_Problems/Problem_{1}'.format(year, prob)
            source = 'AIME I {0}, Problem {1}'.format(year, prob)
        else:
            page = 'https://artofproblemsolving.com/wiki/index.php/{0}_AIME_II_Problems/Problem_{1}'.format(year, prob)
            source = 'AIME II {0}, Problem {1}'.format(year, prob)
    return (source, get_problem(page))
