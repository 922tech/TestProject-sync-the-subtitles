# low-level modules
import re
import datetime
import pandas as pd


def get_numbers(string: str) -> int:
  _number = ''.join([i for i in string if i.isnumeric()])
  return int(_number)


XML_SIGNS  = [
    '<c.white>',
     '</c.white>',
    '<c.mono_sans>',
    '</c.mono_sans>',
    '<c.mono_sans>',
     '<c.bg_transparent>',
    '</c.bg_transparent>','\n'
              ]

     
def clean_text(string: str=None, signs: list=XML_SIGNS) -> str:
  """
  Remove XML sings from text
  """
  text = "".join(string)
  for i in signs:
    text = text.replace(i, ' ')
  return text

def format_datetime(time: str) -> datetime.datetime:
  parsed_time = parse_time(time)
  datetime_object = datetime.datetime(2000, 1, 1, parsed_time['hour'], parsed_time['minute'], parsed_time['second'])
  return datetime_object


def parse_time(time_string: str) -> dict:
  parsed = re.findall('^(\d{2}):(\d{2}):(\d{2})',time_string)
  return {
    'hour':int(parsed[0][0]),
    'minute':int(parsed[0][1]),
    'second':int(parsed[0][2]),
}


class RawSubtitle:
  """
  Converts a file with .vtt format to python object with some attrs.
  Also tokenizes the .vtt content
  """
  def __init__(self, subtitle_path: str = None, offset: int = 14):
    self.subtitle_path = subtitle_path
    self._lines = None
    self._breaks =  None
    self._set_lines(offset)
    self._set_breaks()

  def _set_lines(self, offset):

     _lines = open(self.subtitle_path).readlines()[offset:]
     _lines[0] = '\n'
     self._lines = _lines

  def _set_breaks(self):
      self._breaks = [i for i in range(len(self._lines)) if self._lines[i] == '\n']

  def tokenized(self) -> list:
    # The algorithm works by selecting the items between every 2 single line breaks
    return [ self._lines[self._breaks[i]:self._breaks[i+1]][1:] for i in range(len(self._breaks)-1) ]


class Dialog:
  """
  A Dialog object is a representative of every dialog and
  encapsulates dialog data
  """
  def __init__(self, raw_dialog: list):
    self.number = get_numbers(raw_dialog[0])
    self.start = format_datetime(raw_dialog[1][:12-4])
    self.end = format_datetime(raw_dialog[1][17:29-4])
    self.metadata = raw_dialog[1][29:]
    self.text = raw_dialog[2:]

  def to_dict(self):
    return  {
        "number":self.number,
        "start": self.start.strftime("%H:%M:%S"),
        "end": self.end.strftime("%H:%M:%S"),
        "text": clean_text(self.text)
    }
  
  def __repr__(self) -> str:
    return f"""\n{self.number}\n {self.to_dict()['start']} -->
     {self.to_dict()['start']} {self.metadata}\n {"".join(self.text)}"""


class DialogFactory:
  """
  Factory with a  list of dialogs as the product
  """
  def __init__(self, subtitle_file_path: str) -> None:
    self.subtitle_file_path = subtitle_file_path
    self.dialogs = self.factory()

  def factory(self) -> list:
    _tokens = RawSubtitle(self.subtitle_file_path).tokenized()
    dialogs = [Dialog(token) for token in _tokens]
    return dialogs

 
  def write_to_vtt(self, file_name) -> None:
    with open(f'{file_name}.vtt', 'w') as f:
      for dialog in self.dialogs:
        f.write(f'\n{dialog}')
  
 