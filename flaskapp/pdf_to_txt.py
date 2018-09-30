"""
Parse pdf files from pdf_files dir to text_files dir
"""

import os
import sys
import time
import shutil
import pickle

from utils import Config

# make sure pdftotext is installed
if not shutil.which('pdftotext'):
  print('ERROR: pdftotext not installed. Install it first before calling this script')
  sys.exit()

if not os.path.exists(Config.txt_dir):
  print('creating ', Config.txt_dir)
  os.makedirs(Config.txt_dir)

have = set(os.listdir(Config.txt_dir))
files = os.listdir(Config.pdf_dir)

for i,f in enumerate(files): # there was a ,start=1 here that I removed, can't remember why it would be there. shouldn't be, i think.

  txt_basename = f + '.txt'
  if txt_basename in have:
    print('%d/%d skipping %s, already exists.' % (i, len(files), txt_basename, ))
    continue

  pdf_path = os.path.join(Config.pdf_dir, f)
  txt_path = os.path.join(Config.txt_dir, txt_basename)
  cmd = "pdftotext %s %s" % (pdf_path, txt_path)
  os.system(cmd)

  print('%d/%d %s' % (i, len(files), cmd))

  # check output was made
  if not os.path.isfile(txt_path):
    # there was an error with converting the pdf
    print('there was a problem with parsing %s to text, creating an empty text file.' % (pdf_path, ))
    os.system('touch ' + txt_path) # create empty file, but it's a record of having tried to convert

  time.sleep(0.01) # ctrl+c termination

