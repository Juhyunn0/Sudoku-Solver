#!/usr/bin/env python
# coding: utf-8

# In[391]:


import sys
import pandas as pd


if len(sys.argv) != 3:
    print("ERROR : Not enough/too many/illegal input arguments")
    sys.exit(1)

try:
    MODE = sys.argv[1]  # ALGO
    FILENAME = sys.argv[2]  # FIRST
    possible_modes = ['1', '2', '3', '4']
    # print(f'MODE:{MODE},FILENAME:{FILENAME}')
    # print(type(FILENAME))
    data = pd.read_csv(FILENAME, header=None)

    if MODE in possible_modes:
        print("Jung, Juhyun, A20521244 solution:")
        print("Input file:", FILENAME)
        print("Algorithm:", end=' ')

        if MODE == '1':
            print("brute force search")
        elif MODE == '2':
            print("Constraint Satisfaction Problem back-tracking search")
        elif MODE == '3':
            print("CSP with forward-checking and MRV heuristics")
        else:
            print("TEST if the completed puzzle is correct")
    else:
        print("ERROR : Not enough/too many/illegal input arguments")
except:
    print("ERROR : Not enough/too many/illegal input arguments")


# In[392]:


def count(n):
    return n+1
def ascending_order(csp,assignment):
    var_list=[]
    for var in csp.variables:
        if var not in assignment.keys(): # is var already assigned? 
            var_list.append(var)
    return var_list[0]

def mrv(csp,assignment):
    # assigment = {}
    # csp.variable = ['1','2','5','52','81']
    
    var_list=[]
    length_list=[]
    for var in csp.variables:
        if var not in assignment.keys(): # is var already assigned? 
            var_list.append(var)
            length_list.append(len(csp.domains[var]))

    combined_list = list(zip(var_list,length_list))
    return sorted(combined_list, key=lambda x:x[1])[0][0]    
    
def inference_CSP(csp,var,val,assignment):
    """
    
    check : the value in the board(original) vs 'val'
    i.e csp.domain vs the val 
    
    """
    global c
    
    if val not in csp.domains[var]:
#         print(f"Fasle becuase {var}'s domain : {csp.domains[var]} ")
        return False
    return True
    

def one2nine(csp,var,assignment):
    return ['1','2','3','4','5','6','7','8','9']

def domain_var(csp,var,assigment):
    return csp.domains[var]
    
def forward_checking(csp, var, val, assignment):
    global c 
    if var not in assignment.keys(): # is var already assgined?
        for adj_var in csp.adj[var]: # each variables of neighbor of var
            
            if adj_var not in assignment.keys(): # is adj variable already assigned?
                if val in csp.domains[adj_var]:
                    csp.domains[adj_var].remove(val)
                
                if len(csp.domains[adj_var])==0: # after removing val in adj_val, is there val in adj_var?
                    # this means adj_var has no val
                    csp.domains[adj_var].append(val)
                    return False
            else:
                if assignment[adj_var] == val: # is adj_var val?
                    return False 
    else:
        return False
    return True
def backtracking_search(csp):
    global c
    def backtrack(csp,assignment):
        global c 
        if len(assignment)==(len(csp.variables)):
            return assignment
        
        var = csp.selected_unassigned_variable(csp,assignment)#mrv(csp,assignment) # select_unassigned_variable(csp,assignment)
        for value in csp.order_domain_values(csp,var,assignment): # order_domain_value(var,assignment,csp):
            c=count(c)
            # check : is it okay for the variable to be the value?
            if csp.conflict(var,value,assignment):
                #YES (no conflict)
                infer = csp.inference(csp,var,value,assignment)  # infer : True / False 
                if infer:
                    Before_domains = csp.domains.copy()
                    csp.assign(var,value,assignment)
                    result = backtrack(csp,assignment)
                    
                    if result:
                        return result
                    csp.domains = Before_domains
                    csp.unassign(var,assignment)
        return False
    result = backtrack(csp,{})
    return result



# In[393]:


class csp:
    def __init__(self,variables, domains, adj,selected_unassigned_variable,order_domain_values,inference):
        self.variables = variables 
        self.domains = domains
        self.adj = adj
        self.inference = inference
        self.order_domain_values = order_domain_values
        self.selected_unassigned_variable = selected_unassigned_variable
        
        
    def assign(self,variable,value, assignment):
        assignment[variable] = value
        
    def unassign(self,variable,assignment):
        if variable in assignment:
            del assignment[variable]
            
    
    def conflict(self, variable,value ,assignment):
        """
        
        check whether specific variable is complete or not when the variable is the specific value 
        
        output:
                True : in assignment, Every adj variable does not have the same value as the variable. 
                False : in assignment, Any adj variable already have the same value as the variable. 
        
        """
        # each adj variable 
        for adj_variable in self.adj[variable]:
            # is adj variable in assignment?
            # Yes (adj_variable is in assignment)
            if adj_variable in assignment:
                # is adj_variable in assignment the value?
                # Yes (ajd_variable in assingment is the value)
                if assignment[adj_variable]==value:
