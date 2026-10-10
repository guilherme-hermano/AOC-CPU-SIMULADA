"""
TESTES-BASE
AOC 2026.2

Os testes abaixo verificam apenas as partes já fornecidas
no código-base: LOAD, JMP e HALT.

Depois de implementar STORE e as operações da ULA,
os alunos deverão ampliar este arquivo.
"""

from cpu import CPU


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


if __name__ == "__main__":

    print("Executando testes-base...")
    print()

    teste_load()
    teste_jmp()
    teste_halt()

    print()
    print("Todos os testes-base foram aprovados.")
