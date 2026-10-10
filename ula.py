"""
ULA — Código-base para o projeto de CPU Simulada
AOC 2026.2

Todas as operações estão implementadas. Entradas e
resultado são limitados a 8 bits com & 0xFF.
"""

def limitar_8bits(valor):
    return valor & 0xFF


def ula(operacao, a, b=0):
    a = limitar_8bits(a)
    b = limitar_8bits(b)

    if operacao == "ADD":
        resultado = a + b

    elif operacao == "SUB":
        resultado = a - b

    elif operacao == "AND":
        resultado = a & b

    elif operacao == "OR":
        resultado = a | b

    elif operacao == "XOR":
        resultado = a ^ b

    else:
        raise ValueError(f"Operação inválida: {operacao}")

    return limitar_8bits(resultado)
