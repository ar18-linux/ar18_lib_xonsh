#! /usr/bin/env xonsh

import weakref
import subprocess
import sys

def install_pip_package(package):
  subprocess.check_call([sys.executable, "-m", "pip", "install", package])


class Ar18:
  internals = [
    "__parent"
  ]
  class Struct:
    class __Iterator:
      def __init__(self, parent):
        self.parent = parent
        self.index = 0
        self.keys = list(parent.__dict__)

      def __next__(self):
        if self.index < len(self.keys):
          key = self.keys[self.index]
          self.index += 1
          if key[0:2] != "__":
            result = self.parent.__dict__[key]
            return result
          else:
            return self.__next__()
        raise StopIteration

    try:
      import json5 as __json5
    except ModuleNotFoundError:
      install_pip_package("json5")
      import json5 as __json5
    def __init__(self, object=None, parent=None):
      if parent:
        self.__dict__[Ar18.internals[0]] = weakref.ref(parent)
      else:
        self.__dict__[Ar18.internals[0]] = None
      if isinstance(object, str):
        try:
          object = self.__json5.loads(open(object).read())
        except (ValueError, FileNotFoundError):
          object = None
      elif isinstance(object, Ar18.Struct):
        object = object.dict()
      if isinstance(object, dict):
        for key, item in object.items():
          if isinstance(item, dict):
            self[key] = Ar18.Struct(item)
          else:
            self[key] = item
  
    def __setattr__(self, key, value):
      return self.__setitem__(key, value)
  
    def __setitem__(self, key, value):
      if key in Ar18.internals:
        raise ValueError(f"Keyword [{key}] is reserved.")
      if isinstance(value, dict):
        self.__dict__[key] = Ar18.Struct(value, self)
      elif isinstance(value, Ar18.Struct):
        value.__dict__[Ar18.internals[0]] = self
        self.__dict__[key] = value
      else:
        self.__dict__[key] = value
  
    def __getattr__(self, item):
      return self.__getitem__(item)
  
    def __getitem__(self, item):
      if not item in self.__dict__:
        if self.__dict__[Ar18.internals[0]]:
          return self.__dict__[Ar18.internals[0]].__getitem__(item)
        else:
          self.__dict__.__setitem__(item, Ar18.Struct(parent=self))
      return self.__dict__[item]
  
    def __bool__(self):
      return len(self) != 0
    
    def __contains__(self, item):
      return item in self.dict()
    
    def __eq__(self, other):
      ret = True
      if len(self) != len(other):
        ret = False
      else:
        for key, value in self.items():
          if self[key] != other[key]:
            ret = False
            break
            
      return ret
    
    def __gt__(self, other):
      return len(self) > len(other)
    
    def __ge__(self, other):
      return len(self) >= len(other)
    
    def __lt__(self, other):
      return len(self) < len(other)
    
    def __le__(self, other):
      return len(self) <= len(other)
    
    def __add__(self, other):
      ret = Ar18.Struct(self)
      for key, value in other.items():
        if not key in ret:
          ret[key] = value
        else:
          if type(ret[key]) != type(value):
            raise ValueError("Same key, different type.")
          if isinstance(value, (str,int,float,bool)):
            if ret[key] != value:
              raise ValueError("Same key, different value.")
          elif not isinstance(value, (type(None))):
            if ret[key] != value:
              ret[key] += value
            
      return ret
            
  
    def __delitem__(self, key):
      if key in self.__dict__:
        del self.__dict__[key]
  
    def __delattr__(self, key):
      if key in self.__dict__:
        del self.__dict__[key]

    def __iter__(self):
      return self.__Iterator(self)

    def __len__(self):
      return len(self.__dict__) - len(Ar18.internals)

    def __repr__(self, indent=2):
      s_indent = " " * indent
      ret = "{\n"
      for key, item in self.__dict__.items():
        if key not in Ar18.internals:
          if isinstance(item, Ar18.Struct):
            ret += s_indent + "\"" + key + "\": " + item.__repr__(indent + 2)
          elif isinstance(item, list):
            ret += s_indent + "\"" + key + "\": [\n"
            for itm in item:
              ret += " " * (indent + 2) + itm.__repr__() + ",\n"
            ret += s_indent + "],\n"
          else:
            ret += s_indent + "\"" + key + "\": " + item.__repr__() + ",\n"
      ret += " " * (indent - 2) + "}"
      if self.parent():
        ret += ",\n"
      else:
        ret += "\n"
      return ret

    def items(self):
      return {k: v for k, v in self.__dict__.items() if not k in Ar18.internals}.items()
  
    def parent(self):
      return self.__dict__[Ar18.internals[0]]
    
    def has(self, key):
      return key in self.dict()

    def index(self, idx):
      keys = list(self.__dict__)
      # Skip internal items, which should come before the actual items.
      return self.__dict__[keys[idx + len(Ar18.internals)]]
    
    def write(self, file_path:str):
      with open(file_path, "w") as file:
        file.write(str(self))
        
    def dict(self):
      return dict(filter(lambda elem: elem[0] not in Ar18.internals, self.__dict__.items()))
    
    def unique(self):
      import numpy as np
      ret = Ar18.Struct(self)
      for key, value in ret.items():
        if isinstance(value, list):
          temp = []
          for item in value:
            if not item in temp:
              temp.append(item)
              ret[key] = temp
        elif isinstance(value, Ar18.Struct):
          ret[key] = value.unique()
          
      return ret

def test():
  d = {"f":1,"g":{"h":7}}
  s = Ar18.Struct(d)
  assert s.f == 1
  assert s["f"] == 1
  assert s.g.h == 7
  assert s["g"]["h"] == 7
  shape = Ar18.Struct()
  assert not shape.shape.shape
  s.f = 2
  assert s.f == 2
  assert s["f"] == 2
  s["f"] = 3
  assert s.f == 3
  assert s["f"] == 3
  s.g.h = 8
  assert s.g.h == 8
  assert s["g"]["h"] == 8
  s["g"]["h"] = 9
  assert s.g.h == 9
  assert s["g"]["h"] == 9
  s.g["h"] = 10
  assert s.g.h == 10
  assert s["g"]["h"] == 10
  s["g"].h = 11
  assert s.g.h == 11
  assert s["g"]["h"] == 11
  s.k = 5
  assert s.k == 5
  s["k"] = 6
  assert s.k == 6
  s.d = {"j":"%"}
  assert s.d.j == "%"
  s["d1"] = {"j":"!"}
  assert s.d1.j == "!"
  t = s.d["non_existant_key"]
  assert not t
  s.key_present_in_parent = "mykey"
  t2 = s.d["key_present_in_parent"]
  assert t2 == "mykey"
  s["import"] = 55
  assert s["import"] == 55
  s.d1.foo = {
    "ha": "llo"
  }
  assert s.d1.foo.ha == "llo"
  hg = s.d1.foo.non_existant_key
  assert not hg
  t = s.h.j
  assert not t
  t = s["h"]["j"]
  assert not t
  assert len(s) == 7
  s["65"] = {"78": 90}
  assert len(s) == 8
  s["65"] = 66
  assert len(s) == 8
  del s["65"]
  assert len(s) == 7
  del s.f
  assert len(s) == 6
  s.array = [1,2]
  assert len(s.array) == 2

  print(s)
