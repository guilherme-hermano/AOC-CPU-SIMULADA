"""
TESTES
AOC 2026.2

Testes automáticos da CPU: instruções,
ULA, registradores, PC, FETCH, programa de exemplo do enunciado e
programa próprio de demonstração.
"""

from cpu import CPU
from ula import ula, limitar_8bits

def teste_load():
    # Testa a instrução LOAD, que carrega um valor imediato em um registrador.
    cpu = CPU()

    cpu.memoria[0] = "LOAD R0, 25"
    cpu.memoria[1] = "HALT"

    cpu.executar()

    assert cpu.registradores["R0"] == 25

    print("[OK] LOAD")


def teste_jmp():
    # Testa a instrução JMP, que altera o PC para um valor imediato.
    cpu = CPU()

    cpu.memoria[0] = "LOAD R0, 10"
    cpu.memoria[1] = "JMP 4"
    cpu.memoria[2] = "LOAD R0, 99"      # pulado pelo JMP
    cpu.memoria[3] = "HALT"
    cpu.memoria[4] = "LOAD R1, 20"
    cpu.memoria[5] = "HALT"

    cpu.executar()

    assert cpu.registradores["R0"] == 10    # continua 10: o LOAD 99 não executou
    assert cpu.registradores["R1"] == 20

    print("[OK] JMP")


def teste_halt():
    # Testa a instrução HALT, que encerra a execução da CPU.
    cpu = CPU()

    cpu.memoria[0] = "HALT"

    cpu.executar()

    assert cpu.halted is True

    print("[OK] HALT")

def teste_ula():
    # Testa a ULA com todas as operações implementadas.

    # ADD: normal e estouro de 8 bits
    assert ula("ADD", 5, 8) == 13
    assert ula("ADD", 200, 100) == 44       # 300 & 0xFF
    assert ula("ADD", 255, 1) == 0          # 256 & 0xFF

    # SUB: normal e resultado negativo (complemento de dois em 8 bits)
    assert ula("SUB", 8, 5) == 3
    assert ula("SUB", 5, 8) == 253          # -3 & 0xFF
    assert ula("SUB", 0, 1) == 255          # -1 & 0xFF

    # AND, OR e XOR: 12 = 1100 e 10 = 1010
    assert ula("AND", 12, 10) == 8          # 1000
    assert ula("OR", 12, 10) == 14          # 1110
    assert ula("XOR", 12, 10) == 6          # 0110
    assert ula("XOR", 173, 173) == 0        # x ^ x = 0
    assert ula("AND", 173, 255) == 173      # 0xFF mantém todos os bits

    # Operação inexistente deve gerar erro
    try:
        ula("MUL", 2, 3)
        assert False, "ULA deveria rejeitar a operação MUL"
    except ValueError:
        pass

    print("[OK] ULA")

def teste_store():
    # Testa a instrução STORE, que grava o valor de um registrador na memória.
    cpu = CPU()

    cpu.memoria[0] = "LOAD R0, 42"
    cpu.memoria[1] = "STORE R0, 15"
    cpu.memoria[2] = "HALT"

    cpu.executar()

    assert cpu.memoria[15] == 42
    assert cpu.registradores["R0"] == 42    # STORE copia: a origem não muda

    # Endereço fora de 0 a 15 deve gerar erro
    cpu = CPU()

    cpu.memoria[0] = "LOAD R0, 1"
    cpu.memoria[1] = "STORE R0, 16"
    cpu.memoria[2] = "HALT"

    try:
        cpu.executar()
        assert False, "STORE em 16 deveria falhar"
    except ValueError:
        pass

    print("[OK] STORE")

def teste_registradores():
    # Testa o acesso aos registradores e a operação de cada um.
    cpu = CPU()

    # Todos zerados inicialmente
    for nome in ("R0", "R1", "R2", "R3"):
        assert cpu.registradores[nome] == 0

    # Um valor diferente em cada registrador, sem interferência entre eles
    cpu.memoria[0] = "LOAD R0, 1"
    cpu.memoria[1] = "LOAD R1, 2"
    cpu.memoria[2] = "LOAD R2, 3"
    cpu.memoria[3] = "LOAD R3, 4"
    cpu.memoria[4] = "HALT"

    cpu.executar()

    assert cpu.registradores == {"R0": 1, "R1": 2, "R2": 3, "R3": 4}

    # LOAD respeita 8 bits
    cpu = CPU()

    cpu.memoria[0] = "LOAD R0, 300"
    cpu.memoria[1] = "LOAD R1, -1"
    cpu.memoria[2] = "HALT"

    cpu.executar()

    assert cpu.registradores["R0"] == 44        # 300 & 0xFF
    assert cpu.registradores["R1"] == 255       # -1 & 0xFF

    # ADD, SUB, AND, OR e XOR sobre registradores
    # (operação, valor em R0, valor em R1, esperado em R0)
    casos = [
        ("ADD", 5, 8, 13),
        ("ADD", 200, 100, 44),     # 300 & 0xFF
        ("SUB", 8, 5, 3),
        ("SUB", 5, 8, 253),        # -3 & 0xFF
        ("AND", 12, 10, 8),        # 1100 & 1010 = 1000
        ("OR", 12, 10, 14),        # 1100 | 1010 = 1110
        ("XOR", 12, 10, 6),        # 1100 ^ 1010 = 0110
    ]

    for operacao, a, b, esperado in casos:
        # Cada caso roda em uma CPU nova
        cpu = CPU()

        cpu.memoria[0] = f"LOAD R0, {a}"
        cpu.memoria[1] = f"LOAD R1, {b}"
        cpu.memoria[2] = f"{operacao} R0, R1"
        cpu.memoria[3] = "HALT"

        cpu.executar()

        # A descrição aparece na mensagem de erro e indica o caso que falhou
        descricao = f"{operacao} {a}, {b}"
        assert cpu.registradores["R0"] == esperado, descricao
        assert cpu.registradores["R1"] == b, descricao    # a origem não muda

    print("[OK] Registradores")

