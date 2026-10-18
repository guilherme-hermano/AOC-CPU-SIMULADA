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
        resultado = a + b # Soma simples

    elif operacao == "SUB":
        resultado = a - b # Subtração simples

    elif operacao == "AND":
        resultado = a & b # Operador lógico AND bit a bit

    elif operacao == "OR":
        resultado = a | b # Operador lógico OR bit a bit

    elif operacao == "XOR":
        resultado = a ^ b # Operador lógico XOR bit a bit

    else:
        raise ValueError(f"Operação inválida: {operacao}")

    return limitar_8bits(resultado)
