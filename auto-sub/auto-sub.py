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
import regex as re
import json

from words import Words, Word
import rules


# model = whisper.load_model("tiny.en")
# res = model.transcribe("aud.aac", verbose=True, word_timestamps=True)
with open('auto-sub/dump.json', 'r') as f:
  res = json.load(f)
words = Words(res)

cues = rules.start(words)
rules.maxchars(cues)
srt = rules.end(cues)

print(srt)