from state import STATE
from tabulate import tabulate

class AFND:
    def __init__(self, lista_tokens, lista_gr) -> None:
        self.list_tokens = lista_tokens
        self.list_gr = lista_gr
        self.list_states = list()
        self.quantity_state = 0
        self.header = set()

    def processar_tokens(self):
        for token in self.list_tokens:
            if (len(token) == 0):
                continue
            if (len(self.list_states) == 0):
                # esta vazia - criar estado inicial
                
                initial_state = STATE(True, self.quantity_state)
                self.quantity_state += 1
                self.list_states.append(initial_state) # Adicionando estado inicial a lista de estados
                state = initial_state

                for l in token:

                    self.header.add(l)
                    new_state = STATE(False, self.quantity_state)
                    self.list_states.append(new_state)
                    state.add_way(self.quantity_state, l)
                    self.quantity_state += 1
                    state = new_state


                state.set_final(True)
            else:
                # não esta vazia
                state = self.get_initial_state()
                for l in token:
                    self.header.add(l)
                    new_state = STATE(False, self.quantity_state)
                    self.list_states.append(new_state)
                    state.add_way(self.quantity_state, l)
                    self.quantity_state += 1
                    state = new_state
                state.set_final(True)            
    

    def processar_gr(self):
        for gr in self.list_gr:
            l_to_id = dict()
            
            for row in gr:
                print(l_to_id)
                """
                Saber qual estado esta, caso sejá o estado inicial se ele já estiver criado apenas obter ele, caso não esteja criado criar o estado inicial
                """
                letra_estado_atual = ''
                for i in range(len(row)):
                    if (row[i] == '<'):
                        letra_estado_atual = row[i+1]
                        break
                    
                    
                # Logica para o estado atual
                state = ''
                if (letra_estado_atual == 'S'):
                    # Se for o estado inicial sempre representado pela letra "S"
                    if (len(self.list_states) == 0):
                        # Se não possui nenhum estado la lista de estados, cria o estado inicial
                        state = STATE(True, self.quantity_state)
                        self.list_states.append(state)
                        self.quantity_state += 1
                        l_to_id['S'] = 0
                    else :
                        # Caso contratio obtem o estado inicial
                        state = self.get_initial_state()
                        l_to_id['S'] = 0
                else:
                    if (l_to_id.get(letra_estado_atual) != None):
                        # já existe esse estado
                        state = self.get_state(id=l_to_id.get(letra_estado_atual))
                    else:
                        # não existe esse estado
                        l_to_id[letra_estado_atual] = self.quantity_state
                        state = STATE(False, self.quantity_state)
                        self.list_states.append(state)
                        self.quantity_state += 1
                
                        
                # ler os caminhos para onde o estado atual pode ir
                ways = get_ways(row)
                
                for way in ways:
                    if (len(way) == 2):
                        # Transição para um não terminal
                        if (l_to_id.get(way[0]) == None):
                            # não existe esse estado
                            l_to_id[way[0]] = self.quantity_state
                            self.list_states.append(STATE(False, self.quantity_state))
                            self.quantity_state += 1
                            state.add_way(l_to_id.get(way[0]), way[1])
                            self.header.add(way[1])
                        else:
                            # existe este estado
                            self.header.add(way[1])
                            state.add_way(l_to_id.get(way[0]), way[1])
                            
                    elif (way[0] == "ε"):
                        # Possuio epsilon
                        state.final = True
                    else:
                        # Transição de um terminal
                        new_state = STATE(False, self.quantity_state)
                        new_state.final = True
                        self.quantity_state += 1
                        self.list_states.append(new_state)
                        self.header.add(way[0])
                        state.add_way(new_state.identifier, way[0])
                        
                        
                    

    def get_initial_state(self) -> STATE:
        for state in self.list_states:
            if state.initial == True:
                return state
        return STATE(False, -1)


    def get_state(self, id : int) -> STATE:
        for state in self.list_states:
            if state.identifier == id:
                return state
        return STATE(False, -1)


    def print_afnd(self):
        mat = dict()

        headers = list(self.header.copy())
        
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
        

def get_ways(row):
        ways = list()
        row = row.replace(" ", "")
        flag = 0
        len_r = len(row)
        for i in range(len_r):
            if (row[i] == '='):
                flag = 1
            elif (flag and row[i] == '<'):
                ways.append((row[i+1], row[i-1]))
            elif (flag and row[i] == '|' and row[i-1] != '>'):
                ways.append((row[i-1]))

        if (row[len(row)-1] != '>' and row[len(row)-1] != 'ε'):
            ways.append((row[len(row)-1]))
        
        # Verifica se tem épsilon transição na gramatica
        if ("ε" in row):
            ways.append(("ε"))
        return ways