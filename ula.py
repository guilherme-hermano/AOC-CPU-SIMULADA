"""
ULA — Código-base para o projeto de CPU Simulada
AOC 2026.2

Os alunos devem implementar as operações marcadas como IMPLEMENTAR.
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
