# Finds lines that contain no '\n' and start with '-', removing the '-'

import sys
from srt import parse, compose

def hyphen(srt):
  for line in srt:
    s = line.content
    if '\n' not in s:
      strip = s.replace('<i>', '').replace('</i>', '').strip()
      if strip.startswith('- '):
        line.content = s.replace('- ', '')
      elif strip.startswith('-'):
        line.content = s.replace('-', '')

if len(sys.argv) != 2:
  print(f'usage: {sys.argv[0]} <file.srt>')
  sys.exit(1)

try:
  with open(sys.argv[1], 'r') as file:
    contents = file.read()
    s = list(parse(contents))
    hyphen(s)
    print(compose(s))

except Exception as e:
  print(e)
  sys.exit(2)