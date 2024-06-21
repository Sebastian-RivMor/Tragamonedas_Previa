import random

# Definir el diccionario de probabilidades de símbolos
simbolo_contar = {
    "symbol_apple": 2,       
    "symbol_bar": 5,        
    "symbol_bell": 8,      
    "symbol_watermelon": 14,    
    "symbol_limon": 17,     
    "symbol_cherry": 22,    
    "symbol_seven": 12      
}
simbolo_valor = {
    "symbol_apple": 1000,       
    "symbol_bar": 500,        
    "symbol_bell": 100,      
    "symbol_watermelon": 75,    
    "symbol_limon": 50,     
    "symbol_cherry": 25,    
    "symbol_seven": 250      
}
# Función para obtener la probabilidad de un símbolo específico
def obtener_probabilidad(simbolo):
    return simbolo_contar.get(simbolo, 0)

# Función para obtener un símbolo basado en sus probabilidades
def obtener_simbolo():
    total = sum(simbolo_contar.values())
    rand = random.uniform(0, total)
    upto = 0
    for simbolo, prob in simbolo_contar.items():
        if upto + prob >= rand:
            return simbolo
        upto += prob
    assert False, "No debería llegar aquí"

# Función para determinar las ganancias basadas en la línea, la apuesta y los valores de símbolos
def ganador(linea, apuesta, valores):
    ganancias = 0
    repetidos = 0
    bar = 0

    simbolo_central = linea[1]  # Suponiendo que el símbolo central está en la posición 1 de la lista

    # Verificar combinaciones ganadoras
    if linea.count(simbolo_central) == 3 and simbolo_central != "symbol_watermelon":
        repetidos = 3
    elif "symbol_watermelon" in linea:
        bar = linea.count("symbol_watermelon")

    if repetidos == 3:
        ganancias = valores[simbolo_central] * apuesta
    elif bar == 3:
        ganancias = valores[simbolo_central] * apuesta
    elif bar == 2:
        ganancias = 5 * apuesta
    elif bar == 1:
        ganancias = 2 * apuesta

    return ganancias


# Función para girar los símbolos y generar combinaciones aleatorias
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
        if (valor1 != "symbol_watermelon" and valor2 != "symbol_watermelon" and valor3 != "symbol_watermelon"):
            if (valor1 != valor2 and valor1 != valor3 and valor2 != valor3):
                cambiar_simbolos = [valor1, valor2, valor3]
                break
        if (valor1 != "symbol_limon" and valor2 != "symbol_limon" and valor3 != "symbol_limon"):
            if (valor1 != valor2 and valor1 != valor3 and valor2 != valor3):
                cambiar_simbolos = [valor1, valor2, valor3]
                break    

    return resultado, cambiar_simbolos
