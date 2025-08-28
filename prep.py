#!/usr/bin/env python3
import argparse
from datetime import date
from os import getenv, path
import re
import sys

from Cryptodome.Cipher import AES
from Cryptodome.Util.Padding import unpad
from dotenv import load_dotenv
import requests

import mrm.ansi_term as ansi

class APIData:
    def __init__(self, token, year, day):
        self._cache = {}
        self._cookies = {'everybody-codes': token}
        self.year = year
        self.day = day

    def seed(self):
        if 'seed' in self._cache:
            return self._cache['seed']
        url = 'https://everybody.codes/api/user/me'
        r = requests.get(url, cookies=self._cookies, timeout=5)
        r.raise_for_status()
        self._cache['seed'] = r.json()['seed']
        return self._cache['seed']

    def notes(self):
        if 'notes' in self._cache:
            return self._cache['notes']
        url = f'https://everybody-codes.b-cdn.net/assets/{self.year}/{self.day}/input/{self.seed()}.json'
        r = requests.get(url, cookies=self._cookies, timeout=5)
        r.raise_for_status()
        self._cache['notes'] = r.json()
        return self._cache['notes']

    def keys(self):
        if 'keys' in self._cache:
            return self._cache['keys']
        url = f'https://everybody.codes/api/event/{self.year}/quest/{self.day}'
        r = requests.get(url, cookies=self._cookies, timeout=5)
        r.raise_for_status()
        self._cache['keys'] = r.json()
        return self._cache['keys']

def prep_template(fn, year, day):
    with open('_template.py', 'r', encoding='utf8') as in_file:
        in_data = in_file.read()
    in_data = re.sub('{YEAR}', str(year), in_data)
    in_data = re.sub('{DAY}', f'{day:02}', in_data)
    with open(fn, 'w', encoding='utf8') as out_file:
        out_file.write(in_data)

def decrypt_note(api, part):
    key_name = f'key{part}'
    keys = api.keys()
    if key_name not in keys:
        return None

    key_str = keys[key_name]
    key_bytes = key_str.encode('utf8')
    note_bytes = bytes.fromhex(api.notes()[str(part)])
    iv_bytes = key_bytes[:16]

    cipher = AES.new(key_bytes, AES.MODE_CBC, iv=iv_bytes)
    clear_note = cipher.decrypt(note_bytes)
    clear_note = unpad(clear_note, 16)

    return clear_note

def prep_data(fn, api, part):
    clear_note = decrypt_note(api, part)

    if clear_note is None:
        print('Unable to fetch key for part. Exiting.')
        return False

    with open(fn, 'w', encoding='utf8') as out_file:
        out_file.write(clear_note.decode('utf8'))

    return True

def update_results(api, force):
    result_module_name = f'data.ec_{api.year}.results'
    result_module = __import__(result_module_name, fromlist = [None])
    answers = {int(k[-1]): v for k, v in api.keys().items() if k.startswith('answer')}
    if api.day in result_module.results:
        current = result_module.results[api.day]
    else:
        current = {}
    if any(k in current and current[k] != answers[k] for k in answers):
        print('Current answers:', current)
        print('Conflict with received answers', answers)
        if not force:
            print(ansi.yellow('Skipping!'))
            return
        print(ansi.red('Overwriting!'))
    if force or any(k not in current for k in answers):
        print(ansi.blue('Results updated: ' + str(answers)))
        result_module.results[api.day] = answers
        result_module.results.save()
    else:
        print('Results already up to date')

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('-y', type = int, help = 'Year to prep.')
    ap.add_argument('-d', type = int, help = 'Day to prep.')
    ap.add_argument('-p', type = int, choices = [0, 1, 2, 3, 4], help = 'Only preps specified part 1, 2, or 3. Use 0 for template or 4 for answers.')
    ap.add_argument('-f', action = 'store_true', help = 'Force overwrite. Only valid with a specified part.')
    args = ap.parse_args()

    if not args.y:
        args.y = date.today().year

    # Current logic only works for 2024 event. Will need to see what next year brings.
    if not args.d and args.y == date.today().year == 2024:
        _, w, d = date.today().isocalendar()
        if w < 45 or w > 48 or d < 1 or d > 5:
            print('Day cannot be autodetermined. Please specify.')
            sys.exit(1)
        args.d = (w - 45) * 5 + d
    elif not args.d:
        print('Day must be specified.')
        sys.exit(1)

    valid_years = [2024, 1, 2]
    if args.y not in valid_years:
        print('Year must be in', valid_years)
        sys.exit(1)

    if args.y < 2000:
        valid_days = (1, 3)
    else:
        valid_days = (1, 20)
    if args.d < valid_days[0] or args.d > valid_days[1]:
        print(f'Day must be between {valid_days[0]} and {valid_days[1]} inclusive.')
        sys.exit(1)

    if args.f and args.p is None:
        print('Part must be specified to force overwrite.')
        sys.exit(1)

    part_nums = set([args.p]) if args.p is not None else set([0, 1, 2, 3, 4])

    print(f'Prepping {args.y} Day {args.d}')

    if 0 in part_nums:
        template_file = f'ec_{args.y}/ec_{args.y}_{args.d:02}.py'
        if path.isfile(template_file):
            print(f'{template_file} already exists, ', end='')
            if not args.f:
                print(ansi.yellow('skipping!'))
            else:
                print(ansi.red('overwriting!'))
                prep_template(template_file, args.y, args.d)
        else:
            print(ansi.green('Preparing template.'))
            prep_template(template_file, args.y, args.d)

    if any(p in part_nums for p in [1, 2, 3, 4]):
        load_dotenv()
        token = getenv('EC_TOKEN')
        if token is None:
            print('Access token not found in .env')
            sys.exit(1)
        api = APIData(token, args.y, args.d)

    part_names = {1: 'a', 2: 'b', 3: 'c'}
    for p in part_nums:
        if p in [0, 4]:
            continue
        data_file = f'data/ec_{args.y}/{args.d:02}-{part_names[p]}.txt'
        if path.isfile(data_file):
            print(f'{data_file} already exists, ', end='')
            if not args.f:
                print(ansi.yellow('skipping!'))
            else:
                print(ansi.red('overwriting!'))
                prep_data(data_file, api, p)
        else:
            print(ansi.green(f'Attempting to fetch input for part {p}.'))
            ok = prep_data(data_file, api, p)
            if not ok:
                break

    if any(p in part_nums for p in [1, 2, 3, 4]):
        update_results(api, args.f)

if __name__ == '__main__':
    main()
