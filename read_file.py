from afnd import AFND
from afd import AFD

lista_token = list()
lista_gr = list()
gr = list()

flag = 0

# Leitura do arquivo de entrada separando os dados em uma lista de GR e uma lista de Tokens
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


""" Utilização apenas para DEBUG
for token in lista_token:
    print(token)

for gra in lista_gr:
    print(gra)
"""

afnd = AFND(lista_token, lista_gr)

afnd.processar_tokens()
afnd.processar_gr()

print("AFND")
afnd.print_afnd()

afd = AFD(afnd=afnd)

afd.determinar()

print("AFD")
afd.print_afd()

afd.minimizar()

print("AFD MINIMIZADO")
afd.print_afd()

afd.add_estados_erro()
print("AFD MINIMIZADO COM ESTADO DE ERRO")
afd.print_afd()


