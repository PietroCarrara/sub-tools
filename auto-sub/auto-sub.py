#!/env/python

# Uses OpenAI's Whisper to transcribe a video, and then applies some
# rules to make the resulting subtitle more pleasing to read

# Rules
#  https://engagemedia.org/help/best-practices-for-online-subtitling/
#  https://www.gamedeveloper.com/audio/how-to-do-subtitles-well-basics-and-good-practices
#
#  - Minimum cue time: 1s
#  - If a cue starts mid-phrase and that phrase ends on it and a new one starts, this new phrase
#    must be finished right in this cue (i.e. it can't keep going through the next cue).
#  - Maximum of 38 characters per line and 2 lines per cue, totaling a max of 76 characters per cue

import whisper
import json
import sys

from words import Words
import rules

if len(sys.argv) != 3:
  print(f'usage: f{sys.argv[0]} <input> <model>')
  print(f'  example: f{sys.argv[0]} aud.aac tiny.en')
  print(f'  example: f{sys.argv[0]} out.json base.en')
  sys.exit(1)

fname = sys.argv[1]
modelName = sys.argv[2]

if fname.endswith('.json'):
  with open('auto-sub/dump.json', 'r') as f:
    res = json.load(f)
else:
  model = whisper.load_model(modelName)
  res = model.transcribe(fname, verbose=False, word_timestamps=True)
words = Words(res)

cues = rules.start(words)
rules.maxchars(cues)
srt = rules.end(cues)

with open('out.srt', 'w') as f:
  f.write(srt)