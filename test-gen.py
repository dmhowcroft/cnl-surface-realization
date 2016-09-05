#/usr/bin/python
import sys
import re
from nltk.corpus import wordnet as wn
import time
import nltk.data

import json
import urllib2
from pprint import pprint
import xml.etree.ElementTree as ET

#import nltk.parse.dependencygraph
from nltk.parse import DependencyGraph


def inputsentence_analysis(inputsentence):
	post_data = "sentence="+inputsentence
        url=urllib2.urlopen("http://barbar.cs.lth.se:8081/parse",data=post_data)
        returncode = url.getcode()
        content = url.read()


        #if returncode != 200:
         #       print >> log,'NLP server error (problem processing)'

        #print content
	#print type(content)



        content=content.split('\n')
        sent=""
        #result={}
        #SemPar = 0
        #NoSbj = 0
        #print "data is", repr(content)
	#print content	

        for row in content:
                table=row.split('\t')
                #sent.append([table[0], table[1], table[2], table[4],  table[5], table[6], table[8], table[10], table[12], table[13], "\n"])
                sent+=table[0]+"\t"+table[1]+"\t"+table[2]+"\t"+table[4]+"\t"+table[5]+"\t"+table[6]+"\t"+table[8]+"\t"+table[10]+"\t"+table[12]+"\t"+table[13]+"\n"
		#sent+=table[0]+"\t"+table[1]+"\n"
	print sent
	dg = DependencyGraph(sent)
	tree = dg.tree()
	print tree.pprint()
	#print(dg)
	print(dg.to_conll(4))

def demo():
        inputsentences = "Install the spacer between the two washers."
	inputsentence_analysis(inputsentences)

if __name__=="__main__":
        demo()