def teste_pc():
    # Testa o avanço do PC e o efeito do HALT
    cpu = CPU()

    cpu.memoria[0] = "LOAD R0, 1"
    cpu.memoria[1] = "LOAD R1, 2"
    cpu.memoria[2] = "HALT"

    assert cpu.pc == 0

    cpu.ciclo()
    assert cpu.pc == 1

    cpu.ciclo()
    assert cpu.pc == 2

    cpu.ciclo()                       # executa o HALT
    assert cpu.pc == 2                # HALT não avança o PC
    assert cpu.halted is True

    cpu.ciclo()                       # ciclo após o HALT não faz nada
    assert cpu.pc == 2

    # JMP define o PC diretamente, sem avançar de 1 em 1
    cpu = CPU()

    cpu.memoria[0] = "JMP 5"
    cpu.ciclo()
    assert cpu.pc == 5

    print("[OK] PC")

def teste_fetch():
    # Teste FETCH com PC fora da memória
    cpu = CPU()
    cpu.pc = 16

    try:
        cpu.ciclo()
        assert False, "FETCH com PC 16 deveria falhar"
    except RuntimeError as erro:
        assert "PC fora da memória" in str(erro)

    # Posição sem instrução (programa sem HALT)
    # Depois do LOAD, o PC vai para 1, que contém o inteiro 0 (um dado)
    cpu = CPU()
    cpu.memoria[0] = "LOAD R0, 1"

    try:
        cpu.executar()
        assert False, "FETCH de um dado deveria falhar"
    except RuntimeError as erro:
        # Confere a mensagem para garantir que o erro veio do FETCH
        # e não do limite de ciclos, que também é RuntimeError
        assert "Posição 1" in str(erro)

    print("[OK] FETCH")

def teste_programa_exemplo():
    # Programa de exemplo do enunciado
    cpu = CPU()

    cpu.memoria[0] = "LOAD R0, 5"
    cpu.memoria[1] = "LOAD R1, 8"
    cpu.memoria[2] = "ADD R0, R1"
    cpu.memoria[3] = "STORE R0, 15"
    cpu.memoria[4] = "HALT"

    cpu.executar()

    assert cpu.memoria[15] == 13             # resultado esperado pelo PDF
    assert cpu.registradores["R0"] == 13
    assert cpu.registradores["R1"] == 8      # origem não muda
    assert cpu.pc == 4                       # HALT não avança o PC
    assert cpu.halted is True

    print("[OK] Programa de exemplo")

def teste_programa_proprio():
    # Programa próprio de demonstração, com todas as instruções
    cpu = CPU()

    cpu.memoria[0] = "LOAD R0, 200"
    cpu.memoria[1] = "LOAD R1, 100"
    cpu.memoria[2] = "ADD R0, R1"       # 300 estoura: R0 = 44
    cpu.memoria[3] = "SUB R0, R1"       # 44 - 100 negativo: R0 = 200
    cpu.memoria[4] = "JMP 6"            # pula a posição 5
    cpu.memoria[5] = "LOAD R0, 99"      # nunca executa; se executasse, o XOR mudaria
    cpu.memoria[6] = "LOAD R2, 12"
    cpu.memoria[7] = "LOAD R3, 10"
    cpu.memoria[8] = "AND R2, R3"       # R2 = 12 & 10 = 8
    cpu.memoria[9] = "XOR R0, R3"       # R0 = 200 ^ 10 = 194
    cpu.memoria[10] = "OR R1, R2"       # R1 = 100 | 8 = 108 (usa o R2 do AND)
    cpu.memoria[11] = "STORE R2, 14"
    cpu.memoria[12] = "STORE R0, 15"
    cpu.memoria[13] = "HALT"

    cpu.executar()

    assert cpu.registradores == {"R0": 194, "R1": 108, "R2": 8, "R3": 10}
    assert cpu.memoria[14] == 8              # AND
    assert cpu.memoria[15] == 194            # XOR
    assert cpu.pc == 13                      # HALT não avança o PC
    assert cpu.halted is True

    print("[OK] Programa próprio")

if __name__ == "__main__":

    print("Executando testes...")
    print()

    teste_load()
    teste_jmp()
    teste_halt()
    teste_ula()
    teste_store()
    teste_registradores()
    teste_pc()
    teste_fetch()
    teste_programa_exemplo()
    teste_programa_proprio()

    print()
    print("Todos os testes foram aprovados.")