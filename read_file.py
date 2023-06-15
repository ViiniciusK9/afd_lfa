

lista_token = list()
lista_gr = list()
gr = list()

flag = 0


with open("input", "r") as file:
    for line in file:
        print(line[0], line[1])
        if ("$" == line[0] and "$" == line[1]):
            print("caiu")
            lista_gr.append(gr.copy())
            flag = 0
            gr.clear()
        elif (line.startswith("$")):
            # atomato
            flag = 1
            pass
        elif (flag == 1):
            gr.append(line)
        else:
            lista_token.append(line)


    
for token in lista_token:
    print(token)

for gra in lista_gr:
    print(gra)