#                     print(f"conflict in assignment, because assignment[{adj_variable}] : {assignment[adj_variable]}")
                    return False
        return True

            
        


# In[477]:


import time
class Soduku(csp):
    def __init__(self,FILENAME,MODE):
        data = pd.read_csv(FILENAME, header=None)
        self.FILENAME = FILENAME
        self.board = data.values.tolist()
        for i in range(9):
            for j in range(9):
                if type(self.board[i][j])==int:
                    self.board[i][j]=str(self.board[i][j])
        
        self.MODE = MODE
        selected_unassigned_variable = ascending_order
        inference = inference_CSP
        order_domain_values = one2nine
        if MODE == '3':
            selected_unassigned_variable = mrv
            order_domain_values = domain_var
            inference = forward_checking
        super().__init__(self.getVariable(),self.getDomain(),self.getAdj(),selected_unassigned_variable,order_domain_values,inference)
        global c 
        c=1
        
        print("Input puzzle :\n")
        for row in self.board:
            print(",".join(map(str,row)))
    
        
        
    def display(self):
        for row in self.board:
            print(",".join(map(str,row)))
    
    def valid(self,state):
        for row in state:
            if 'X' in row:
                return False
        
        # Check row : ONE 1,2,3,4,5,6,7,8,9?
        for row in state:
            if sorted(list(map(float,row)))!=list(range(1,10)):
                return False
        
        # Check column : ONE 1,2,3,4,5,6,7,8,9
        for i in range(len(state)):
            column = state[:][i]
            if sorted(list(map(float,column)))!=list(range(1,10)):
                return False
        
        # Check 3x3 boxes
        for i in range(0,7,3): # i = 0, 3, 6
            for j in range(0,7,3): # j =0, 3, 6
                box = []
                for k in range(3):
                    for m in range(3):
                        box.append(state[i+k][j+m])
                if sorted(list(map(float,box)))!=list(range(1,10)):
                    return False
        return True

            
        
    
    def analyze(self):
        state= self.board
        # Is there 'X'?
        for row in state:
            if 'X' in row:
                return False
        
        # Check row : ONE 1,2,3,4,5,6,7,8,9?
        for row in state:
            if sorted(list(map(float,row)))!=list(range(1,10)):
                return False
        
        # Check column : ONE 1,2,3,4,5,6,7,8,9
        for i in range(len(state)):
            column = state[:][i]
            if sorted(list(map(float,column)))!=list(range(1,10)):
                return False
        
        # Check 3x3 boxes
        for i in range(0,7,3): # i = 0, 3, 6
            for j in range(0,7,3): # j =0, 3, 6
                box = []
                for k in range(3):
                    for m in range(3):
                        box.append(state[i+k][j+m])
                if sorted(list(map(float,box)))!=list(range(1,10)):
                    return False
        
        # Meet all conditions
        return True

    def convert_to_number(self, x):
        if x.isdigit():
            return int(x)
        return x
            
    def twoD2oneD(self,i,j):
        return i*9+j
    
    def oneD2twoD(self,k):
        if type(k)==str:
            k=int(k)
        i=k//9
        j=k-i*9
        return i,j
    
    def getVariable(self):
        var_list = []
        
        for k in range(81):
            i,j = self.oneD2twoD(k)
            if self.board[i][j]=='X':
                var_list.append(f'{k}')
        return var_list    
    
    def getAdj(self):
        adj_dic={}
        for k in range(81):
            i,j = self.oneD2twoD(k)
            if self.board[i][j]=='X':
                # check row 
                
                for m in range(9):
                    row=m*9+j
                    if m!=i:
                        if self.board[m][j]=='X':
                            if f'{k}' in adj_dic:
                                adj_dic[f'{k}'].append(f'{row}')
                            else:
                                adj_dic[f'{k}'] = [f'{row}']
                
                # check column
                for n in range(9):
                    column=i*9+n
                    if n!=j:
                        if self.board[i][n]=='X':
                            if f'{k}' in adj_dic:
                                adj_dic[f'{k}'].append(f'{column}')
                            else:
                                adj_dic[f'{k}'] = [f'{column}']
                
                # check box
                a = i//3
                b = j//3
                for m in range(a*3,(a+1)*3):
                    for n in range(b*3,(b+1)*3):
                        if ((m!=i) and (n!=j)):
                            if self.board[m][n]=='X':
                                box=self.twoD2oneD(m,n)
                                if f'{k}' in adj_dic:
                                    adj_dic[f'{k}'].append(f'{box}')
                                else:
                                    adj_dic[f'{k}'] = [f'{box}']

                                    
        #sorted value (small to big)
        for key, value in adj_dic.items():
            adj_dic[key] = sorted(value, key=int)
        adj_dic = dict(sorted(adj_dic.items(), key=lambda x: int(x[1][0])))

        return adj_dic
    
    def getDomain(self):
        domain_dic = {}
        var_list = self.getVariable()
        
        for var in var_list:
            possible_nums=['1','2','3','4','5','6','7','8','9']
            i,j = self.oneD2twoD(int(var))
            for k in range(9):
                #check row

                if self.board[i][k] in possible_nums:
                    possible_nums.remove(self.board[i][k])
                #check column
                if self.board[k][j] in possible_nums:
                    possible_nums.remove(self.board[k][j]) 
            # check box 
            i = i//3
            j = j//3   
            for m in range(i*3,(i+1)*3):
                for n in range(j*3,(j+1)*3):
                    if self.board[m][n] in possible_nums:
                        possible_nums.remove(self.board[m][n])
        
            if var in domain_dic:
                domain_dic[var].append(possible_nums)
            else:
                domain_dic[var]=possible_nums
        return domain_dic
    def complete(self,assignment):
        for k in assignment:
            i,j = self.oneD2twoD(int(k))
            self.board[i][j] = assignment[k]
            
    def save(self):
        df1 = pd.DataFrame(self.board)
        
        name  = self.FILENAME[:-4]+"_SOLUTION"

        df1.to_csv(f"{name}.csv",header=False,index=False)

    
    def empty_location(self): # Find empty location 
        for i in range(9):
            for j in range(9):
                if self.board[i][j]=='X':
                    return i,j
        return None,None
    
    def BFS(self):
        global c
        global flag
        global timeEnd 
        global timeStart
        
        i,j = self.empty_location()
        if i == None:
            if self.analyze():
                return True
            else:
                return False
        else:
            domain = ['1','2','3','4','5','6','7','8','9']
            
            for nums in domain:
                c=count(c)
                self.board[i][j]=nums
                if self.BFS(): 
                    return True
                else:
                    if self.board[i][j]=='9':
                        c=c-1
                    self.board[i][j]='X'
                
    def main(self):
        global flag
        global c
        global timeEnd
        global timeStart
        
        flag = False
        
        if self.MODE== '1':
            c=0
            T1=0
            timeStart = time.time()
            result_state  = self.BFS()
            timeEnd = time.time()
            T1 = timeEnd-timeStart
            if not result_state:
                print("Solution could not be found.")
            else:
                print(f'\n\nNumber of search tress nodes generated : {c}')
                print(f'Search time: {T1:.8f} seconds\n')
                print('Solved puzzle: \n')
                self.display()
                self.save()
                
                
        elif self.MODE == '2':
            c=0
            T1=0
            timeStart= time.time()
            result_state = backtracking_search(self)
            timeEnd = time.time()
            T1 = timeEnd-timeStart
            if not result_state:
                print("Solution could not be found.")
            else:
                print(f'\n\nNumber of search tress nodes generated : {c}')
                print(f'Search time: {T1:.8f} seconds\n')
                print('Solved puzzle: \n')
                game.complete(result_state)
                self.display()
                self.save()
        elif self.MODE == '3':
            c=0
            T1=0
            timeStart= time.time()
            result_state = backtracking_search(self)
            timeEnd = time.time()
            T1 = timeEnd-timeStart
            if not result_state:
                print("\n\nSolution could not be found")
            else:
                print(f'\n\nNumber of search tress nodes generated : {c}')
                print(f'Search time: {T1:.8f} seconds\n')
                print('Solved puzzle: \n')
                game.complete(result_state)
                self.display()
                self.save()
            
            
        elif self.MODE == '4':
            print("")
            if self.analyze():
                print("This is a valid, solved, Sudoku puzzle.")
            else:
                print("ERROR: This is NOT a solved Sudoku puzzle.")

        


# In[474]:


FILENAME='testcase6.csv'
MODE='3'


# In[478]:


game=Soduku(FILENAME,MODE)
game.main()


# In[476]:


T=0
for i in range(10):
    
    game=Soduku(FILENAME,MODE)
    T = T+game.main()
T=T/10
print(f'T:{T:.10f}')


# In[429]:


print(T1)


# In[420]:


game=Soduku(FILENAME,MODE)
game.main()


# In[ ]:




