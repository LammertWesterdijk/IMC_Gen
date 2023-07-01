from .generic_AOPS import *

def random_problem(difficulty):
    if difficulty < 7:
        return None
    year = random.randint(2000, 2023)
    json = get_comm_contest(3411, year)
    if json == None:
        return None
    # Derive what format was used as USA TST is very inconsistent
    num_probs = count_probs(json)
    if num_probs <= 0:
        return None
    # Determine problems per day
    daily_probs = 0
    if num_probs % 12 == 0: # cannot distinguish 3 and 4
        return None
    if num_probs % 3 == 0:
        daily_probs = 3
    elif num_probs % 4 == 0:
        daily_probs = 4
    if daily_probs == 0:
        return None
    days = num_probs // daily_probs

    # Calculate which problem best matches difficulty
    if difficulty >= 9:
        prob = daily_probs
    else:
        offs = int(((9 - difficulty) / 2) * (daily_probs - 1))
        if offs > daily_probs - 2:
            prob = 1
        else:
            prob = daily_probs - 1 - offs
    day = random.randint(0, days - 1)
    source = 'USA TST {0}, Day {1}, Problem {2}'.format(year, day + 1, prob)
    return (source, parse_comm(json, prob, day, daily_probs))
