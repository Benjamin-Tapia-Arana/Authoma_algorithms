import os

def automathon(fileName):
    attempts = 10
    while True:
        try:
            filePath = os.path.join(os.path.dirname(__file__), fileName)
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
                    fileName = input('\nNombre del archivo CSV: ')
                    break
                elif option == 'N':
                    print('\n***SE CERRÓ EL PROGRAMA***\n')
                    exit()
                else:
                    option = input('\nIntroduzca una opción válida\n\n¿Desea reintentar? (S/N): ')

    automata = []
    step = None
    for row in textFile:
        if(row == 'Estados\n'):
            step = 0
        elif(row == 'Alfabeto\n'):
            step = 1
        elif(row == 'Transiciones\n'):
            step = 2

        # Se crean los diccionarios pertenecientes a cada estado
        elif(step == 0 and row != '\n'):
            state = {'Name': row.strip('\n').strip('{>*}'),
                        'Initial': 0,
                        'Final': 0}
            if(row[0] == '>'):
                state['Initial'] = 1
            if(row[0] == '*' or row[1] == '*'):
                state['Final'] = 1
            automata.append(state)

        # Agrega los símbolos del alfabeto como una key con valor una lista vacía, ya que aún no sen agregan las transiciones
        elif(step == 1 and row != '\n'):
            for dict in automata:
                dict[row.strip('\n')] = []

        # Agrega los estados a los que transiciona cada estado dado cada símbolo
        elif(step == 2 and row != '\n'):
            transition = row.strip('\n').split(' ')
            for i in transition:
                i.strip('{').strip('}s')
            for dict in automata:
                if dict['Name'] == transition[0]:
                    dict[transition[1]].append(transition[3])

    textFile.close()
    return automata

automata = automathon(input('File name: '))
print(automata)