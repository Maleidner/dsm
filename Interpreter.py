import sys
from Datatypes import *
import operators
import copy
import numpy as np

symbol_table = {};

class Interpreter:
    
    def __init__(self):
        self.now = TimeType(value = datetime.now())

    def runOperator(self, fct, arg, handling, unary = False):
        evalArgs = [];

        if handling == "NO":
            for a in arg:
                evalArgs.append(self.ev(a))
            return self.callOperator(fct, evalArgs)

        elif handling == "DEF":
            argsAreLists = False
            listLengths = []


            if unary == True:
                for a in arg:
                    ea = self.ev(a)
                    if isinstance(ea, ListType):
                        return self.callOperator(fct, [ea])
                    else:
                        return self.callOperator(fct, [ea])


            if fct == "_iswithin":
                i = 1
                for a in arg:
                    ea = self.ev(a)
                    if i == 2 and isinstance(ea, ListType):
                        if ea.value[0].value < ea.value[1].value:
                            evalArgs.append(ea.value[0].value)
                        else:
                            evalArgs.append(ea.value[1].value)
                    elif i == 3 and isinstance(ea, ListType):
                        if ea.value[0].value < ea.value[1].value:
                            evalArgs.append(ea.value[1].value)
                        else:
                            evalArgs.append(ea.value[0].value)
                    else:
                        evalArgs.append(ea.value)
                    i = i+1
                
                return self.callOperator(fct, evalArgs)
                
            for a in arg:
                ea = self.ev(a)
                if(a["type"] == "VARIABLE" and isinstance(ea, NumType)):
                        evalArgs.append(symbol_table[a.get("name")])

                elif(a["type"] == "VARIABLE"):
                    if(isinstance(a[1], ListType)):
                        argsAreLists = True
                        li = ListType()
                        length = len(a[1].value)
                        listLengths.append(length)
                        for i in range(length):
                            li.value.append(a[1].value[i])
                        evalArgs.append(li)

              #  elif(a["type"] == "NUMBER"):
                #    li = []
                 #   for i in range(length):
                  #      li.append(NumType(a["value"]).value)
                   # evalArgs.append(li)
                   # evalArgs.append([li])

                elif isinstance(ea, ListType):
                    argsAreLists = True
                    listLengths.append(len(ea.value))
                    evalArgs.append(ea)
                elif(type(ea) == list):
                    argsAreLists = True
                    listLengths.append(len(ea))
                    evalArgs.append(ea)
                else:
                    evalArgs.append(ea)

            if not argsAreLists:
                return self.callOperator(fct, evalArgs)

            else:
                sameLength = True
                refLength = listLengths[0]
                for l in listLengths:
                    if l != refLength:
                        sameLength = False

                if not sameLength:
                    return NullType()

              #  modifiedArgs = [evalArgs[0]] * refLength
                modifiedArgs = []
                for e in evalArgs:
                    #if type(e) == float or type(e) == int:
                   #     modifiedArgs.append([e] * refLength)
                    if type(e) == float or type(e) == int or type(e) == NumType:
                        modifiedArgs.append([e] * refLength)
                    elif type(e) == list:
                        e = list(e)
                        tmp = []
                        for i in range(len(e)): 
                            tmp.append(e[i])
                        modifiedArgs.append(tmp)
                    elif type(e) == ListType:
                        tmp = []
                        for i in range(len(e.value)): 
                            tmp.append(e.value[i])
                        modifiedArgs.append(tmp)

                
                result = ListType()

                for i in range(refLength):
                    callArgs = []
                    for m in modifiedArgs:
                        callArgs.append(m)
                    temp = [callArgs[0][i], callArgs[1][i]]
                    if type(temp[0]) == NumType:
                        result.value.append(self.callOperator(fct, [temp[0], temp[1]]))
                    elif type(temp[1]) == NumType:
                        result.value.append(self.callOperator(fct, [temp[0], temp[1]]))
                    else:
                        result.value.append(self.callOperator(fct, temp))

                return result

    def callOperator(self, fct, earg):
        if len(earg) == 1:
            return getattr(operators, fct)(earg[0])
        elif len(earg) == 2:
            return getattr(operators, fct)(earg[0], earg[1])
        elif len(earg) == 3:
             return getattr(operators, fct)(earg[0], earg[1], earg[2])

    # Evaluiert einen Knoten im AST
    def ev(self, node):
        if node["type"] == "STATEMENTBLOCK":
            for s in node["statements"]:
                self.ev(s)
                
        elif node["type"] == "WRITE":
            print (self.ev(node["arg"])) 
 
        elif node["type"] == "STRTOKEN":
            return StrType (node["value"])

        elif node["type"] == "NUMBER":
            return NumType (node["value"])

        elif node["type"] == "TRUE":
            return BoolType (node["value"])

        elif node["type"] == "FALSE":
            return BoolType (node["value"])

        elif node["type"] == "NULL":
            return BoolType (node["type"])
        
       

        elif node["type"] == "AND":
            res = self.ev(node["arg"][0])
            for element in node['arg'][1:]:
                r = res and self.ev(element)
            return BoolType (r)

        elif node["type"] == "OR":
            res = self.ev(node["arg"][0])
            for element in node['arg'][1:]:
                r = res or self.ev(element)
            return BoolType (r)


        elif node["type"] == "NOT":
            res = self.ev(node["arg"][0])
            r = not eval(res.value)
            return BoolType (r)

        #elif node["type"] == "LIST":
         #   return ListType (node["args"])
        elif node["type"] == "LIST":
            list_ = ListType()
            for element in node['args']:
                val = self.ev(element)
                list_.value += [val]
            return list_


        elif node["type"] == "NOW":
            return self.now

        elif node["type"] == "TIMESTAMP":
            return TimeType(datetime.strptime(node.get("value"),"%Y-%m-%dT%H:%M:%S"))

        elif node["type"] == "CURRENTTIME":
            return TimeType(value = datetime.now())

        elif node["type"] == "POWER":
            return self.runOperator("_power", node["arg"], "DEF")
 

        elif node["type"] == "PLUS":
            return self.runOperator("_plus", node["arg"], "DEF")
          
        elif node["type"] == "MAXIMUM":
            return self.runOperator("_maximum", node["arg"], "DEF", True)

        elif node["type"] == "MINIMUM":
            return self.runOperator("_minimum", node["arg"], "DEF", True)

        elif node["type"] == "FIRST":
            return self.runOperator("_first", node["arg"], "DEF", True)

        elif node["type"] == "LAST":
            return self.runOperator("_last", node["arg"], "DEF", True)
        
        elif node["type"] == "SUM":
            return self.runOperator("_sum", node["arg"], "DEF", True)

        elif node["type"] == "COUNT":
            return self.runOperator("_count", node["arg"], "DEF", True)

        elif node["type"] == "TIMEOF":
            val = self.ev(node["arg"])
            if type(val) == ListType:
                timestamp_list = ListType()
                for i in val.value:
                    timestamp_list.value += [TimeType(i.timestamp)]
                return timestamp_list
            else:
                return TimeType(value=val.timestamp)

        elif node["type"] == "TIMEASSIGNMENT":
            ts = self.ev(node["arg"])
          #  if (not isinstance(ts, TimeType)):
           #     raise "TIMEASSIGNMENT"
            symbol_table[node.get("varname")].timestamp = ts.value


        elif node['type'] == 'TIMES':
            return self.runOperator("_times", node["arg"], "DEF")


        elif node["type"] == "MINUS":
            return self.runOperator("_minus", node["arg"], "DEF")

        elif node["type"] == "UMINUS":
            return self.runOperator("_uminus", node["arg"], "DEF")


        elif node["type"] == "DIVIDE":
            return self.runOperator("_divide", node["arg"], "DEF")


        elif node["type"] == "ASSIGN":
            symbol_table[node.get("varname")] = copy.deepcopy(self.ev(node.get("arg")))

        elif node["type"] == "VARIABLE":
            return symbol_table.get(node.get("name"), NullType)

        elif node["type"] == "LT":
            return self.runOperator("_lessthan", node["arg"], "DEF")
        
        elif node["type"] == "GT":
            return self.runOperator("_greaterthan", node["arg"], "DEF")
        
        elif node["type"] == "LTOE":
            return self.runOperator("_lessthanorequal", node["arg"], "DEF")

        elif node["type"] == "GTOE":
            return self.runOperator("_greaterthanorequal", node["arg"], "DEF")

        elif node["type"] == "EQUAL":
            return self.runOperator("_equal", node["arg"], "DEF")

        elif node["type"] == "ISWITHIN":
            return self.runOperator("_iswithin", node["arg"], "DEF")

        elif node["type"] == "FOR":
            indices = ListType()
            val = self.ev(node["expression"])
            for i in val.value:
                indices.value += [i]
            node["statements"]["statements"][0]["arg"]["arg"][0][1] = indices
            node["statements"]["statements"][0]["for"] = True
            self.ev(node["statements"]["statements"][0])
        elif node["type"] == "SEQTO":
            return self.runOperator("_seqto", node["arg"], "DEF")
            
        elif node["type"] == "ISNUMBER":
            res = self.ev(node["arg"][0])
            length = len(res.value)
            bools = []
            for i in range(length):
                bools.append(isinstance(res.value[i], NumType))
            return BoolType (bools)

        elif node["type"] == "ISLIST":
            res = self.ev(node["arg"][0])
            return BoolType (isinstance(res, ListType))

        elif node["type"] == "IF":
            if self.ev(node["condition"]).value:
                return self.ev(node["thenbranch"])
            else:
                return self.ev(node["elsebranch"])