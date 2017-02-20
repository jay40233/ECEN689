import sys
import getopt
import os
import math
import operator
class NW:
  def __init__(self):
    self.table = [[]]
    self.str1 = ""
    self.str2 = ""
    self.backtrace = []
    self.buff = []
    self.check_point = []
    self.check_count = []
  #initial the score table  
  def initial_table(self,a,b):
    self.table = [[0]*(len(b)+1) for _ in range(len(a)+1)]
    for j in range(0,len(b)+1):
      self.table[0][j] = j*(-1)
    for i in range(0,len(a)+1):
      self.table[i][0] = i*(-1)
    self.str1 = a
    self.str2 = b
    self.buff = [[len(a),len(b)]]
  #apply the scoring method
  def check_match(self,a,b):
    if a==b:
      return 1
    return -1

  def Needleman(self,i,j):
    if j ==0 or i ==0:
      return self.table[i][j]
    else:
      self.table[i][j] = max(self.Needleman(i,j-1)-1,self.Needleman(i-1,j)-1,self.Needleman(i-1,j-1)+self.check_match(self.str1[i-1],self.str2[j-1]))
    return self.table[i][j]

  def TraceBack(self,i,j):
    if i==0 and j==0:
      buff_copy = self.buff[:]
      self.backtrace.append(buff_copy)
      if self.check_point:
        #print("Check point last item:" , self.check_point[-1])
        #print("Check point count:",self.check_count)
        temp = self.check_point[-1]
        self.check_count[-1] -= 1
        if self.check_count[-1] == 0:
          del self.check_point[-1]
          del self.check_count[-1]
        self.buff = temp[:]
      #print(self.backtrace)
      return 0
    elif i ==0:
      self.buff.append([i,j-1])
      self.TraceBack(i,j-1)
    elif j ==0:
      self.buff.append([i-1,j])
      self.TraceBack(i-1,j)
    else:
      if ((self.table[i-1][j]-1 == self.table[i][j]) + (self.table[i][j-1]-1 == self.table[i][j]) +(self.table[i-1][j-1]-1 == self.table[i][j] or self.table[i-1][j-1]+1 == self.table[i][j]))>=2:
        count = ((self.table[i-1][j]-1 == self.table[i][j]) + (self.table[i][j-1]-1 == self.table[i][j]) +(self.table[i-1][j-1]-1 == self.table[i][j] or self.table[i-1][j-1]+1 == self.table[i][j]))
        temp = self.buff[:]
        self.check_point.append(temp)
        self.check_count.append(count-1)
        #print("Check point:", self.check_point)
      if self.table[i-1][j]-1 == self.table[i][j]:
        self.buff.append([i-1,j])
        self.TraceBack(i-1,j)  
      if self.table[i][j-1]-1 == self.table[i][j]:
        self.buff.append([i,j-1])
        self.TraceBack(i,j-1)
      if self.table[i-1][j-1]-1 == self.table[i][j] or self.table[i-1][j-1]+1 == self.table[i][j]:
        self.buff.append([i-1,j-1])
        self.TraceBack(i-1,j-1)

def printAlignments(traces,a,b):
  output = []
  for trace in traces:
    print("=======================")
    print("The Alignment:")
    output_A = ""
    output_B = ""
    trace_t = trace[::-1]
    for i in range(1,len(trace_t)):
      if trace_t[i][0]-trace_t[i-1][0] !=0:
        output_A += a[trace_t[i][0]-1]
      else:
        output_A += "_"
      if trace_t[i][1]-trace_t[i-1][1] !=0:
        output_B += b[trace_t[i][1]-1]
      else:
        output_B += "_"
    output.append([output_A, output_B])
    print(output_A)
    print("|"*len(output_A))
    print(output_B)
    print("Alignment length = ",len(output_A))
  print("=======================")
  return output

def main():
  (options, args) = getopt.getopt(sys.argv[1:], 'fbm')
  if not len(args[0]) or not len(args[1]):
    print("===================================================|")
    print("Please give two sequences with at least length 1 !!|")
    print("===================================================|")
    return 0
  alignment = NW()
  alignment.initial_table(args[0],args[1])
  alignment.Needleman(len(args[0]),len(args[1]))
  alignment.TraceBack(len(args[0]),len(args[1]))
  #print(alignment.backtrace)
  #alignments = printAlignments(alignment.backtrace,args[0],args[1])
  print("The alignment score is ",alignment.table[len(args[0])][len(args[1])])

  return 0

if __name__ == "__main__":
    main()