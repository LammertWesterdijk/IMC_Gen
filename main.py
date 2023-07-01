from lxml import etree
from io import StringIO
import requests
import random
import subprocess
import os
import argparse
from contests import USAMO, USAJMO, IMO, AIME, Putnam, BMO, CanadianMO, JBMO


# Version support
VERSION = 'v0.3'

# IMC hates euclidean geometry
def has_eucl(tex):
    return 'ABC' in tex

# TEST GENERATION
def random_problem(difficulty):
    while True:
        contest = random.randint(0, 8)
        if contest == 0:
            res = USAMO.random_problem(difficulty)
        elif contest == 1:
            res = USAJMO.random_problem(difficulty)
        elif contest == 2:
            res = IMO.random_problem(difficulty)
        elif contest == 3:
            res = AIME.random_problem(difficulty)
        elif contest == 4 or contest == 5: # Putnam-type problems are underrepresented so 2x.
            res = Putnam.random_problem(difficulty)
        elif contest == 6:
            res = BMO.random_problem(difficulty)
        elif contest == 7:
            res = CanadianMO.random_problem(difficulty)
        elif contest == 8:
            res = JBMO.random_problem(difficulty)
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

def generate_contestid(args):
    return '_'.join([str(args.seed), str(args.diff_lo), str(args.diff_hi), str(args.num_prob)]) + '({0})'.format(VERSION)

def generate_test(args):
    seed = args.seed
    mindif = args.diff_lo
    maxdif = args.diff_hi
    n = args.num_prob
    contestid = generate_contestid(args)
    random.seed(seed)
    if not os.path.exists('./generated/IMC_{0}/'.format(contestid)):
        os.mkdir('./generated/IMC_{0}/'.format(contestid))
    with open('./generated/template.tex', 'r', encoding="utf-8") as t, open('./generated/IMC_{0}/IMC_{0}.tex'.format(contestid), 'w', encoding="utf-8") as fw, open('./generated/IMC_{0}/IMC_{0}_Sources.txt'.format(contestid), 'w', encoding="utf-8") as fl:
        template = t.read()
        log, problems = generate_problems(mindif, maxdif, n, seed)
        fw.write((template.replace('SEED', str(seed))).replace('PROBLEMS', problems))
        fl.write(log)
    subprocess.check_call('pdflatex -output-directory generated/IMC_{0}/ ./generated/IMC_{0}/IMC_{0}.tex'.format(contestid))
    
if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='IMC-Gen')
    parser.add_argument('-n','--num_prob', action="store", default = 5, dest='num_prob', help="number of problems in test", type = int)
    parser.add_argument('-dl','--diff_lo', action="store", default = 6, dest='diff_lo', help="minimum difficulty (first problem)", type = int)
    parser.add_argument('-dh','--diff_hi', action="store", default = 10, dest='diff_hi', help="maximum difficulty (last problem)", type = int)
    parser.add_argument('-s','--seed', action="store", default = random.randint(0, 1000000), dest='seed', help="random seed", type = int)
    args = parser.parse_args()
    generate_test(args)
