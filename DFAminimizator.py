import os

# FUNCIÓN QUE LEE EL ARCHIVO DE TEXTO Y ENTREGA UNA LISTA CON EL AUTÓMATA Y EL ALFABETO
def automataTextReader():
    attempts = 10
    while True: # LECTOR DEL ARCHIVO
        try:
            filePath = os.path.join(os.path.dirname(__file__), input('\nFile name: '))
            textFile = open(filePath, 'r')
            break
        except FileNotFoundError:
            print('\nEl archivo no existe en la ruta especificada')
            attempts -= 1
            if(attempts == 0):
                print('\nDemasiados intentos inválidos, se cerrará el programa\n\n***SE CERRÓ EL PROGRAMA***\n')
                exit()
            option = input('\n¿Desea reintentar? (S/N): ')
            while True:
                if option == 'S':
                    break
                elif option == 'N':
                    print('\n***SE CERRÓ EL PROGRAMA***\n')
                    exit()
                else:
                    option = input('\nIntroduzca una opción válida\n\n¿Desea reintentar? (S/N): ')

    automata = [] # LISTA DE DICCIONARIOS QUE REPRESENTAN AL AUTÓMATA, CADA DICCIONARIO REPRESENTA UN ESTADO
    alphabet = [] # LISTA CON SÍMBOLOS DEL ALFABETO
    step = None
    for row in textFile: # CREADOR DEL AUTÓMATA Y EL ALFABETO
        if(row == 'Estados\n'):
            step = 0
        elif(row == 'Alfabeto\n'):
            step = 1
        elif(row == 'Transiciones\n'):
            step = 2

        # SE CREAN LOS DICCIONARIOS PERTENECIENTES A CADA ESTADO
        elif(step == 0 and row != '\n'):
            state = {'Name': row.strip('\n').strip('{>*}'), 'Initial': 0, 'Final': 0, 'epsilon': []}
            if(row[0] == '>'):
                state['Initial'] = 1
            if(row[0] == '*' or row[1] == '*'):
                state['Final'] = 1
            automata.append(state)

        # AGREGA LOS SÍMBOLOS DEL ALFABETO COMO UNA KEY CON VALOR UNA LISTA VACIA, YA QUE AÚN NO SE AGREGAN LAS TRANSICIONES
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
    return [automata, alphabet]

# FUNCIÓN RECURSIVA QUE ELIMINA TODOS LOS ESTADOS QUE NO TIENEN SENTIDO DE ESTAR EN EL AUTÓMATA, ESTADO A LOS QUE NO SE PUEDE ACCEDER
def eliminateUselessStates(automata, alphabet):
    newAutomata = []
    uselessStates = []
    for i in automata:
        useless = None
        if(i['Initial'] == 0):
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
    
# FUNCIÓN RECURSIVA QUE RETORNA UNA LISTA CON LISTAS COMPUESTAS POR CADA POSIBLE PAREJA DE ESTADOS DEL AUTÓMATA, NO IMPORTA EL ORDEN Y NO HAY PAREJAS DE UN MISMO ESTADO
def statesPairSet(automata):
    pairs = []
    def recursive(automata, pairs):
        if len(automata) > 1:
            for i in range(1, len(automata)):
                pair = [automata[0]['Name'], automata[i]['Name']]
                pairs.append(pair)
            automata.pop(0)
            return recursive(automata, pairs)
        else:
            return pairs
    return recursive(automata, pairs)

