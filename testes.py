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

if __name__ == "__main__":

    print("Executando testes-base...")
    print()

    teste_load()
    teste_jmp()
    teste_halt()
    teste_ula()

    print()
    print("Todos os testes-base foram aprovados.")
