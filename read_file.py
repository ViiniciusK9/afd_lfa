"""
Ler a linha
identificar se é um token
se for token -> tratar token
se for uma GR -> tratar GR

"""
from afnd import AFND

lista_token = list()
lista_gr = list()
gr = list()

flag = 0


with open("input", "r", encoding="utf-8") as file:
    for line in file:
        #print(line[0], line[1])
        if ("$" == line[0] and "$" == line[1]):
            lista_gr.append(gr.copy())
            flag = 0
            gr.clear()
        elif (line.startswith("$")):
            # atomato
            flag = 1
            pass
        elif (flag == 1):
            gr.append(line.replace("\n", ""))
        else:
            lista_token.append(line.replace("\n", ""))


    
for token in lista_token:
    print(token)

for gra in lista_gr:
    print(gra)


afnd = AFND(lista_token, lista_gr)

print(afnd.list_states)
afnd.processar_tokens()
afnd.processar_gr()
print(afnd.list_states, " tamanho: ", len(afnd.list_states))

afnd.print_afnd()


'''
for state in afnd.list_states:
    print(f"State: {state.identifier}\nInitial: {state.initial}\nFinal: {state.final}\n", end="")
    print("Ways: ")
    for way in state.ways:
        print(way)

'''
