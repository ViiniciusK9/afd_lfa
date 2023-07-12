from tabulate import tabulate
from state import STATE
from afnd import AFND
import queue

class AFD():
    def __init__(self, afnd : AFND) -> None:
        self.afnd = afnd
        self.list_states = list()
        self.list_states_aux = list()
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
                continue

            for way in state.ways:
                if (dic.get(way[1]) != None):
                    dic[way[1]].add(way[0])
                else:
                    dic[way[1]] = set()
                    dic[way[1]].add(way[0])
            
            for k in dic.keys():
                dic[k] = list(dic[k])

            
            s = set()
            for k, v in dic.items():
                if (len(v) == 1):
                    current_state.add_way(v[0], k)
                    s.add(v[0])
                else:
                    if(not exists_mult_state(self.list_states_aux, v)):
                        new_state = STATE(identifier= self.quantity_state, initial=False)
                        new_state.mult = v
                        self.quantity_state += 1
                        for i in v:
                            aux_state = self.afnd.get_state(i)
                            if (aux_state.final):
                                new_state.final = True
                            for way in aux_state.ways:
                                new_state.add_way(way[0], way[1])
                        current_state.add_way(self.quantity_state - 1, k)
                        q.put(new_state)
                        self.list_states_aux.append(new_state)
            
            self.list_states.append(current_state)
            for i in s:
                if (not exists_state(self.list_states, i)):
                    q.put(self.afnd.get_state(i))         
            
            print(f"ESTADO ATUAL: {current_state.identifier}\n ")
            print(dic)
            print(s)
    

    def minimizar(self):
        """
            Remover estados mortos e inalcançáveis, porem devido a forma de determinação do automato
            já eliminamos os estados inalcançaveis com isso iremos apenas remover os estados mortos.
        """
        for state in self.list_states:
            flag = False
            q = queue.Queue()
            q.put(state)

            visited = list()
            for i in range(self.quantity_state):
                visited.append(0)

            while (not q.empty()):
                at_state = q.get()
                visited[at_state.identifier] = 1
                if (at_state.final == True):
                    flag = True
                    break
                for way in at_state.ways:
                    if (visited[way[0]] == 0):
                        q.put(get_state(self.list_states, way[0]))


            if (not flag):
                self.list_states.remove(state)


    def add_estados_erro(self):
        """
            Adicicionar estado de erro em todas as transições vazias
        """
        if (not exists_state_error(self.list_states)):

            self.list_states.append(STATE(initial=False, identifier=-1))

            for state in self.list_states:
                s = set()
                for way in state.ways:
                    s.add(way[1])
                
                aux = self.header.difference(s)
                for tr in aux:
                    state.add_way(-1, tr)
        

def exists_state_error(list_states) -> bool:
    flag = False
    for state in list_states:
        if (state.identifier == -1):
            flag = True
    return flag


def get_state(list_states, id) -> STATE | None:
    for state in list_states:
        if (state.identifier == id):
            return state
    return None
        
def exists_state(list_states, id) -> bool:
    flag = False
    for state in list_states:
        if (state.identifier == id):
            flag = True

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
        