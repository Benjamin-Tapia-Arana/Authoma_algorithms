import os
import copy


# FUNCIÓN QUE LEE EL ARCHIVO DE TEXTO Y ENTREGA UNA LISTA CON EL AUTÓMATA, EL
# ALFABETO Y UNA LISTA DE LOS ESTADOS
def automataTextReader(fileName):
    filePath = os.path.join(os.path.dirname(__file__), fileName)
    textFile = open(filePath, 'r')
    automata = [] # LISTA DE DICCIONARIOS QUE REPRESENTAN AL AUTÓMATA, CADA DICCIONARIO REPRESENTA UN ESTADO
    alphabet = [] # LISTA CON SÍMBOLOS DEL ALFABETO
    states = [] # LISTA CON ESTADOS
    step = None

    for row in textFile: # CREADOR DEL AUTÓMATA Y EL ALFABETO
        if row == 'Estados\n': step = 0
        elif row == 'Alfabeto\n': step = 1
        elif row == 'Transiciones\n': step = 2

        # SE CREAN LOS DICCIONARIOS PERTENECIENTES A CADA ESTADO Y SE AGREGAN
        # LOS ESTADOS A LA LISTA DE ESTOS
        elif (step == 0) and (row != '\n'):
            dicState = {'Name': row.strip('\n').strip('{>*}'), 'Initial': False, 'Final': False, 'epsilon': []}
            state = row.strip('\n').strip('{>*}')
            if row[0] == '>': dicState['Initial'] = True
            if (row[0] == '*') or (row[1] == '*'): dicState['Final'] = True
            automata.append(dicState)
            states.append(state)

        # AGREGA LOS SÍMBOLOS DEL ALFABETO COMO UNA KEY CON VALOR UNA LISTA VACIA,
        # YA QUE AÚN NO SE AGREGAN LAS TRANSICIONES
        elif (step == 1) and (row != '\n'):
            alphabet.append(row.strip('\n'))
            for dict in automata: dict[row.strip('\n')] = []

        # AGREGA LOS ESTADOS A LOS QUE TRANSICIONAN CADA ESTADO DADO CADA SÍMBOLO
        elif (step == 2) and (row != '\n'):
            transition = row.strip('\n').split(' ')
            for i in transition: i.strip('{').strip('}')
            for dict in automata:
                if dict['Name'] == transition[0]: dict[transition[1]].append(transition[3])

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
        if not i['Initial']:
            useless = True
            for j in automata:
                if i['Name'] != j['Name']:
                    for symbol in alphabet:
                        if i['Name'] in j[symbol]:
                            useless = False
        if useless:
            uselessStates.append(i['Name'])
    for state in automata:
        if state['Name'] not in uselessStates: newAutomata.append(state)
    if newAutomata == automata: return newAutomata
    else: return eliminateUselessStates(newAutomata)
    
# FUNCIÓN RECURSIVA QUE RETORNA UNA LISTA DE DICCIONARIOS COMPUESTAS POR CADA
# POSIBLE PAREJA DE ESTADOS DEL AUTÓMATA (NO IMPORTA EL ORDEN Y NO HAY PAREJAS
# DE UN MISMO ESTADO) Y POR LA PROPIEDAD MARK
def statesPairSetter(automata):
    automata = copy.deepcopy(automata)
    pairs = []
    def recursive(automata, pairs):
        if len(automata) > 1:
            for i in range(1, len(automata)):
                pair = {'Pair': [automata[0]['Name'], automata[i]['Name']], 'Mark': False}
                pairs.append(pair)
            automata.pop(0)
            return recursive(automata, pairs)
        else: return pairs 
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
                if state1 != None: state2 = state
                else: state1 = state
            if state['Name'] == pair1['Pair'][1]:
                if state1 != None: state2 = state
                else: state1 = state
        if (not state1['Final'] and state2['Final']) or (state1['Final'] and not state2['Final']): pair1['Mark'] = True
        else:
            for symbol in alphabet:
                s1 = state1[symbol][0]
                s2 = state2[symbol][0]
                for pair2 in newPairs:
                    if (s1 in pair2['Pair']) and (s2 in pair2['Pair']) and (pair2['Mark']) and (s1 != s2): pair1['Mark'] = True
    
    recurse = False
    for i in range(len(pairs)):
        if pairs[i]['Mark'] != newPairs[i]['Mark']: recurse = True
    if recurse: return pairsMarker(automata, alphabet, newPairs)
    return newPairs

# FUNCIÓN QUE RECIBE UNA LISTA DE PAREJA ESTADOS Y RETORNA UNA LISTA SOLO CON LAS
# PAREJAS DE ESTADOS MARCADOS
def nonMarkPairsSetter(pairs):
    pairs = copy.deepcopy(pairs)
    newPairs = []
    for pair in pairs:
        if not pair['Mark']: newPairs.append(pair)
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
            if (pair[0] in mergedPairs[i]) and (pair[1] in mergedPairs[i]):
                used = True
            elif (pair[0] in mergedPairs[i]) and (pair[1] not in mergedPairs[i]) and (not used):
                mergedPairs[i].append(pair[1])
                used = True
            elif (pair[1] in mergedPairs[i]) and (pair[0] not in mergedPairs[i]) and (not used):
                mergedPairs[i].append(pair[0])
                used = True
        if not used:
            mergedPairs.append(pair)
    
    for state in states:
        present = False
        for set in mergedPairs:
            if state in set:
                present = True
        if not present:
            mergedPairs.append([state])

    return mergedPairs

