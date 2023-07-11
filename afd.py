from tabulate import tabulate
from state import STATE
from afnd import AFND
import queue

class AFD():
    def __init__(self, afnd : AFND) -> None:
        self.afnd = afnd
        self.list_states = list()
        self.quantity_state = afnd.quantity_state
        self.header = afnd.header
    
    
    def print_afd(self):
        mat = dict()

        headers = list(self.header.copy())
        
        self.list_states = sorted(self.list_states, key= lambda state: state.identifier)
        
        for state in self.list_states:
            aux = dict()
            print(state.identifier, " | ", end="")
            for way in state.ways:
                if(aux.get(way[1]) != None):
                    aux[way[1]] = f"{aux[way[1]]}, {way[0]}"
                else:
                    aux[way[1]] = f"{way[0]}"
                print(way, end=" ")
            print()
            for header in headers:
                if(not (aux.get(header) != None)):
                    aux[header] = ""
                

            mat[state.identifier] = aux.copy()

        mat_aux = list()
        aux_list = list()
        for state in self.list_states:
            aux_list.clear()
            aux_list.append(f"{'*' if (state.final == True) else ''}{state.identifier}")
            for header in headers:
                aux_list.append(mat[state.identifier].get(header))
            mat_aux.append(aux_list.copy())

        headers.insert(0, "Estados")
        for key, values in mat.items():
            print(key, values)
        

        print(tabulate(mat_aux, headers, tablefmt="heavy_grid"))
    
    
    
    def determinar(self):
        q = queue.Queue()
        q.put(self.afnd.get_initial_state())
        
        while (not q.empty()):  
            dic = dict()
            state = q.get()
            
            current_state = STATE(identifier=state.identifier, initial=state.initial)
            current_state.final = state.final
            
            if (exists_state(self.list_states, current_state.identifier)):
                remove_state(self.list_states, current_state.identifier)
            
            for way in state.ways:
                if (dic.get(way[1]) != None):
                    dic[way[1]].append(way[0])
                else:
                    dic[way[1]] = [way[0]]
            
            s = set()
            for k, v in dic.items():
                if (len(v) == 1):
                    current_state.add_way(v[0], k)
                    s.add(v[0])
                else:
                    if(not exists_mult_state(self.list_states, v)):
                        new_state = STATE(identifier= self.quantity_state, initial=False)
                        new_state.mult = v
                        self.quantity_state += 1
                        for i in v:
                            aux_state = self.afnd.get_state(i)
                            if (aux_state.final):
                                new_state.final = True
                            for way in aux_state.ways:
                                new_state.add_way(way[0], way[1])
                        self.list_states.append(new_state)
                        current_state.add_way(self.quantity_state - 1, k)
                        q.put(new_state)
                        
            self.list_states.append(current_state)
            for i in s:
                if (not exists_state(self.list_states, i)):
                    q.put(self.afnd.get_state(i))         
            
            print(dic)
            print(s)
    
    
        
def exists_state(list_states, id) -> bool:
    flag = False
    for state in list_states:
        if (state.identifier == id):
            flag = True
            break

    return flag


def remove_state(list_states, id):
    aux_state = None
    
    for state in list_states:
        if (state.identifier == id):
            aux_state = state
            break
        
    if (aux_state != None):
        list_states.remove(aux_state)
        
        
def exists_mult_state(list_states, mult) -> bool:
    flag = False
    for state in list_states:
        if ((flag == False) and (state.mult != None) and (len(state.mult) == len(mult))):
            x = len(mult) 
            a = sorted(state.mult)
            mult = sorted(mult)
            flag = True
            for i in range(x):
                if (mult[i] != a[i]):
                    flag = False

    return flag
        