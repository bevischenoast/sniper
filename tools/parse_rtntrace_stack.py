#!/usr/bin/env python

import sys, os, collections, subprocess, sniper_lib, sniper_config

def ex_ret(cmd):
  return subprocess.Popen(cmd, stdout = subprocess.PIPE).communicate()[0]
def cppfilt(name):
  return ex_ret([ 'c++filt', name ])

if len(sys.argv) > 1:
  resultsdir = sys.argv[1]
else:
  resultsdir = '.'

filename = os.path.join(resultsdir, 'sim.rtntracefull')
if not os.path.exists(filename):
  print >> sys.stderr, 'Cannot find trace file', filename
  sys.exit(1)

config = sniper_lib.get_config(resultsdir = resultsdir)
freq = 1e9 * float(sniper_config.get_config(config, 'perf_model/core/frequency'))
fs_to_cycles_cores = freq / 1e15


functions = {}
calls = {}
children = collections.defaultdict(set)
roots = set()
totals = {}


class Function:
  def __init__(self, eip, name, location):
    self.eip = eip
    self.name = cppfilt(name).strip()
    self.location = location
  def __str__(self):
    return self.name
    #return '[%8s] %s' % (self.eip, self.name)

class Call:
  def __init__(self, stack, data):
    self.stack = stack
    self.data = data
  def buildTotal(self):
    # Add self to global total
    for k in self.data:
      totals[k] = totals.get(k, 0) + self.data[k]
	# Calculate children's totals
    for stack in children[self.stack]:
      calls[stack].buildTotal()
    # Add all children to our total
    self.total = dict(self.data)
    for stack in children[self.stack]:
      for k in calls[stack].total:
        self.total[k] += calls[stack].total[k]
  def printLine(self):
    print '%7d\t' % self.data['calls'] + \
          '%6.2f%%\t' % (100 * self.total['core_elapsed_time'] / float(totals['core_elapsed_time'])) + \
          '%6.2f%%\t' % (100 * self.data['core_elapsed_time'] / float(totals['core_elapsed_time'])) + \
          '%6.2f%%\t' % (100 * self.total['instruction_count'] / float(totals['instruction_count'])) + \
          '%7.2f\t' % (self.total['instruction_count'] / (fs_to_cycles_cores * float(totals['core_elapsed_time']))) + \
          '%7.2f\t' % (1000 * self.total['l2miss'] / float(self.total['instruction_count'])) + \
          '  '*len(self.stack.split(':')) + str(functions[self.stack.split(':')[-1]])
  def printTree(self):
    self.printLine()
    for stack in sorted(children[self.stack], key = lambda stack: calls[stack].total['core_elapsed_time'], reverse = True):
      if calls[stack].total['core_elapsed_time'] / float(totals['core_elapsed_time']) < .001:
        break
      calls[stack].printTree()


fp = open(filename)
headers = fp.readline().strip().split('\t')

for line in fp:
  if line.startswith(':'):
    eip, name, location = line.strip().split('\t')
    eip = eip[1:]
    functions[eip] = Function(eip, name, location)
  else:
    line = line.strip().split('\t')
    stack = line[0]
    data = dict(zip(headers[1:], map(long, line[1:])))
    calls[stack] = Call(stack, data)
    parent = stack.rpartition(':')[0]
    children[parent].add(stack)

roots = set(calls.keys())
for parent in calls:
  for child in children[parent]:
    roots.remove(child)

for stack in roots:
  calls[stack].buildTotal()

print '%7s\t%7s\t%7s\t%7s\t%7s\t%7s  %s' % ('calls', 'time', 't.self', 'icount', 'ipc', 'l2.mpki', 'name')
for stack in sorted(roots, key = lambda stack: calls[stack].total['core_elapsed_time'], reverse = True):
  calls[stack].printTree()