# FUNCIÓN QUE, USANDO EL RESTO DE LAS FUNCIONES DEFINIDAS MÁS ARRIBA, RECIBE EL
# NOMBRE DEL ARCHIVO .TXT QUE CONTENDRA LA DEFINICIÓN DE UN DFA Y EL NOMBRE DEL
# NUEVO ARCHIVO .TXT A CREAR QUE CONTENDRA AL DFA MINIMIZADO. FINALMENTE CREA EL
# NUEVO ARCHIVO .TXT CON EL DFA MINIMIZADO
def DFAminimizator(fileName, newFileName):
    automataAlphabetStates = automataTextReader(fileName)
    automata, alphabet, states = automataAlphabetStates[0], automataAlphabetStates[1], automataAlphabetStates[2]
    automata = eliminateUselessStates(automata, alphabet)
    nonMarkSets = mergePairs(nonMarkPairsSetter(pairsMarker(automata, alphabet, statesPairSetter(automata))), states)

    # FUNCIÓN QUE ESCRIBE LOS CONJUNTOS DE LOS NUEVOS ESTADOS. SE LE ENTREGAN TRES PARÁMETROS;
    # SET QUE RECIBE ELDICCIONARIO DEL ESTADO,
    # KEY QUE RECIBE EL KEY A ESCRIBIR,
    # CONJUNTO QUE INDICA SI SERÁ ESCRITO EN LA SECCIÓN DE CONJUNTOS O NO
    def writeSet(set, key, conjunto):
        set = copy.deepcopy(set)
        x = None
        if conjunto:
            if set['Initial']: newFile.write('>')
            if set['Final']: newFile.write('*')
        newFile.write('{')
        x = 0
        for state in set[key]:
            if x == 1: newFile.write(',')
            newFile.write(f'{state}')
            x = 1
        newFile.write('}')
        if conjunto: newFile.write('\n')

    # CREA UNA VARIABLE STR CON EL VALOR DEL NOMBRE DEL ESTADO INICIAL Y UNA LISTA CON TODOS LOS ESTADOS FINALES
    finalStates = []
    for state in automata:
        if state['Initial']: initial = state['Name']
        if state['Final']: finalStates.append(state['Name'])

    # CREA LA LISTA DE DICCIONARIOS DEL NUEVO AUTÓMATA
    newAutomata = []
    newStates = []
    for set in nonMarkSets:
        newState = {'Set': set, 'Initial': False, 'Final': False}
        for symbol in alphabet: newState[symbol] = []
        newAutomata.append(newState)
        newStates.append(set)
    
    # DEFINE LAS TRANSICIONES DEL DFA MINIMIZADO
    for newStateSet in newAutomata:
        newState = newStateSet['Set']
        for state in automata:
            if state['Name'] in newState:
                for symbol in alphabet:
                    if len(newStateSet[symbol]) == 1:    
                        if newStateSet[symbol][0] in newState: newStateSet[symbol] = state[symbol]
                    elif len(newStateSet[symbol]) == 0:
                        newStateSet[symbol] = state[symbol]
    for newStateSet in newAutomata:
        for symbol in alphabet:
            for set in newStates:
                if newStateSet[symbol][0] in set: newStateSet[symbol] = set
    
    # VUELVE TRUE LAS KEY INITIAL Y FINAL DEL DFA MINIMIZADO EN CASO DE SER VERDADERAS
    for newStateSet in newAutomata:
        if initial in newStateSet['Set']: newStateSet['Initial'] = True
        for state in finalStates:
            if state in newStateSet['Set']: newStateSet['Final'] = True

    # CREA Y COMPLETA EL NUEVO ARCHIVO .TXT
    newFile = open(newFileName, 'w')           
    x = 0
    while x < 3:
        if x == 0:
            newFile.write('Estados\n')
            for newStateSet in newAutomata: writeSet(newStateSet, 'Set', True)
            x = 1
        elif x == 1 :
            newFile.write('Alfabeto\n')
            for symbol in alphabet: newFile.write(f'{symbol}\n')
            x = 2
        elif(x == 2):
            newFile.write('Transiciones\n')
            for newStateSet in newAutomata:
                for symbol in alphabet:
                    writeSet(newStateSet, 'Set', False)
                    newFile.write(f' {symbol} -> ')
                    writeSet(newStateSet, symbol, False)
                    newFile.write('\n')
            x = 3

    newFile.close() 


# MENÚ
attempts = 10
while True:
    try:
        fileName, newFileName = input('\nIngrese nombre del archivo a leer: '), input('Ingrese nombre del archivo a crear: ')
        DFAminimizator(fileName, newFileName)
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