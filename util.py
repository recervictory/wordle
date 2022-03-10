import random
import re
import string
import pandas as pd

class Wordle(object):

    def __init__(self):
        self._answers = self.readfiles('2315_possible_answers.txt')
        self._allowed = self.readfiles('12972_allowed_words.txt')

    #----   Reading Files -------

    def readfiles(self, file):
        with open(file,'r') as fh:
            lines = fh.readlines()
        return [line.rstrip('\n') for line in lines]

    #----- Green Gray or Yellow
    def isMatched(self,text, pattern):
        if re.search(pattern, text):
            return True
        return False
    
    def gray(self, grayset, allowed = None):
        if allowed is None:
            allowed = self._passed

        if grayset == "":
            return allowed
        
        pattern = re.compile('[{0}]'.format(grayset))
        passed_ = []
        for word in allowed:
            if not self.isMatched(word, pattern):
                passed_.append(word)
        
        return passed_


    def green(self,greenList,allowed):
        passed_ = []       
        if greenList == []:
            return allowed
        else:
            char , position = greenList[0]
            for word in allowed:
                if word[position] == char:
                    passed_.append(word)
            return self.green(greenList[1:],passed_)
    
    def notGreen(self,greenList,allowed):
        passed_ = []       
        if greenList == []:
            return allowed
        else:
            char , position = greenList[0]
            for word in allowed:
                if word[position] != char:
                    passed_.append(word)
            return self.notGreen(greenList[1:],passed_)

    def yellow(self, yellowset,yellowList,allowed = None):
        if allowed is None:
            allowed = self._passed

        if yellowset == "":
            return allowed
        
        pattern = re.compile('[{0}]'.format(yellowset))
        passed_ = []
        for word in allowed:
            if self.isMatched(word, pattern):
                passed_.append(word)
        
        passed_ = self.notGreen(yellowList,passed_)
        return passed_

    def compareWord(self,guess,word, tup = True):
        gray_ = ""
        yellow_ = ""
        yellowList_ = set()
        greenList_ = set()
        
        for i in range(0,5):
            if guess[i] == word[i]:
                greenList_.add((guess[i],i))
            else:
                if guess[i] in word:
                    if guess[i] not in yellow_:
                        yellow_ += guess[i]
                    yellowList_.add((guess[i],i))
                if guess[i] not in word and guess[i] not in gray_:
                    gray_ += guess[i]
        
        if tup:
            return (gray_, tuple(yellowList_), tuple(greenList_))
        else:
            return {    "gray"      : gray_ ,
                    "yellow"    : yellow_,
                    "yellowList" : yellowList_,
                    "greenList" : greenList_ }

    

        
