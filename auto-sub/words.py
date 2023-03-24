from datetime import timedelta

class Word:
  def __init__(self, word: str, start: float, end: float):
    self.word = word
    self.start = timedelta(seconds=start)
    self.end = timedelta(seconds=end)

  def __str__(self) -> str:
    return f"[{self.start} --> {self.end}] {self.word}"

  def __repr__(self) -> str:
    return str(self)

class Words:
  def __init__(self, data):
    self.data = data
    self.segment = 0
    self.word = 0

  def peek(self) -> Word|None:
    w = self.__peek()
    if w is not None:
      w.word = w.word.strip()
    return w

  def __peek(self) -> Word|None:
    if self.segment < len(self.data['segments']) and self.word < len(self.data['segments'][self.segment]['words']):
      word = self.data['segments'][self.segment]['words'][self.word]
      return Word(word['word'], word['start'], word['end'])
    return None

  def __next(self) -> bool:
    self.word += 1
    if (self.word >= len(self.data['segments'][self.segment]['words'])):
      self.word = 0
      self.segment += 1
      if (self.segment >= len(self.data['segments'])):
        self.word = len(self.data['segments'][-1])-1
        self.segment = len(self.data['segments'])-1
        return False
    return True

  def pop(self) -> Word:
    w = self.peek()

    # Pop and check if next word is something like '-playing', that should be
    # 'role-playing' (i.e, not a different word) or '&D' from 'D&D'
    if w is not None and self.__next():
      n = self.__peek()
      if n.word.startswith('-') or not n.word.startswith(' '):
        w.word += n.word
        w.end = n.end
        self.__next()

    return w

  def isEmpty(self):
    return self.word >= len(self.data['segments'][self.segment]['words']) or self.segment >= len(self.data['segments'])