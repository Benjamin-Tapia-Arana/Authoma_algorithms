Alfabeto = []
modelo = {}
endlist= []
flg=0
isstart=0
isend=0


# MENÚ
attempts = 10
while True:
    try:
        fileName, newFileName = input('\nIngrese nombre del archivo a leer: '), input('Ingrese nombre del archivo a crear: ')
        f = open(fileName, "r")
        break
    except FileNotFoundError:
        print('\nEl archivo a leer no existe en la ruta especificada')
        attempts -= 1
        if(attempts <= 0):
            print('\nDemasiados intentos inválidos\n\n***SE CERRÓ EL PROGRAMA***\n')
            exit()
        option = input('\n¿Desea reintentar? (S/N): ')
        while True:
            if option == 'S': break
            elif option == 'N':
                print('\n***SE CERRÓ EL PROGRAMA***\n')
                exit()
            else: option = input('\nIntroduzca una opción válida\n\n¿Desea reintentar? (S/N): ')


# Lector del archivo
for x in f:
    if x == "Estados\n":
        flg=1
        continue
    if x == "Alfabeto\n":
        flg=2
        continue
    if x == "Transiciones\n":
        flg=3
        continue

    isstart=0
    isend=0
    x=x.replace('\n','')
    
    # lee los nodos
    if flg==1:
        if x[0] == ">":             # si son iniciales
            isstart=1
            x=x.replace(">","")
        if x[0] == "*":             # si son finales
            isend=1
            x=x.replace("*","")
            endlist.append(x)

        modelo[x]={}
        modelo[x]["inicial"] =isstart 
        modelo[x]["final"] =isend

    if flg==2:
        Alfabeto.append(x)          # añade el alfabeto a una lista

    if flg==3:
        x= x.split()
        try:                        # añade los nodos a los que se conecta
            modelo[x[0]][x[1]].append(x[3])
        except KeyError:
            modelo[x[0]][x[1]] = [x[3]]
        
f.close()

    #itera sobre todas las conecciones posibles solo mediante epsilons y añade los nodos a una lista
def epsilon_enclosure(automata,nodo, total):
    pasos = []
    subnodo = modelo[nodo]
    if "epsilon" in subnodo:
        pasos=subnodo["epsilon"]
        for i in subnodo["epsilon"]:
            if i != nodo:
                if i in total:
                    return pasos, total
                total.append(i)
                
                    
                res = epsilon_enclosure(automata,i,total)
                pasos.extend(res[0])
                total.extend(res[1])
                
    return pasos, total


for i in modelo.keys():                            
    enclosure = []
    enclosure = epsilon_enclosure(modelo, i, enclosure)[0]
    enclosure = list(set(enclosure))
    if len(enclosure) > 0:
        modelo[i].pop("epsilon")
        for j in enclosure:
            for k in Alfabeto:
                try:
                    if j not in modelo[i][k]:   # para que no se repitan nodos
                        modelo[i][k].append(j)
                except KeyError:
                    modelo[i][k] = [j]
            if j in endlist:
                modelo[i]["final"]=1



        
# escribo en un archivo     
ans = open(newFileName, "w")

#en los estados cambia cuales son finales
ans.write("Estados\n")
for i in modelo.keys():
    if modelo[i]["inicial"]==1:
        ans.write(">")
    if modelo[i]["final"]==1:
        ans.write("*")
    ans.write(i+"\n")

#el alfabeto se mantiene constante
ans.write("Alfabeto\n")
for i in Alfabeto:
    ans.write(i+"\n")

#muevo todos los valores del diccionario
ans.write("Transiciones\n")
for i in modelo.keys():
    for j in Alfabeto:    
        try:
            for k in modelo[i][j]:
                ans.write(i+ " "+j+ " -> "+k+"\n")
        except KeyError:
            pass

ans.close()
        
















