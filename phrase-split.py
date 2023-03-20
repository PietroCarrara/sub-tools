# Takes in a srt file and splits each cue into more cues,
# for a max of one phrase per line.

import sys
import re
from datetime import timedelta
from srt import parse, compose, Subtitle

REGEX = r"(\.\.\.)|\.|\!|\?|\:"
REGEX_END = f"({REGEX})$"
GLUE = 50

# if len(sys.argv) != 2:
#   print(f'usage: {sys.argv[0]} in.srt >> out.srt')
#   sys.exit(1)

try:
	with open('in.srt', 'r') as f1:
		s1 = list(parse(f1.read()))
		out = list[Subtitle]()

		for i in range(len(s1)):
			curr = s1[i]

			if len(out) != 0 and (curr.start - out[-1].end) < timedelta(milliseconds=GLUE):
				prev = out[-1]

				if re.search(REGEX_END, prev.content) is None:
					match = re.search(REGEX, curr.content)
					if match is None:
						# No '.' found, this cue phrase doesn't end the phrase
						prev.content += ' ' + curr.content
						prev.end = curr.end
						curr.start = curr.end
					else:
						idx = match.end()
						# Cue duration * percentage removed
						duration = (curr.end - curr.start) * ((idx+1) / len(curr.content))
						prev.content += ' ' + curr.content[:idx+1]
						prev.end += duration
						curr.content = curr.content[idx+1:].strip()
						curr.start += duration

			if curr.start != curr.end:
				out.append(Subtitle(len(out)+1, curr.start, curr.end, curr.content))

		print(compose(out))

except Exception as e:
	raise e
	print(e)
	sys.exit(2)