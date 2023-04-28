from queue import PriorityQueue

## Holds Sudoku board data and provides functions for iteratoring over indexes
class Sudoku:

    ## Initializes gamedata with either a file or a string of gamedata
    def __init__(self, file):
        if type(file) == type(''):
            ##f = open(file)
            self.gamedata = file
        else:
            self.gamedata = file.read()
            ##print(self.gamedata)
        self.gamedata = self.gamedata.translate({ord(i): None for i in ' \n'}) 
        self.size = 9
        ##print(self.gamedata)

    ## Returns a function to iterate over values in the same row as i
    def rowIter(self, i):
        row = i // self.size
        return lambda j : self.__rowIter__(row, j)
    
 
    ## Returns a function to iterate over values in the same col as i
    def colIter(self, i):
        col = i % (self.size)
        return lambda j : self.__colIter__(col, j)

    ## Returns a function to iterate over values in the same cell as i
    def cellIter(self, i):
        col = i % (self.size)
        row = i // self.size
        cell = 3 * self.__cellRow__(row) + self.__cellCol__(col)

       ## print("cell: " + str(cell))
        return lambda j : self.__cellIter__(row, col, cell, j)
    
    def solved(self):
        print("In Solved")
        row = '123456789'
        col = '123456789'
        cell = '123456789'
        
        for i in range(0, 9):
            rowIter = self.rowIter(i)
            colIter = self.colIter(i)
            cellIter = self.cellIter(i)
            for j in range(0, 9):
                row = row.replace(self.gamedata[rowIter(j)], '')
                print(row)
                col = col.replace(self.gamedata[colIter(j)], '')
                print(col)
                cell = cell.replace(self.gamedata[cellIter(j)], '')
                print(cell)
            if row != '' and col != '' and cell != '':
                return False
            row = '123456789'  
            col = '123456789'
            cell ='123456789'
        print("Here Solved")
        return True
        
        return True
    def __cellIter__(self, row, col, cell, i):
        cellRow = self.__cellRow__(row)
        if cellRow == 0:
            start_i = 0
        elif cellRow == 1:
            start_i = 27
        elif cellRow == 2:
            start_i = 54
        return (((i // 3) * 9 + (i % 3) ) + start_i) + (3 * self.__cellCol__(col))
    
    def __cellCol__(self, col):
        return col // 3

    def __cellRow__(self, row):
        
       return row // 3
   
    def __colIter__(self, col, i):
        return (i * self.size) + col

    def __rowIter__(self, row, i):
        last = (row + 1) * self.size - 1
        ##print("LAST: " + str(last))
        if i >= self.size:
            i = row * self.size
        return i + (row * self.size)

    
    def __repr__(self):
        s = ''
        for i in range(0, len(self.gamedata)):
            s += self.gamedata[i] + ' '
            if (i + 1) % self.size == 0:
                s += '\n'
               ## print("TESTING:")
       ## for i in s:
            ##print(i)
        return s

## Object for solving Sudoku Objects
class SudokuSolver:

    ## Initializes Variables, Domains, Constraints, Availability list
    def __init__(self, s):
        self.sod = s
        self.X = self.sod.gamedata
        self.D = self.__initDomain__()
        self.C = self.__initCons__()
        self.A = self.__initAvailList__()
        self.solved = False
        if not self.A:
            ##print("Unsolvable")
            return None
        


    
        
        
        
    def solvable(self, S):
        sol = SudokuSolver(S)
        return sol.A

    ## prints solution
    def solve(self):
        ##print(self.X)
        ##print("Here")
        S = self.__search__(self.X)
      ##  print(self.X)
      ##  print(self.A)
        print(S)
        ##print(S.gamedata)
        return S

    ## Returns goal state as a Sudoku object
    def __search__(self, X):
        i = len(self.A)-1
      ##  print(i)
        node = self.A[i]
        found = False
        ##self.expand(node, i, found)
        q = self.__initPQ__()
        node = q.get()
        self.fastExpand(node, q)
      ##  print("After")
      ##  print(self.X)
        return Sudoku(self.X)
        
        
    def setString_i(self, i, s, c):
        return s[:i] + c + s[i + 1:]

    ## searches for goal state using most constraining variable as heuristic
    def fastExpand(self, node, q):
        node = q.get()
        ##print(node)
        cons = node[1]
        i = cons[0]
        ##print(cons)

        ##self.printQ(q)
        sol = SudokuSolver(Sudoku(self.X))
        if q.empty() or self.solved:
            self.X = self.setString_i(i, self.X, cons[1])
            self.solved = True
            return

        for j in cons[1]:
            newX = self.setString_i(i , sol.X, j)
            sol = SudokuSolver(Sudoku(newX))
            ##print(self.X)
            ##print(newX)
            ##print(sol.sod)

            if sol.A:
                newNode = q.get()
                sol.fastExpand(newNode, sol.__initPQ__())
                if sol.solved:
                    self.solved = True
                    self.X = sol.X
                    return
            
        
    ## recursively searches for goal state
    def expand(self, node, i, found):
        sol = SudokuSolver(Sudoku(self.X))
        if i == -1 or self.solved:
            self.solved = True
        ##    print("Returning")
        ##    print(self.X)
            p = self.X
            return 
        for j in node:
            newX = self.setString_i(i, sol.X, j)
            ##print(self.X)
            ##print(newX)
            sol = SudokuSolver(Sudoku(newX))
            ##print(sol.sod)
            if sol.A:
                ##print("solvable")
                newNode = sol.A[i-1]
                ##print(sol.A)
                sol.expand(newNode, i-1, found)
         ##       print("Returned")
         ##       print(sol.solved)
                if sol.solved:
                    self.solved = True
                    self.X = sol.X
         ##           print("Returning:")
         ##           print(sol.X)
                    return 
            
            ##if newNode:
       ## if sol.solved:
       ##     print("Bottom")
       ##     sol = SudokuSolver(Sudoku(self.X))
            
            
    def test(self, l):
        l.pop()
        print(l)
            
        
                
                ##self.__search__(sol) 
      ##  while not q.empty():
      ##      cons = q.get()[1]
      ##      list.append(cons)
      ##      print("list: ")
      ##      print(list)
      ##  for l in list:
      ##      print(l)
      ##      
      ##      for c in l[1]:
      ##          
      ##          X = X[:l[0]] + c + X[l[0] + 1:]
      ##          ##print(self.X)
      ##          S = Sudoku(X)
      ##          print(S)
      ##          sol = SudokuSolver(S)
      ##          if sol.A:
      ##              newQueue = sol.__initPQ__()
      ##              self.printQ(newQueue)
      ##          print(S)
      ##      if not sol.A:
      ##          print("Returning: ")
      ##          return None
      ##         ## self.printQ(newQueue)

      
    def printQ(self, q):
        count = 0
        while not q.empty():
            i = q.get()
            count = count + 1
            print(i)
        print(count)

    def __initPQ__(self):
        queue = PriorityQueue()
        ##print("Initing PQ: ")
        index = 0
        for i in self.A:
          ##  print(i)
            if i == self.X[index]:
                index = index + 1
                continue
            else:
                if len(i):
                    queue.put((len(i), (index, i) ))
            index = index + 1
        return queue
        
    def __initDomain__(self):
        D = []
        values = '123456789'
        for i in self.X:
            if i != '0':
                D.append(i)
            else:
                D.append(values)
        ##print("Domain")
        ##print(D)
        ##print(self.X)
        return D

    def __initAvailList__(self):
        A = []
        index = 0
        for cons in self.C:
            avail = self.D[index]
            ##print(self.D[index])
            ##print(len(self.D))
            ##print(len(self.C))
            ##print(len(self.D))
           ## print("constraints")
           ## print(self.C)
           ## print(cons)
           ## print(avail)
           ## print(self.X[index])
            if self.X[index] != '0':
                avail = avail 
            else:
                for char in cons:
          ##          print("Char: " + char)
                    avail = avail.replace(char, '')
            index = index + 1
            ##print(avail)
            if avail == '':
                ##print("Unsolvable at: " + str(index-1))
                ##print(A)
                return False
            ##if len(avail) == 0:
             ##   return False
            ##if avail == '':
             ##   return False
            A.append(avail)
        
       ## print("Testing")
       ## print(A)
       ## print(self.X.count('0'))
        return A
    
    def __initCons__(self):
        cons = []
        index = 0
        for d in self.D:
            d_cons = ''
            ##if len(d) != 1:
            d_cons = d_cons + self.__rowCons__(index)
            d_cons = d_cons + self.__colCons__(index)
            d_cons = d_cons + self.__cellCons__(index)
            ##else:
            ##d_cons = '123456789'.replace(d, '')
            ## flat = [i for sublist in d_cons for i in sublist
            d_cons = ''.join(set(d_cons))
            if d == None:
                d_cons = None
            cons.append(d_cons)
            index = index + 1
       ## print("CONS")
       ## print(len(cons))
        ##print(cons)
        return cons

    def __rowCons__(self, i):
        iter = self.sod.rowIter(i)
        return self.__grabCons__(iter)
   ## iter = self.sod.rowIter(i)
   ## for j in range(0, 9):
   ##     c = iter(j)
   ##     if self.sod.gamedata[c] in cons or self.sod.gamedata[c] == '0':
   ##         continue
   ##     else:
   ##         cons.append(self.sod.gamedata[c])
   ## return cons

    def __colCons__(self, i):
        iter = self.sod.colIter(i)
        return self.__grabCons__(iter)

    def __cellCons__(self, i):
        iter = self.sod.cellIter(i)
        return self.__grabCons__(iter)

    def __grabCons__(self, iter):
        cons = ''
        for i in range(0, 9):
            c = iter(i)
            if self.sod.gamedata[c] in cons or self.sod.gamedata[c] == '0':
                continue
            else:
                cons = cons + self.sod.gamedata[c]
        return cons
##file = open(input('Enter File Name: '))
file = open('sudokus/s16.txt')
x = Sudoku(file)
s = SudokuSolver(x)

##print (x)
##print(s.D)
##print()

##print(s.C)
##print("Availability List: ")
##print(s.A)

##print(s.D)
##print(type(''))
S = s.solve()
##print(S)
##print(S.solved())
##l = [1, 2, 3]
