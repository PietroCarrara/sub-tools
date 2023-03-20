# Joins two srt files that have a matching number of entries,
# the use case being to grab a srt file, machine-transle it,
# join the two and edit the output on aegisub to make manual
# revisions using the translation tool.

import sys
from srt import parse, compose, Subtitle

if len(sys.argv) != 3:
  print(f'usage: {sys.argv[0]} <file1.srt> <file2.srt>')
  sys.exit(1)

try:
  with open(sys.argv[1], 'r') as f1, open(sys.argv[2], 'r') as f2:
    s1 = list(parse(f1.read()))
    s2 = list(parse(f2.read()))
    out = list()

    if len(s1) != len(s2):
      raise Exception(f"subtitles must have a matching number of entries! file 1 has {len(s1)} and file 2 has {len(f2)}!")

    for i in range(len(s1)):
      out.append(Subtitle(i+1, s1[i].start, s1[i].end, s1[i].content + '\n' + s2[i].content))

    print(compose(out))

except Exception as e:
  print(e)
  sys.exit(2)