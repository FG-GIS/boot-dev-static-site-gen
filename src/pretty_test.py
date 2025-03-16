def print_test(func, expected, result):
    # Esegui la funzione con i dati in input
    # Se input_data è una tupla o lista, la espande, altrimenti la passa direttamente

    # Stampa i dettagli del test
    print("\n\nFunction: ", func.__name__)
    print("Expected: ", expected)
    print("Result: ", result)