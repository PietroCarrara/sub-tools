import regex as re
from math import ceil
from datetime import timedelta
from srt import Subtitle, compose

from words import Words, Word

phraseEnd = r"(?<!Dr|Mr|Sr|Mrs)(\.|\!|\?|:)"

MAX_CHARS_PER_CUE = 76

def start(words: Words) -> list[list[Word]]:
  cues: list[list[Word]] = []
  cue: list[Word] = []

  i = words.pop()
  while i is not None:
    cue.append(i)

    if re.search(phraseEnd, i.word, re.IGNORECASE):
      cues.append(cue)
      cue = []

    # Add a bit more time to be able to read better
    j = words.pop()
    if j is not None:
      j.start = max(i.end, j.start - timedelta(seconds=0.1))
      i.end = min(i.end + timedelta(seconds=0.1), j.start)
    i = j

  return cues

def maxchars(cues: list[list[Word]]):
  i = 0
  while i < len(cues):
    charcount = sum(map(lambda x: len(x.word), cues[i]))
    if charcount > MAX_CHARS_PER_CUE:
      n = ceil(charcount / MAX_CHARS_PER_CUE)
      parts = list(split(cues[i], n))
      del cues[i]
      for p in range(len(parts)):
        cues.insert(i+p, parts[p])

    i += 1

def end(cues: list[list[Word]]) -> Subtitle:
  res = []

  for i in range(len(cues)):
    res.append(words2sub(cues[i], i+1))

  return compose(res)

def words2sub(cue: list[Word], id = 0) -> Subtitle:
  start = cue[0].start
  end = cue[-1].end
  return Subtitle(id, start, end, ' '.join(map(lambda x: x.word, cue)))


def split(a, n):
    k, m = divmod(len(a), n)
    return (a[i*k+min(i, m):(i+1)*k+min(i+1, m)] for i in range(n))