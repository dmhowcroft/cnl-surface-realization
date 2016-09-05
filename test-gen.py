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


def inputsentence_analysis(inputsentence):
	post_data = "sentence="+inputsentence
        url=urllib2.urlopen("http://barbar.cs.lth.se:8081/parse",data=post_data)
        returncode = url.getcode()
        content = url.read()


        #if returncode != 200:
         #       print >> log,'NLP server error (problem processing)'

        print content
        content=content.split('\n')
        sent=[]
        result={}
        SemPar = 0
        NoSbj = 0
        #print "data is", repr(content)

        for row in content:
                table=row.split('\t')
                sent.append(table)


def demo():
        inputsentences = "Install the spacer between the two washers."
	inputsentence_analysis(inputsentences)

if __name__=="__main__":
        demo()

