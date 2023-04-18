import os
import copy

# FUNCIÓN QUE LEE EL ARCHIVO DE TEXTO Y ENTREGA UNA LISTA CON EL AUTÓMATA, EL ALFABETO Y UNA LISTA DE LOS ESTADOS
def automataTextReader():
    filePath = os.path.join(os.path.dirname(__file__), input('\nFile name: '))
    textFile = open(filePath, 'r')
    automata = [] # LISTA DE DICCIONARIOS QUE REPRESENTAN AL AUTÓMATA, CADA DICCIONARIO REPRESENTA UN ESTADO
    alphabet = [] # LISTA CON SÍMBOLOS DEL ALFABETO
    states = [] # LISTA CON ESTADOS
    step = None

    for row in textFile: # CREADOR DEL AUTÓMATA Y EL ALFABETO
        if(row == 'Estados\n'):
            step = 0
        elif(row == 'Alfabeto\n'):
            step = 1
        elif(row == 'Transiciones\n'):
            step = 2

        # SE CREAN LOS DICCIONARIOS PERTENECIENTES A CADA ESTADO Y SE AGREGAN
        # LOS ESTADOS A LA LISTA DE ESTOS
        elif(step == 0 and row != '\n'):
            dicState = {'Name': row.strip('\n').strip('{>*}'), 'Initial': False, 'Final': False, 'epsilon': []}
            state = row.strip('\n').strip('{>*}')
            if(row[0] == '>'):
                dicState['Initial'] = True
            if(row[0] == '*' or row[1] == '*'):
                dicState['Final'] = True
            automata.append(dicState)
            states.append(state)

        # AGREGA LOS SÍMBOLOS DEL ALFABETO COMO UNA KEY CON VALOR UNA LISTA VACIA,
        # YA QUE AÚN NO SE AGREGAN LAS TRANSICIONES
        elif(step == 1 and row != '\n'):
            alphabet.append(row.strip('\n'))
            for dict in automata:
                dict[row.strip('\n')] = []

        # AGREGA LOS ESTADOS A LOS QUE TRANSICIONAN CADA ESTADO DADO CADA SÍMBOLO
        elif(step == 2 and row != '\n'):
            transition = row.strip('\n').split(' ')
            for i in transition:
                i.strip('{').strip('}')
            for dict in automata:
                if dict['Name'] == transition[0]:
                    dict[transition[1]].append(transition[3])

    textFile.close()
    return [automata, alphabet, states]

# FUNCIÓN RECURSIVA QUE ELIMINA TODOS LOS ESTADOS QUE NO TIENEN SENTIDO DE ESTAR
# EN EL AUTÓMATA, ESTADO A LOS QUE NO SE PUEDE ACCEDER
def eliminateUselessStates(automata, alphabet):
    automata = copy.deepcopy(automata)
    alphabet = copy.deepcopy(alphabet)
    newAutomata = []
    uselessStates = []
    for i in automata:
        useless = None
        if(i['Initial'] == False):
            useless = True
            for j in automata:
                if(i['Name'] != j['Name']):
                    for symbol in alphabet:
                        if(i['Name'] in j[symbol]):
                            useless = False
        if useless == True:
            uselessStates.append(i['Name'])
    for state in automata:
        if state['Name'] not in uselessStates:
            newAutomata.append(state)
    if newAutomata == automata:
        return newAutomata
    else:
        return eliminateUselessStates(newAutomata)
    
# FUNCIÓN RECURSIVA QUE RETORNA UNA LISTA DE DICCIONARIOS COMPUESTAS POR CADA
# POSIBLE PAREJA DE ESTADOS DEL AUTÓMATA (NO IMPORTA EL ORDEN Y NO HAY PAREJAS
# DE UN MISMO ESTADO) Y POR LA PROPIEDAD MARK
def statesPairSetter(automata):
    automata = copy.deepcopy(automata)
    pairs = []
    def recursive(automata, pairs):
        if len(automata) > 1:
            for i in range(1, len(automata)):
                pair = {'Pair': [automata[0]['Name'], automata[i]['Name']],
                        'Mark': False}
                pairs.append(pair)
            automata.pop(0)
            return recursive(automata, pairs)
        else:
            return pairs 
    return recursive(automata, pairs)

