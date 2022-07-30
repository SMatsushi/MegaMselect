#!/usr/bin/env python3

import random
import argparse
from re import I

parser = argparse.ArgumentParser()
parser.add_argument('-c', '--chkJp', action='store_true',
	help='Check Jackpot in ticket purchased, which is defined in the code')
parser.add_argument('-j', '--jpFind', default=0,
	help='Try to find jackpot. Spedified number is prise, 1=until jackpod, 2=until 2nd prize')
args = parser.parse_args()
chkJp = False
if args.chkJp:
    chkJp = True
jpFind = int(args.jpFind)

# check jackpot
jp_ball = dict.fromkeys([7, 29, 60, 63, 66], True)
jp_mega = dict.fromkeys([15], True)

ball_bin = tuple(range(1, 70))
mega_bin = tuple(range(1, 25))
dict = {}   # empty dictionary
rnd_seed = 12345678     # example, modify it for better lack

cr_assoc = {}  # candidate-res assoc: associated with n_appear to search
#  n_appear    m_candi  m_cur  [results] [ticket_purchased]
cr_assoc[1] = [5, 0, [], {5:True}]    #  5 of first appear
cr_assoc[2] = [20, 0, [], {1:True, 5:True, 8:True}]   # 20 of appear twice
cr_assoc[3] = [6, 0, [], {5:True}]    #  6 of appear 3 times

random.seed(rnd_seed)
dict = {}   # empty dictionary

loop = 0
loop_check_mod = 500000
srch_str = ""
single_pick = False # true if n_apper = 1 exists
n_multi_pick = 0    # show number of n_apper > 1 cases
for key in cr_assoc.keys():
    srch_str += f"({key},{cr_assoc[key][0]}),"

print(f"Search (n_appear, m_candi) = {srch_str} rndSeed={rnd_seed} ...")
if jpFind > 0:
    print(f" continue to find #{jpFind} prize.")

hl_green = "\033[1;32m"
hl_yellow = "\033[1;33m"
hl_pink = "\033[1;35m"
hl_out = "\033[0m"
def jackpotChk(balls, mega):
    b_str, m_str = '',''
    b_match, m_match = 0, 0
    for b in balls:
        if b in jp_ball:
            b_str += f"{hl_pink}{b}{hl_out},"
            b_match += 1
        else:
            b_str += f"{b},"

    if mega in jp_mega:
        m_str = f"{hl_pink}{mega}{hl_out}"
        m_match += 1
    else:
        m_str = f"{mega}"
    return [b_str, m_str, b_match, m_match]

findJpLoop = False
while True:
    b_picked = sorted(random.sample(ball_bin, 5))
    m_picked = random.choice(mega_bin)
    rnd_picked = f"{b_picked}{m_picked}"
    loop += 1
    n_appear = 1
    if rnd_picked in dict:
        dict[rnd_picked] += 1
        n_appear = dict[rnd_picked]
    else:
        dict[rnd_picked] = 1
    done = True
    if findJpLoop:
        done = False
        # if n_appear > 1:
        cr_assoc[n_appear][1] += 1
        ckres = jackpotChk(b_picked, m_picked)
        if ckres[2] >= 4:  # above 4th prize
#            if ckres[2] == 5 or ckres[3] == 1:  # above 3nd
            print(f"{m}: {ckres[0]} Mega:{ckres[1]} : {n_appear} times at loop {loop}")
            if ckres[2] == 5:  # above 2nd prize
                if jpFind >= 2: # 2nd found break
                    break
                else:
                    if ckres[3] > 0:   #  jackpot
                        break
    else:
        cr_assoc[n_appear][1] += 1
        m = cr_assoc[n_appear][1]   # m_candi count
        if m <= cr_assoc[n_appear][0]:  # needed m_candi
            if chkJp or jpFind > 0:
                ckres = jackpotChk(b_picked, m_picked)
                if m in cr_assoc[n_appear][3]:
                    # tiecket bought
                    cr_assoc[n_appear][2].append(f"{hl_green}{m}:{hl_out} {ckres[0]} Mega:{ckres[1]} {hl_green}: {n_appear} times at loop {loop}{hl_out}")
                else:
                    cr_assoc[n_appear][2].append(f"{m}: {ckres[0]} Mega:{ckres[1]} : {n_appear} times at loop {loop}")
            else:
                cr_assoc[n_appear][2].append(f"{m}: {b_picked}, Mega:{m_picked} : {n_appear} times at loop {loop}")
        for key in cr_assoc.keys():
            if cr_assoc[key][1] < cr_assoc[key][0]:  # not done as m_candi count < needed m_candi
                done = False
                break
    if done or ((loop % loop_check_mod) == 1):
        srch_str = ""
        for key in cr_assoc.keys():
            srch_str += f"({key},{cr_assoc[key][1]}),"
        print(f"loop={loop} (na, nc)={srch_str} done={done}")
    if done:
        for key in cr_assoc.keys():
            print(f"{key} appear:")
            for res in cr_assoc[key][2]:
                print(f" {res}")
            print()
        if jpFind > 0:
            # cr_assoc[1][1] = None
            findJpLoop = True
        else:
            break
