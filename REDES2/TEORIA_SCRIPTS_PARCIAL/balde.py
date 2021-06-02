ids = [0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19]
tr = [21,23,24,27,36,37,38,39,40,41,42,45,50,51,56,57,58,61,92,96]
tamaños = [6,3,3,7,4,6,7,7,6,7,5,4,6,7,5,7,6,4,7,7]


class BALDEqueue:
    actualtime = 0
    jumptime = 1

    fichasbalde = 0
    def __init__(self, ids, tamaños, tr, tamañobuffer, segundosporficha):
        self.totalength = len(ids)
        self.classessum = {} 
        self.list = sorted(zip(ids, tr, tamaños), key = lambda tup: tup[1])
        self.segundosporficha = segundosporficha
        self.tamañobuffer = tamañobuffer
        

    def pop(self):
        element_to_return = (self.actualtime, None, None, None)
        if self.actualtime % self.segundosporficha == 0 and self.actualtime != 0:
            self.fichasbalde += 1
            element_to_return = (self.actualtime, None, self.fichasbalde)

        tamañoactualbuffer = len([i for i in self.list if self.actualtime >= i[1]]) 
        if tamañoactualbuffer > self.tamañobuffer:
            print(f"OVERFLOW DESCARTANDO {self.list.pop(tamañoactualbuffer-1)[0]}")


        if self.actualtime >= self.list[0][1] and self.fichasbalde > 0:
            element_to_return = self.list.pop(0)
            tamañopaquete = element_to_return[2]
            element_to_return = self.actualtime, element_to_return[0], self.fichasbalde-1

            self.fichasbalde -= 1

            for i in range(self.actualtime+1, self.actualtime+tamañopaquete):
                if i%self.segundosporficha == 0:
                    
                    self.fichasbalde += 1
                    break
    
            self.actualtime += tamañopaquete

        else:
            self.actualtime += self.jumptime

        return element_to_return
    
    def empty(self):
        return len(self.list) == 0

   



if __name__ == "__main__":
    str = ""
    balde = BALDEqueue(ids, tamaños, tr, tamañobuffer=10, segundosporficha= 10)
    print("============= BALDE: =============")
    #print("exit\tid\ttamaño")
    while not balde.empty():
        element = balde.pop()
        if element[1] != None:
            #print(f"{element[0]}\t{element[1]}\t{element[2]}")
            str += f"{element[1]}-{element[0]}:"
    



    print(str[:-1])

            