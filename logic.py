import random

simbolo_contar = {
    "symbol_3bar": 2,       
    "symbol_bar": 5,        
    "symbol_bell": 8,      
    "symbol_cherry": 22, 
    "symbol_grape": 17,     
    "symbol_seven": 12,
    "symbol_watermelon": 14        
}

simbolo_valor = {
    "symbol_apple": 2,       
    "symbol_bar": 5,        
    "symbol_bell": 8,      
    "symbol_cherry": 22, 
    "symbol_grape": 17,     
    "symbol_seven": 12,
    "symbol_watermelon": 14      
}

def obtener_simbolo():
    total = sum(simbolo_contar.values())
    rand = random.uniform(0, total)
    upto = 0
    for simbolo, prob in simbolo_contar.items():
        if upto + prob >= rand:
            return simbolo
        upto += prob
    assert False, "No debería llegar aquí"

def ganador(linea, apuesta, valores):
    ganancias = 0
    repetidos = 0
    bar = 0

    for i in range(len(linea)):
        simbolo = linea[0]
        aux_simbolo = linea[i]
        if simbolo == aux_simbolo and simbolo != "symbol_bar":
            repetidos += 1
        else:
            if aux_simbolo == "symbol_bar":
                bar += 1

    if repetidos == 3:
        ganancias = valores[simbolo] * apuesta
    if bar == 3:
        ganancias = valores[simbolo] * apuesta
    if bar == 2:
        ganancias = 5 * apuesta
    if bar == 1:
        ganancias = 2 * apuesta

    return ganancias

def girar(fila):
    todos_simbolos = []
    for simbolo, cantidad in simbolo_contar.items():
        for _ in range(cantidad):
            todos_simbolos.append(simbolo)

    resultado = []
    cambiar_simbolos = []

    for _ in range(fila):
        valor = random.choice(todos_simbolos)
        resultado.append(valor)

    while True:
        valor1 = random.choice(todos_simbolos)
        valor2 = random.choice(todos_simbolos)
        valor3 = random.choice(todos_simbolos)
        if (valor1 != "symbol_bar" and valor2 != "symbol_bar" and valor3 != "symbol_bar"):
            if (valor1 != valor2 and valor1 != valor3 and valor2 != valor3):
                cambiar_simbolos = [valor1, valor2, valor3]
                break

    return resultado, cambiar_simbolos