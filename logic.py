import random #Librería para generar número aleatorios

#Diccionario para establecer la cantidad de los símbolos
simbolo_contar = {
    "symbol_3bar": 2,       
    "symbol_bar": 5,        
    "symbol_bell": 12,      
    "symbol_cherry": 22, 
    "symbol_grape": 17,     
    "symbol_seven": 8,
    "symbol_watermelon": 14        
}

#Diccionario para establecer el valor de los símbolos
simbolo_valor = {
    "symbol_3bar": 1000,
    "symbol_bar": 500,
    "symbol_bell": 100,
    "symbol_cherry": 25, 
    "symbol_grape": 50,
    "symbol_seven": 250,
    "symbol_watermelon": 75
}
#Función que determina si ganamos o perdemos
def ganador(linea, apuesta, valores):
    ganancias = 0
    repetidos = 0
    bar = 0
        #Recorrido de toda la fila
    for i in range(len(linea)):
        simbolo = linea[0]
        aux_simbolo = linea[i]
        #Condición que permite recolectar símbolos que se repiten exceptuando "bar"
        if simbolo == aux_simbolo and simbolo != "symbol_bar":
             #!=bar  ==> para considerar este caso:  bar bar any 
            #(si no hay != bar entonces repetidos = 2 y bar = 0) no tendría ninguna ganancia
            repetidos += 1
        else:
            #Condición que permite recolectar todos los símbolos que sean "bar"
            if aux_simbolo == "symbol_bar":
                bar += 1
    #Condiciones para establecer la ganancia
    if repetidos == 3:
        ganancias = valores[simbolo] * apuesta
    if bar == 3:
        ganancias = valores[simbolo] * apuesta
    if bar == 2:
        ganancias = 5 * apuesta
    if bar == 1:
        ganancias = 2 * apuesta

    return ganancias

#Algoritmo aleatorio: Permite seleccionar 2 combinaciones de 3 símbolos de manera aleatoria
#Siempre me va generar una combinación pérdedora
def girar(fila):
    #Array que almacenerá todas las cantidades de cada símbolo del diccionario simbolo_contar
    todos_simbolos = []
    #Llenado del Array todos_simbolos
    for simbolo, cantidad in simbolo_contar.items():#simbolo: elemento, simbolo_contar: cantidad
        for _ in range(cantidad):
            todos_simbolos.append(simbolo)
    #Selección aleatoria de la combinación
    #Array que puede almacenar la combinación ganadora
    resultado = []
    #Array que almacena la combinación perdedora
    cambiar_simbolos = []
    #Generación de la combinación (Que puede ser la ganadora)
    for _ in range(fila):
        valor = random.choice(todos_simbolos)
        resultado.append(valor)
    #Generar de la combinación (Perdedora)
    while True:
        valor1 = random.choice(todos_simbolos)
        valor2 = random.choice(todos_simbolos)
        valor3 = random.choice(todos_simbolos)
        # No debe generarme el sìmbolo "bar"
        if (valor1 != "symbol_bar" and valor2 != "symbol_bar" and valor3 != "symbol_bar"):
            if (valor1 != valor2 and valor1 != valor3 and valor2 != valor3):
                cambiar_simbolos = [valor1, valor2, valor3]
                break

    return resultado, cambiar_simbolos

