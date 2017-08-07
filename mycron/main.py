#!/usr/bin/env python
'''
  read crontab file and run a cronjob service
  Usage:
    python mycron.py < crontab
'''

import argparse
import collections
import logging
import sys

def mycron(fh_in):
  '''
    run a crontab service
  '''
  logging.info("reading crontab...")
  for line in fh_in:
    if line.startswith('#'):
      continue

  logging.info("waiting for next command to run...")
  logging.info("done")

def main():
  parser = argparse.ArgumentParser(description='crontab service')
  parser.add_argument('--verbose', required=False, action='store_true')
  args = parser.parse_args()
  if args.verbose:
    logging.basicConfig(format='%(asctime)s %(levelname)s %(message)s', level=logging.DEBUG)
  else:
    logging.basicConfig(format='%(asctime)s %(levelname)s %(message)s', level=logging.INFO)
  mycron(sys.stdin)

if __name__ == '__main__':
  main()
