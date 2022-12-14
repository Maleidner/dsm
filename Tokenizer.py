# -*- coding: utf-8 -*-
"""
Created on Tue Oct 11 17:01:40 2022

@author: maren

"""

import sys, re, os
    
    
class Tokenizer: 
    

    source = ""
    tokenstream = []
    line = 1
    
    
    constants={
            "ASSIGN": ":=",
            "SEMICOLON": ";",
            "PLUS": "+",
            "MINUS": "-",
            "UMINUS": "-",
            "POWER": "**",
            "TIMES": "*",
            "DIVIDE": "/",
            "UNEQUAL": "!=",
            "EQUAL": "=",
            "LTOE": "<=",
            "GTOE": ">=",
            "LT": "<",
            "GT": ">",
            "LPAR": "(",
            "RPAR": ")",
            "LSPAR": "[",
            "RSPAR": "]",
            "LCPAR": "{",
            "RCPAR": "}",
            "AMPERSAND": "&",
            "COMMA": ",",
            "SEQTO": "..."
            }
            
            
    regexes = {
            "IDENTIFIER": r'[a-z]+',
            "TIMESTAMP": r'^(\d{4}-\d{2}-\d{2})T(\d{2}:\d{2}:\d{2})?',
            "STRTOKEN": r'"(.*?)"',
            "NUMTOKEN": r'\d+(\.\d+)?',
            "COMMENT": r'^/{2}.*'
            }
    
    
    reserved = ["NULL", "IF", "THEN",  "ELSE", "TRUE", "FALSE", "SQRT", "WRITE", "ELSEIF", "ENDIF", "FOR", "IN", "DO", "ENDDO", "AND", "OR", "NOT", "MAXIMUM", "MINIMUM", "FIRST",
    "LAST", "SUM", "COUNT", "IS", "WITHIN", "TO", "NOW", "TIME", "OF", "IS", "NUMBER", "LIST", "CURRENTTIME"]
    
    def __init__(self, name):
        with open(os.path.join(os.getcwd(), name), "r") as f:
            self.source = f.read()
            print(self.source)
        
        
    def tokenize(self):
        while len(self.source) > 0:
            if self.source.startswith(" "):
                self.source = self.source[1:]
                
            if self.source.startswith("\n"):
                self.source = self.source[1:]
                self.line += 1
                
            self.matchRegex()
            self.matchConst()
            
        return self.tokenstream
            
            
    def matchRegex(self):
        for key, value in self.regexes.items():
            result = re.match(value, self.source, re.I)
            if result:
                value = result.group()
                if value.upper() in self.reserved:
                    key = value.upper()
                self.source = self.source[len(value):]
                if key.upper() == "STRTOKEN":
                    value = value[1:-1]
                self.tokenstream.append([str(self.line), key, value])
           
    
    def matchConst(self):
        for key, value in self.constants.items():
            if self.source.startswith(value):
                self.tokenstream.append([str(self.line), key, value])
                self.source = self.source[len(value):]
               