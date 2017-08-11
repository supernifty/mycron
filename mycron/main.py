#!/usr/bin/env python
'''
  read crontab file and run a cronjob service
    minutes = 0-59
    hours = 0-23
    days = 1-31
    months = 1-12
    dow = 0-6 sunday = 0
  Usage:
    python mycron.py < crontab
'''

import argparse
import collections
import datetime
import logging
import os
import sys
import time

def parse_field(field, max_val):
  result = set()
  for v in field.split(','):
    if '*' in v:
      result.update(list(range(0, max_val+1)))
    elif '-' in v:
      start, finish = v.split('-')
      result.update(list(range(int(start), int(finish) + 1)))
    else:
      result.add(int(v))
  return result

def parse_command(fields):
  return {
    'minutes': parse_field(fields[0], 59),
    'hours': parse_field(fields[1], 23),
    'days': parse_field(fields[2], 31),
    'months': parse_field(fields[3], 12),
    'dow': parse_field(fields[4], 6),
    'command': fields[5]
  }

def can_run(current, command):
  return current.minute in command['minutes'] and \
    current.hour in command['hours'] and \
    current.day in command['days'] and \
    current.month in command['months'] and \
    (current.weekday() + 1) % 7 in command['dow']

def run_command(command, dry, background=True):
  if dry:
    logging.info('would run %s', command)
  else:
    logging.info('running "%s"...', command)
    if background:
      os.system("{} &".format(command))
    else:
      os.system(command)
    logging.info('running "%s": done', command)

def mycron(fh_in, dry, background):
  '''
    run a crontab service
  '''
  logging.info("reading crontab...")
  commands = []
  for idx, line in enumerate(fh_in):
    if line.startswith('#'):
      continue
    fields = line.strip().split(' ', 5)
    if len(fields) != 6:
      logging.warn('Line %i: expected 6 fields, got %i', idx, len(fields))
    commands.append(parse_command(fields))

  logging.debug(commands)
  logging.info("checking for commands to run...")
  last_check = datetime.datetime.now()
  while True:
    logging.debug("checking...")
    # get current time
    current = datetime.datetime.now()
    while last_check < current:
      for command in commands:
        if can_run(last_check, command):
          run_command(command['command'], dry, background)
      last_check += datetime.timedelta(seconds=60)
    time.sleep(30)
        
    
  logging.info("done")

def main():
  parser = argparse.ArgumentParser(description='crontab service')
  parser.add_argument('--verbose', required=False, action='store_true')
  parser.add_argument('--dry', required=False, action='store_true')
  parser.add_argument('--background', required=False, action='store_true')
  args = parser.parse_args()
  if args.verbose:
    logging.basicConfig(format='%(asctime)s %(levelname)s %(message)s', level=logging.DEBUG)
  else:
    logging.basicConfig(format='%(asctime)s %(levelname)s %(message)s', level=logging.INFO)
  mycron(sys.stdin, args.dry, args.background)

if __name__ == '__main__':
  main()
