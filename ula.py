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
        # IMPLEMENTAR
        resultado = 0

    elif operacao == "SUB":
        # IMPLEMENTAR
        resultado = 0

    elif operacao == "AND":
        # IMPLEMENTAR
        resultado = 0

    elif operacao == "OR":
        # IMPLEMENTAR
        resultado = 0

    elif operacao == "XOR":
        # IMPLEMENTAR
        resultado = 0

    else:
        raise ValueError(f"Operação inválida: {operacao}")

    return limitar_8bits(resultado)
