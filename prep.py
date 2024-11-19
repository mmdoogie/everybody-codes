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

def prep_template(fn, year, day):
    with open('_template.py', 'r', encoding='utf8') as in_file:
        in_data = in_file.read()
    in_data = re.sub('{YEAR}', str(year), in_data)
    in_data = re.sub('{DAY}', str(day), in_data)
    with open(fn, 'w', encoding='utf8') as out_file:
        out_file.write(in_data)

data_cache = {}

def decrypt_note(part):
    key_name = f'key{part}'
    if key_name not in data_cache['keys']:
        return None

    key_str = data_cache['keys'][key_name]
    key_str = key_str[:20] + '~' + key_str[21:]
    key_bytes = key_str.encode('utf8')
    note_bytes = bytes.fromhex(data_cache['notes'][str(part)])
    iv_bytes = key_bytes[:16]

    cipher = AES.new(key_bytes, AES.MODE_CBC, iv=iv_bytes)
    clear_note = cipher.decrypt(note_bytes)
    clear_note = unpad(clear_note, 16)

    return clear_note

def prep_data(fn, token, year, day, part):
    cookies = {'everybody-codes': token}

    if 'seed' not in data_cache:
        url = 'https://everybody.codes/api/user/me'
        r = requests.get(url, cookies=cookies, timeout=5)
        r.raise_for_status()
        data_cache['seed'] = r.json()['seed']

    if 'notes' not in data_cache:
        seed = data_cache['seed']
        url = f'https://everybody-codes.b-cdn.net/assets/{year}/{day}/input/{seed}.json'
        r = requests.get(url, cookies=cookies, timeout=5)
        r.raise_for_status()
        data_cache['notes'] = r.json()

    if 'keys' not in data_cache:
        url = f'https://everybody.codes/api/event/{year}/quest/{day}'
        r = requests.get(url, cookies=cookies, timeout=5)
        r.raise_for_status()
        data_cache['keys'] = r.json()

    clear_note = decrypt_note(part)
    if clear_note is None:
        print('Unable to fetch key for part. Exiting.')
        return False

    with open(fn, 'w', encoding='utf8') as out_file:
        out_file.write(clear_note.decode('utf8'))

    return True

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('-y', type = int, help = 'Year to prep.')
    ap.add_argument('-d', type = int, help = 'Day to prep.')
    ap.add_argument('-p', type = int, choices = [0, 1, 2, 3], help = 'Only preps specified part 1, 2, or 3. Use 0 for template.')
    ap.add_argument('-f', action = 'store_true', help = 'Force overwrite. Only valid with a specified part.')
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

    if args.d < 1 or args.d > 20:
        print('Day must be between 1 and 20 inclusive.')
        sys.exit(1)

    if args.f and args.p is None:
        print('Part must be specified to force overwrite.')
        sys.exit(1)

    part_nums = set([args.p]) if args.p is not None else set([0, 1, 2, 3])

    print(f'Prepping {args.y} Day {args.d}')

    if 0 in part_nums:
        template_file = f'ec_{args.y}/ec_{args.y}_{args.d}.py'
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

    if any(p in part_nums for p in [1, 2, 3]):
        load_dotenv()
        token = getenv('EC_TOKEN')
        if token is None:
            print('Access token not found in .env')
            sys.exit(1)

    part_names = {1: 'a', 2: 'b', 3: 'c'}
    for p in part_nums:
        if p == 0:
            continue
        data_file = f'data/ec_{args.y}/{args.d}-{part_names[p]}.txt'
        if path.isfile(data_file):
            print(f'{data_file} already exists, ', end='')
            if not args.f:
                print(ansi.yellow('skipping!'))
            else:
                print(ansi.red('overwriting!'))
                prep_data(data_file, token, args.y, args.d, p)
        else:
            print(ansi.green(f'Attempting to fetch input for part {p}.'))
            ok = prep_data(data_file, token, args.y, args.d, p)
            if not ok:
                break

if __name__ == '__main__':
    main()
