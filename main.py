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
as nove instruções da CPU (LOAD, STORE, ADD, SUB, AND, OR,
XOR, JMP e HALT) e os quatro registradores (R0, R1, R2, R3).

Organização da memória (16 posições):
posições 0 a 13: instruções do programa
posições 14 e 15: dados gravados pelas instruções STORE

O HALT na posição 13 encerra a execução antes de o PC chegar
à região de dados, então a CPU nunca tenta executar um valor.

O que o programa demonstra:
ADD com estouro de 8 bits: 200 + 100 = 300, que vira 44
SUB com resultado negativo: 44 - 100 = -56, que vira 200
JMP: pula a posição 5, então LOAD R0, 99 nunca é executado
AND em R2 e R3: 12 & 10 = 8
XOR em R0 e R3: 200 ^ 10 = 194
OR em R1 e R2: 100 | 8 = 108, que usa o resultado do AND
STORE gravando os resultados do AND e do XOR na memória

Resultado esperado ao final:
R0 = 194, R1 = 108, R2 = 8 e R3 = 10
MEM[14] = 8 (AND) e MEM[15] = 194 (XOR)
PC final = 13, a posição do HALT

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
# Posições 0 a 13: código.
# Posições 14 e 15: dados gravados pelo STORE.
#

cpu.memoria[0] = "LOAD R0, 200"     # R0 = 200
cpu.memoria[1] = "LOAD R1, 100"     # R1 = 100
cpu.memoria[2] = "ADD R0, R1"       # 300 estoura: R0 = 44
cpu.memoria[3] = "SUB R0, R1"       # 44 - 100 negativo: R0 = 200
cpu.memoria[4] = "JMP 6"            # pula a posição 5
cpu.memoria[5] = "LOAD R0, 99"      # nunca é executado
cpu.memoria[6] = "LOAD R2, 12"      # R2 = 12
cpu.memoria[7] = "LOAD R3, 10"      # R3 = 10
cpu.memoria[8] = "AND R2, R3"       # R2 = 8
cpu.memoria[9] = "XOR R0, R3"       # R0 = 194
cpu.memoria[10] = "OR R1, R2"       # R1 = 108
cpu.memoria[11] = "STORE R2, 14"    # MEM[14] = 8
cpu.memoria[12] = "STORE R0, 15"    # MEM[15] = 194
cpu.memoria[13] = "HALT"            # encerra a execução


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

for endereco in range(14, 16):
    print(f"  MEM[{endereco}] = {cpu.memoria[endereco]}")