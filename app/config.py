from pathlib import Path
import json

class Config:
  
  def __init__(self, path):
    if Path(path).is_file():
      self.path = path
    else:
      raise Exception('File \'%s\' doesn\'t exist' % path)

  def load(self):
    with open(self.path, 'r') as config:
      return json.load(config)

  def save(self, data):
    with open(self.path, 'w') as config:
      json.dump(data, config, indent = 2)
