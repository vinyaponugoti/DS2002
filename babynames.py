#!/usr/bin/python
# Copyright 2010 Google Inc.
# Licensed under the Apache License, Version 2.0
# http://www.apache.org/licenses/LICENSE-2.0

# Google's Python Class
# http://code.google.com/edu/languages/google-python-class/

import sys
import re

"""Baby Names exercise

Define the extract_names() function below and change main()
to call it.

For writing regex, it's nice to include a copy of the target
text for inspiration.

Here's what the html looks like in the baby.html files:
...
<h3 align="center">Popularity in 1990</h3>
....
<tr align="right"><td>1</td><td>Michael</td><td>Jessica</td>
<tr align="right"><td>2</td><td>Christopher</td><td>Ashley</td>
<tr align="right"><td>3</td><td>Matthew</td><td>Brittany</td>
...

Suggested milestones for incremental development:
 -Extract the year and print it
 -Extract the names and rank numbers and just print them
 -Get the names data into a dict and print it
 -Build the [year, 'name rank', ... ] list and print it
 -Fix main() to use the extract_names list
"""

def extract_names(filename):
  """
  Given a file name for baby.html, returns a list starting with the year string
  followed by the name-rank strings in alphabetical order.
  ['2006', 'Aaliyah 91', Aaron 57', 'Abagail 895', ' ...]
  """
  # +++your code here+++

  # list to return
  baby_names = []

  name_file = open(filename, 'r')
  babynames_file = name_file.read()

  year = re.search(r'Popularity\sin\s(\d\d\d\d)', babynames_file)
  
  if year:
    baby_names.append(year.group(1))

  tuples = re.findall(r'<td>(\d+)</td><td>(\w+)</td>\<td>(\w+)</td>', babynames_file)    
  
  to_sort = []
  all_names = {}
  girl_names = {}
  for t in tuples:
    all_names[t[1]] = t[0]
    to_sort.append(t[1])
    girl_names[t[2]] = t[0]
    to_sort.append(t[2])

  to_sort = set(to_sort)
  to_sort = sorted(to_sort)
  

  for name in girl_names:
    if name in all_names:
        if(all_names[name] < girl_names[name]):
          girl_names[name] = all_names[name]

  all_names.update(girl_names)

  for name in to_sort:
    baby_names.append(name + " " + all_names[name])

  # print(all_names)
  return baby_names


def main():
  # This command-line parsing code is provided.
  # Make a list of command line arguments, omitting the [0] element
  # which is the script itself.
  args = sys.argv[1:]

  if not args:
    print ('usage: [--summaryfile] file [file ...]')
    sys.exit(1)

  # Notice the summary flag and remove it from args if it is present.
  summary = False
  if args[0] == '--summaryfile':
    summary = True
    del args[0]

  # +++your code here+++
  # For each filename, get the names, then either print the text output
  # or write it to a summary file
  for filename in args:
    names = extract_names(filename)
    text = '\n'.join(names)

    if summary:
      outf = open(filename + '.summary', 'w')
      outf.write(text + '\n')
      outf.close()
    else:
      print (text)
if __name__ == '__main__':
  main()