# FUNCIÓN RECURSIVA QUE RETORNA LA LISTA DE DICCIONARIOS DE PAREJAS DE ESTADOS
# CON LAS PAREJAS CORRESPONDIENTES MARCADAS
def pairsMarker(automata, alphabet, pairs):
    automata = copy.deepcopy(automata)
    alphabet = copy.deepcopy(alphabet)
    pairs = copy.deepcopy(pairs)
    newPairs = copy.deepcopy(pairs)

    for pair1 in newPairs:
        state1 = None
        state2 = None
        for state in automata:
            if state['Name'] == pair1['Pair'][0]:
                if state1 != None:
                    state2 = state
                else:
                    state1 = state
            if state['Name'] == pair1['Pair'][1]:
                if state1 != None:
                    state2 = state
                else:
                    state1 = state
        if((state1['Final'] == False and state2['Final'] == True) or (state1['Final'] == True and state2['Final'] == False)):
            pair1['Mark'] = True
        else:
            for symbol in alphabet:
                s1 = state1[symbol][0]
                s2 = state2[symbol][0]
                for pair2 in newPairs:
                    if((s1 in pair2['Pair']) and (s2 in pair2['Pair']) and (pair2['Mark'] == True) and (s1 != s2)):
                        pair1['Mark'] = True
    
    recurse = False
    for i in range(len(pairs)):
        if(pairs[i]['Mark'] != newPairs[i]['Mark']):
            recurse = True

    if recurse == True:
        return pairsMarker(automata, alphabet, newPairs)
    return newPairs

# FUNCIÓN QUE RECIBE UNA LISTA DE PAREJA ESTADOS Y RETORNA UNA LISTA SOLO CON LAS
# PAREJAS DE ESTADOS MARCADOS
def nonMarkPairsSetter(pairs):
    pairs = copy.deepcopy(pairs)
    newPairs = []
    for pair in pairs:
        if(pair['Mark'] == False):
            newPairs.append(pair)
    return newPairs

# FUNCIÓN QUE RETORNA UNA LISTA DE CONJUNTOS (LISTAS) DE ESTADOS, FUSIONANDO
# LOS CONJUNTOS CON ESTADOS EN COMÚN, ADEMÁS SE AÑADEN LOS ESTADOS QUE QUEDARON
# INDEPENDIENTES COMO CONJUNTOS
def mergePairs(pairs, states):
    pairs = copy.deepcopy(pairs)
    justPairs = []
    mergedPairs = []

    for pair in pairs:
        justPairs.append(pair['Pair'])

    for pair in justPairs:
        used = False
        for i in range(0, len(mergedPairs)):
            if((pair[0] in mergedPairs[i]) and (pair[1] in mergedPairs[i])):
                used = True
            elif((pair[0] in mergedPairs[i]) and (pair[1] not in mergedPairs[i]) and (used == False)):
                mergedPairs[i].append(pair[1])
                used = True
            elif((pair[1] in mergedPairs[i]) and (pair[0] not in mergedPairs[i]) and (used == False)):
                mergedPairs[i].append(pair[0])
                used = True
        if(used == False):
            mergedPairs.append(pair)
    
    for state in states:
        present = False
        for set in mergedPairs:
            if state in set:
                present = True
        if(present == False):
            mergedPairs.append([state])

    return mergedPairs





# EXAMPLE:
automataAlphabetStates = automataTextReader()
automata = automataAlphabetStates[0]
alphabet = automataAlphabetStates[1]
states = automataAlphabetStates[2]

automata = eliminateUselessStates(automata, alphabet)

pairs = statesPairSetter(automata)

newPairs = pairsMarker(automata, alphabet, pairs)

nonMarkPairs = nonMarkPairsSetter(newPairs)

nonMarkPairsSet = mergePairs(nonMarkPairs, states)

print(nonMarkPairsSet)






# attempts = 10
# while True: # LECTOR DEL ARCHIVO
#     try:
#         filePath = os.path.join(os.path.dirname(__file__), input('\nFile name: '))
#         textFile = open(filePath, 'r')
#         break
#     except FileNotFoundError:
#         print('\nEl archivo no existe en la ruta especificada')
#         attempts -= 1
#         if(attempts == 0):
#             print('\nDemasiados intentos inválidos, se cerrará el programa\n\n***SE CERRÓ EL PROGRAMA***\n')
#             exit()
#         option = input('\n¿Desea reintentar? (S/N): ')
#         while True:
#             if option == 'S':
#                 break
#             elif option == 'N':
#                 print('\n***SE CERRÓ EL PROGRAMA***\n')
#                 exit()
#             else:
#                 option = input('\nIntroduzca una opción válida\n\n¿Desea reintentar? (S/N): ')