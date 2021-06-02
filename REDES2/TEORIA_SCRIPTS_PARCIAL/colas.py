print("PROPIEDAD DE: RODRIGO JUEZ HERNÁNDEZ")
print("DISEÑADO PARA EL 3er PARCIAL DE REDES2")

ids = [0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19]
classes = [0,1,0,1,2,1,2,2,1,2,2,2,0,0,0,0,0,0,2,2]
tr = [6,8,12,16,18,22,28,30,31,36,41,47,51,52,54,56,62,63,68,69]



class FIFOqueue:
    actualtime = 0
    sumele = 0
    def __init__(self, ids, classes, tr, jumptime):
        self.totalength = len(ids)
        self.classesinput = classes
        self.classessum = {} 
        self.jumptime = jumptime
        self.list = sorted(zip(ids, tr, classes), key = lambda tup: tup[1])
        for i in set(classes):
            self.classessum[i] = 0



    def pop(self):
        element_to_return = (self.actualtime, None)
        if self.list[0][1] <= self.actualtime:
            element_to_return = self.list.pop(0)
            
            self.sumele += self.actualtime - element_to_return[1]
            self.classessum[element_to_return[2]] += self.actualtime - element_to_return[1]
            
            element_to_return = self.actualtime,  element_to_return[0]
        
        self.actualtime += self.jumptime
        return element_to_return

    def empty(self):
        return len(self.list) == 0

    def averages(self):
        averages = {}
        for key, suma in self.classessum.items():
            averages[key] = suma/len([i for i in self.classesinput if i == key])
        averages['total'] = self.sumele/self.totalength
        return averages 





class WFQqueue:
    
    sumele = 0
    actualtime = 0
    classindex = 0
    classes = {}
    classessum = {}
    #classorder should have the weights embeded in the order you want
    def __init__(self, ids, classes, tr, jumptime, classorder):
        self.listclassesinput = classes
        self.classorder = classorder
        self.totalength = len(ids)
        self.jumptime = jumptime
        
        
        for id, cla, tr in zip(ids, classes, tr):
            if self.classes.get(cla) == None:
                self.classes[cla] = []
                self.classessum[cla] = 0

            self.classes[cla].append((id, tr))

        for cla, li in self.classes.items():
            self.classes[cla] =  sorted(li, key = lambda tup: tup[1])

    def print(self):
        print(self.classes)

    def pop(self):
        element_to_return = (self.actualtime, None)

        for i in range(0, len(self.classorder)):
            classtopop = self.classorder[self.classindex]
            flag_pop = False

            #print(f"checking class {self.classorder[self.classindex]}: {self.classes[classtopop]}")
            if (not (len(self.classes[classtopop]) == 0)) and self.classes[classtopop][0][1] <= self.actualtime:
                element_to_return = self.classes[classtopop].pop(0)
                self.classessum[classtopop] += self.actualtime - element_to_return[1]
                self.sumele += self.actualtime - element_to_return[1]
                element_to_return = self.actualtime,  element_to_return[0]
                flag_pop = True


            self.classindex = (self.classindex+1)%len(self.classorder)
            if flag_pop == True:
                break

        self.actualtime += self.jumptime
        return element_to_return

    def empty(self):
        for key, classlist in self.classes.items():
            if not len(classlist) == 0:
                return False
        return True


    def averages(self):
        averages = {}
        for key, suma in self.classessum.items():
            averages[key] = suma/len([i for i in self.listclassesinput if i == key])
        averages['total'] = self.sumele/self.totalength
        return averages




if __name__ == "__main__":
    print("NO ESTA TESTEADO LO SUFICIENTE")
    sumele = 0
    FIFO = FIFOqueue(ids, classes, tr, 10)
    print("\n============= FIFO: =============")
    #print("exit\tid")
    str = ""
    while not FIFO.empty():
        element = FIFO.pop()
        #print(f"{element[0]}\t{element[1]}")
        if element[1] != None:
            str+=f"{element[1]}-"
    print(f"average {FIFO.averages()}")
    print(str[:-1])


    RR = WFQqueue(ids, classes, tr, 10, [0,1,2])
    print("\n============= RR: =============")
    #print("exit\tid")
    str = ""
    while not RR.empty():
        element = RR.pop()
        #print(f"{element[0]}\t{element[1]}")
        if element[1] != None:
            str+=f"{element[1]}-"
    print(f"average {RR.averages()}")
    print(str[:-1])

    WFQ = WFQqueue(ids, classes, tr, 10, [0,1,2,1,2,1])
    print("\n============= WFQ: =============")
    #print("exit\tid")
    str = ""
    while not WFQ.empty():
        element = WFQ.pop()
        #print(f"{element[0]}\t{element[1]}")
        if element[1] != None:
            str+=f"{element[1]}-"
    print(f"average {WFQ.averages()}")
    print(str[:-1])


    