#!/usr/bin/env python
'''
krush - Apply templated Kubernetes manifests

Usage:
  krush [--vars=<file.vars>] [<path>]

Arguments:
  path                    Optional search path or file name

Options:
  --vars=<file.vars>      File with variables defined and assigned
  -h, --help              Show this message and exit.
'''

import os
import yaml
import urllib.parse
import hmac
import hashlib
import base64
from sys import argv
from jinja2 import FileSystemLoader, Environment, meta
from subprocess import Popen, PIPE
from docopt import docopt

class krush():
  __manifests = []
  __variables = []
  __path = ""
  __varfile = ""
  __vars = {}

  def __init__(self,path,varfile,vars):
    self.__path = path
    self.__varfile = varfile
    self.__vars = vars
    self.__env = Environment(loader=FileSystemLoader(searchpath=self.__path))
    self.__env.globals['hmac_sha256'] = self.hmac_sha256
    self.__env.globals['base64_encode'] = self.base64_encode
    self.__env.globals['url_escape'] = self.url_escape
    self.get_manifests()
    self.get_vars()
    self.prompt_undefined()
    self.apply()

  def hmac_sha256(self, key, msg):
    return hmac.HMAC(str(key).encode('utf-8'), str(msg).encode('utf-8'), hashlib.sha256).digest()

  def base64_encode(self, value):
    return base64.b64encode(value).decode('utf-8')

  def url_escape(self, url):
    return urllib.parse.quote_plus(str(url))

  def get_manifests(self):
    self.__manifests = []
    varfilepath = os.path.abspath(self.__varfile)
    if os.path.isdir(self.__path):
      searchdir = os.path.expanduser(os.path.expandvars(self.__path))
      for root, dirs, files in os.walk(searchdir, followlinks = True):
        for name in files:
          filename = os.path.abspath(os.path.join(root,name))
          if (filename.endswith('.yaml') or filename.endswith('.yml')) and filename != varfilepath:
            self.__manifests.append(filename)

    elif os.path.isfile(self.__path) and (self.__path.endswith('.yaml') or self.__path.endswith('.yml')) and self.__path != varfilepath:
      self.__manifests.append(self.__path)

    if not len(self.__manifests) > 0:
      print("Unable to find manifests")
      print("Please run: krush --help")
      exit(1)

  def get_vars(self):
    self.__variables = []
    tempvars = []
    for i in self.__manifests:
      src = self.__env.loader.get_source(self.__env, os.path.relpath(i, self.__path))[0]
      parsed = self.__env.parse(source=src)
      tempvars += list(meta.find_undeclared_variables(ast=parsed))
    for i in tempvars:
      if i not in self.__variables and i not in self.__env.globals.keys():
        self.__variables.append(i)
    self.__variables.sort()

  def prompt_undefined(self):
    for i in self.__variables:
      if i not in self.__vars.keys():
        v = input("Enter value for %s: " % i)
        self.__vars[i] = v

  def apply(self):
    cmd = "kubectl apply -f -".split()
    for i in self.__manifests:
      template = self.__env.get_template(os.path.relpath(i, self.__path))
      rendered = template.render(self.__vars)
      p = Popen(cmd, stdin=PIPE)
      p.communicate(input=rendered.encode('utf-8'))

def main():
  varfile = ""
  args = docopt(__doc__)
  if args['--vars']:
    varfile = os.path.abspath(args['--vars'])
  if not args['<path>']:
    p = "."
  else:
    p = args['<path>']
  path = os.path.abspath(p)
  if varfile:
    with open(varfile, 'r') as f:
      vars = yaml.load(f)
  else:
    vars = {}

  k = krush(path,varfile,vars)

if __name__ == "__main__":
    main()
