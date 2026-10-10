"""
MAIN — Demonstração do código-base
AOC 2026.2

Este programa utiliza somente LOAD, JMP e HALT,
que já estão implementados no código-base.

Depois de implementar as demais instruções, substitua
o programa de teste por um programa mais completo.

------------

VERSÃO FINAL

Este arquivo agora executa um programa próprio que utiliza
as nove instruções da CPU: LOAD, STORE, ADD, SUB, AND, OR,
XOR, JMP e HALT.

Organização da memória (16 posições):
- posições 0 a 12: instruções do programa
- posições 13 a 15: dados gravados pelas instruções STORE

O HALT na posição 12 encerra a execução antes de o PC chegar
à região de dados, então a CPU nunca tenta executar um valor.

O que o programa demonstra:
- ADD com estouro de 8 bits: 200 + 100 = 300, que vira 44
- SUB com resultado negativo: 44 - 100 = -56, que vira 200
- JMP: pula a posição 5, então LOAD R0, 99 nunca é executado
- AND, XOR e OR sobre o mesmo par de valores (R0 e R1)
- STORE gravando o resultado de cada operação lógica

Resultado esperado ao final:
R0 = 100 e R1 = 100
MEM[13] = 64 (AND), MEM[14] = 36 (XOR), MEM[15] = 100 (OR)
PC final = 12, a posição do HALT

O programa pergunta se a execução deve ser passo a passo.
Nesse modo, a CPU espera um Enter entre os ciclos, mostrando
o PC, a instrução atual e os registradores a cada passo.
"""

from cpu import CPU


cpu = CPU()

# ==========================================
# PROGRAMA PRÓPRIO
# ==========================================
#
# Valores de partida: R0 = 200 e R1 = 100.
#
# Posições 0 a 12: código.
# Posições 13 a 15: dados gravados pelo STORE.
#

cpu.memoria[0] = "LOAD R0, 200"     # R0 = 200
cpu.memoria[1] = "LOAD R1, 100"     # R1 = 100
cpu.memoria[2] = "ADD R0, R1"       # 300 estoura: R0 = 44
cpu.memoria[3] = "SUB R0, R1"       # 44 - 100 negativo: R0 = 200
cpu.memoria[4] = "JMP 6"            # pula a posição 5
cpu.memoria[5] = "LOAD R0, 99"      # nunca é executado
cpu.memoria[6] = "AND R0, R1"       # R0 = 64
cpu.memoria[7] = "STORE R0, 13"     # MEM[13] = 64
cpu.memoria[8] = "XOR R0, R1"       # R0 = 36
cpu.memoria[9] = "STORE R0, 14"     # MEM[14] = 36
cpu.memoria[10] = "OR R0, R1"       # R0 = 100
cpu.memoria[11] = "STORE R0, 15"    # MEM[15] = 100
cpu.memoria[12] = "HALT"            # encerra a execução


print("======================================")
print("       CPU SIMULADA — 8 BITS")
print("======================================")

passo_a_passo = input("Executar passo a passo? (s/n): ").strip().lower() == "s"

if passo_a_passo:

    while not cpu.halted:

        cpu.ciclo()

        if not cpu.halted:
            input("\nPressione Enter para o próximo ciclo...")

else:

    cpu.executar()


print()
print("======================================")
print("RESULTADO FINAL")
print("======================================")

print("PC final:", cpu.pc)

cpu.mostrar_estado()

print("Memória:")

for endereco in range(13, 16):
    print(f"  MEM[{endereco}] = {cpu.memoria[endereco]}")