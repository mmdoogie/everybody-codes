#!/usr/bin/env python3
import argparse
from datetime import date
from os import getenv
import sys
import time
import traceback

from dotenv import load_dotenv
import requests

import mrm.ansi_term as ansi

COLOR_PASS_STR = ansi.green('PASS')
COLOR_FAIL_STR = ansi.red('FAIL')

def do_submit(year, day, part, value):
    load_dotenv()
    token = getenv('EC_TOKEN')
    if token is None:
        print('Skipping submit: access token not found in .env')
        return

    cookies = {'everybody-codes': token}
    payload = '{ "answer": "' + str(value) + '" }'

    url = f'https://everybody.codes/api/event/{year}/quest/{day}/part/{part}/answer'
    r = requests.post(url, cookies=cookies, data=payload, timeout=5)
    r.raise_for_status()
    print(ansi.blue(r.text))

def run_daypart(year, day_num, part_num, output, submit):
    day_str = f'{day_num:02d}'
    day_module_name = f'ec_{year}.ec_{year}_{day_str}'

    result_module_name = f'data.ec_{year}.results'
    result_module = __import__(result_module_name, fromlist = [None])

    try:
        day_module = __import__(day_module_name, fromlist = [None])
    except Exception as ex:
        print(f'Year {year} day {day_str} not found or error running: {ex}')
        return 0, 0

    if day_num in result_module.results:
        results = result_module.results[day_num]
    else:
        results = None

    try:
        t_before = time.process_time()

        if part_num == 1:
            daypart_val = day_module.part1(output)
        elif part_num == 2:
            daypart_val = day_module.part2(output)
        else:
            daypart_val = day_module.part3(output)

        t_after = time.process_time()
        exec_time = round(t_after - t_before, 3)

        print(f'[{exec_time:>7.3f}] Day {day_str}, Part {part_num}: ', end='')
        if results is not None and part_num in results:
            if 'no_match' not in results or part_num not in results['no_match']:
                daypart_expect = results[part_num]
                passing = daypart_val == daypart_expect
                pf_str = COLOR_PASS_STR if passing else COLOR_FAIL_STR
                print(f'{daypart_val:<35}', f'{daypart_expect:<35}', pf_str)
            else:
                passing = True
                print(f'{daypart_val:<35}', f'expecting: {daypart_expect:<35}')
        else:
            passing = False
            print(f'{daypart_val:<35}')

        if submit:
            if not daypart_val:
                print(ansi.yellow('Result appears blank; skipping submit request.'))
            elif results is not None and part_num in results:
                print(ansi.yellow('Correct answer already populated in results; skipping submit request.'))
            else:
                do_submit(year, day_num, part_num, daypart_val)
    except Exception as ex:
        print(f'Day {day_str}, Part {part_num}: Not found or error running: {ex}')
        print(traceback.format_exc())
        sys.exit(1)

    return passing, exec_time

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('-y', type = int, help = 'Year to run.')
    ap.add_argument('-d', type = int, help = 'Day to run. 0 for all.')
    ap.add_argument('-p', type = int, choices = [1, 2, 3], help = 'Only runs specified part 1, 2, or 3.')
    ap.add_argument('-o', action = 'store_true', help = 'Show optional output. Ignored for -d0.')
    ap.add_argument('-s', action = 'store_true', help = 'Submit result via API. Only valid if day and part specified.')
    args = ap.parse_args()

    if not args.y:
        args.y = date.today().year

    # Current logic only works for 2024 event. Will need to see what next year brings.
    if not args.d:
        _, w, d = date.today().isocalendar()
        if w < 45 or w > 48 or d < 1 or d > 5:
            print('Day cannot be autodetermined. Please specify.')
            sys.exit(1)
        args.d = (w - 45) * 5 + d

    if args.y != 2024:
        print('Year must be 2024')
        sys.exit(1)

    if args.d < 0 or args.d > 20:
        print('Day must be between 1 and 20 inclusive.  Use 0 for all')
        sys.exit(1)

    if args.s and (args.d == 0 or args.p is None):
        print('Can only auto submit for a single specified day and part')
        sys.exit(1)

    part_nums = set([args.p]) if args.p else set([1, 2, 3])

    if args.d == 0:
        ansi.clear_screen()
        results = [run_daypart(args.y, day, part, False, False) for day in range(1, 21) for part in part_nums]
        passing = sum(r[0] for r in results)
        total_time = sum(r[1] for r in results)
        total_cnt = 20 * len(part_nums)
        print(f'[{total_time:>7.3f}] Passing:', passing, 'of', total_cnt)
    else:
        for part_num in part_nums:
            run_daypart(args.y, args.d, part_num, args.o, args.s)

if __name__ == '__main__':
    main()
