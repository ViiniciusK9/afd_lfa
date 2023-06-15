from state import STATE

class AFND:
    def __init__(self, lista_tokens, lista_gr) -> None:
        self.list_tokens = lista_tokens
        self.list_gr = lista_gr
        self.list_states = list()
        self.quantity_state = 0

    def processar_tokens(self):
        for token in self.list_tokens:
            if (len(token) != 0):
                    continue
            if (not self.list_states):
                # esta vazia - criar estado inicial
                
                initial_state = STATE(True, self.quantity_state)
                self.quantity_state += 1
                self.list_states.append(initial_state) # Adicionando estado inicial a lista de estados
                state = initial_state
                for l in token:
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
                    new_state = STATE(False, self.quantity_state)
                    self.list_states.append(new_state)
                    state.add_way(self.quantity_state, l)
                    self.quantity_state += 1
                    state = new_state
                state.set_final(True)
                

    def get_initial_state(self) -> STATE:
        for state in self.list_states:
            if state.initial == True:
                return state
        return STATE(False, -1)




    