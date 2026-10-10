"""
TESTES-BASE
AOC 2026.2

Os testes abaixo verificam apenas as partes já fornecidas
no código-base: LOAD, JMP e HALT.

Depois de implementar STORE e as operações da ULA,
os alunos deverão ampliar este arquivo.
"""

from cpu import CPU
from ula import ula, limitar_8bits

def teste_load():
    cpu = CPU()

    cpu.memoria[0] = "LOAD R0, 25"
    cpu.memoria[1] = "HALT"

    cpu.executar()

    assert cpu.registradores["R0"] == 25

    print("[OK] LOAD")


def teste_jmp():
    cpu = CPU()

    cpu.memoria[0] = "LOAD R0, 10"
    cpu.memoria[1] = "JMP 4"
    cpu.memoria[2] = "LOAD R0, 99"
    cpu.memoria[3] = "HALT"
    cpu.memoria[4] = "LOAD R1, 20"
    cpu.memoria[5] = "HALT"

    cpu.executar()

    assert cpu.registradores["R0"] == 10
    assert cpu.registradores["R1"] == 20

    print("[OK] JMP")


def teste_halt():
    cpu = CPU()

    cpu.memoria[0] = "HALT"

    cpu.executar()

    assert cpu.halted is True

    print("[OK] HALT")

def teste_ula():
    assert ula("ADD", 5, 8) == 13
    assert ula("ADD", 200, 100) == 44 
    assert ula("ADD", 255, 1) == 0 

    assert ula("SUB", 8, 5) == 3
    assert ula("SUB", 5, 8) == 253     
    assert ula("SUB", 0, 1) == 255   

    assert ula("AND", 12, 10) == 8        
    assert ula("OR", 12, 10) == 14        
    assert ula("XOR", 12, 10) == 6       
    assert ula("XOR", 173, 173) == 0    
    assert ula("AND", 173, 255) == 173    

    try:
        ula("MUL", 2, 3)
        assert False, "ULA deveria rejeitar a operação MUL"
    except ValueError:
        pass

    print("[OK] ULA")

def teste_store():
    cpu = CPU()

    cpu.memoria[0] = "LOAD R0, 42"
    cpu.memoria[1] = "STORE R0, 15"
    cpu.memoria[2] = "HALT"

    cpu.executar()

    assert cpu.memoria[15] == 42
    assert cpu.registradores["R0"] == 42  

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

    cpu = CPU()

    cpu.memoria[0] = "LOAD R0, 300"
    cpu.memoria[1] = "LOAD R1, -1"
    cpu.memoria[2] = "HALT"

    cpu.executar()

    assert cpu.registradores["R0"] == 44
    assert cpu.registradores["R1"] == 255

    # ADD, SUB, AND, OR e XOR sobre registradores
    # (operação, valor em R0, valor em R1, esperado em R0)
    casos = [
        ("ADD", 5, 8, 13),
        ("ADD", 200, 100, 44),
        ("SUB", 8, 5, 3),
        ("SUB", 5, 8, 253),
        ("AND", 12, 10, 8),        # 1100 & 1010 = 1000
        ("OR", 12, 10, 14),        # 1100 | 1010 = 1110
        ("XOR", 12, 10, 6),        # 1100 ^ 1010 = 0110
    ]

    for operacao, a, b, esperado in casos:
        cpu = CPU()

        cpu.memoria[0] = f"LOAD R0, {a}"
        cpu.memoria[1] = f"LOAD R1, {b}"
        cpu.memoria[2] = f"{operacao} R0, R1"
        cpu.memoria[3] = "HALT"

        cpu.executar()

        descricao = f"{operacao} {a}, {b}"
        assert cpu.registradores["R0"] == esperado, descricao
        assert cpu.registradores["R1"] == b, descricao

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
    cpu = CPU()
    cpu.memoria[0] = "LOAD R0, 1"

    try:
        cpu.executar()
        assert False, "FETCH de um dado deveria falhar"
    except RuntimeError as erro:
        assert "Posição 1" in str(erro)

    print("[OK] FETCH")

def teste_programa_exemplo():
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

    print()
    print("Todos os testes foram aprovados.")
