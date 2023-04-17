Alfabeto = []
modelo = {}
endlist= []
flg=0
isstart=0
isend=0


# Lector del archivo
f = open("nfae.txt", "r")
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
def epsilon_enclosure(automata,nodo):
    pasos=[]
    subnodo = modelo[nodo]
    if "epsilon" in subnodo:
        pasos=subnodo["epsilon"]
        for i in subnodo["epsilon"]:
            if i != nodo:
                pasos.extend(epsilon_enclosure(automata,i))
    return pasos


for i in modelo.keys():                            
    enclosure = epsilon_enclosure(modelo, i)
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



print(modelo)







        
        

        
















