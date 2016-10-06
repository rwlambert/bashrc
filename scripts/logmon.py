#!/usr/bin/env python

import time
import string
import os
import sys

class tail:
	def __init__(self, filename, callback, tailbytes = 0):
		'''Create a new tail instance.
		Create a tail object which periodicly polls the specified file looking
		for new data which was written.  The callback routine is called for each
		new line found in the file.

		@return Nothing
		@param filename File to read.
		@param callback Function which takes one argument, called with each
				line read from the file.
		@param tailbytes Specifies bytes from end of file to start reading
				(defaults to 0, meaning skip entire file, -1 means read full file).
		'''
		self.skip = tailbytes
		self.filename = filename
		self.callback = callback
		self.fp = None
		self.lastSize = 0
		self.lastInode = -1
		self.data = ''

	def process(self):
		'''Examine file looking for new lines.
		When called, this function will process all lines in the file being
		tailed, detect the original file being renamed or reopened, etc...
		This should be called periodicly to look for activity on the file.

		@return Nothing
		'''
		#  open file if it's not already open
		if not self.fp:
			try:
				self.fp = open(self.filename, 'r')
				stat = os.stat(self.filename)
				self.lastIno = stat[1]
				if self.skip >= 0 and stat[6] > self.skip:
					self.fp.seek(0 - (self.skip), 2)
				self.skip = -1
				self.lastSize = 0
			except:
				if self.fp: self.fp.close()
				self.skip = -1    #  if the file doesn't exist, we don't skip
				self.fp = None
		if not self.fp: return

		#  check to see if file has moved under us
		try:
			stat = os.stat(self.filename)
			thisSize = stat[6]
			thisIno = stat[1]
			if thisSize < self.lastSize or thisIno != self.lastIno:
				raise Exception
		except:
			self.fp.close()
			self.fp = None
			self.data = ''
			return

		#  read if size has changed
		if self.lastSize < thisSize:
			while 1:
				thisData = self.fp.read(4096)
				if len(thisData) < 1:
					break
				self.data = self.data + thisData

				#  process lines within the data
				while 1:
					pos = string.find(self.data, '\n')
					if pos < 0: break
					line = self.data[:pos]
					self.data = self.data[pos + 1:]
					#  line is line read from file
					if self.callback: self.callback(line)

		self.lastSize = thisSize
		self.lastIno = thisIno

	def mainloop(self, sleepfor = 1):
		'''Loop forever processing activity on the tail object.
		This routine is intended to be called in programs which do not need
		to do other processing.  This routine never returns.

		@return Never returns
		@param sleepfor Seconds between processing (default is 5 seconds).
		'''
		while 1:
			self.process()
			time.sleep(sleepfor)


lastpattern=''
import re
def reppattern(line):
  #print "in:", line
  line=re.sub(r'\d','#',line)
  while '##' in line:
    line=line.replace('##','#')
  #print "out:", line
  return line


linewidth=120
if len(sys.argv)>2:
  linewidth=sys.argv[2]

def inteliresize(line,length):
    if len(line)<length:
       return line
    # "find distance between first and last number, if it's small enough, print back from last number"
    first=None
    last=None
    alln=[]
    for char in range(len(line)): 
       if line[char] in "0123456789":
         if first is None:
           first=char
         last=char
	 alln.append(char)
    if first is None or last<length:
      return line[:length]
    if last-first<length:
      return line[last-length:last]
    line=line[first:last]
    # if this is still too long, I need to replace parts of it, I will replace parts where the number of characters in a string with no numbers is >= than 6 with a '...'
    replacestr=[]
    for i in range(len(alln)-1):
      if alln[i+1]-alln[i]>5:
        replacestr.append(line[alln[i]:alln[i+1]])
    for repl in replacestr:
      line=line.replace(repl,'...')
      if len(line)<length:
        return line
    #finally, if this still doesn't work, return just the width specified
    return line[:length]

lastlen=0

def callback(line):
    global lastpattern
    global lastlen
    line=line.rstrip().lstrip()
    prline=inteliresize(line,linewidth)
    if len(lastpattern) and lastpattern==reppattern(line):
        sys.stdout.write('\r'+' '*lastlen)
        sys.stdout.write('\r'+prline)
        #print "matched",
    else:
        #print "no match", 
        sys.stdout.write('\n'+prline)
    lastlen=len(prline)
    lastpattern=reppattern(line)
    sys.stdout.flush()
        

if len(sys.argv)<2 or "--help" in sys.argv or "-h" in sys.argv:
  print "usage, logmon.py filename [max linewidth, default 120] [update frequency in seconds, default 1]"
  print " will poll a file to see if there are any moee lines added, and print them, but will pring on the same line if the only difference is some nubmer, so that you can turn some random printout into a sort of progress bar "
  print "use max linewidth to prevent line-wrapping which causes carriage return to fail"

sleepfor=1
if len(sys.argv)>3:
  sleepfor=sys.argv[3]

tail(sys.argv[1], callback).mainloop()
print
print "Yeeeeah"
