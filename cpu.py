"""
CPU SIMULADA — Código-base
AOC 2026.2

CPU de 8 bits:
- 4 registradores: R0, R1, R2, R3
- memória com 16 posições
- PC (Program Counter)
- ULA
- instruções LOAD, STORE, ADD, SUB, AND, OR, XOR, JMP e HALT

No código-base, LOAD, JMP e HALT já estão implementados.
As demais instruções possuem partes para implementação.
"""

from ula import ula, limitar_8bits


class CPU:

    def __init__(self):
        self.registradores = {
            "R0": 0,
            "R1": 0,
            "R2": 0,
            "R3": 0
        }

        # 16 posições de memória
        self.memoria = [0] * 16

        # Program Counter
        self.pc = 0

        # Estado da CPU
        self.halted = False

        # Métodos para manipular registradores
    def ler_registrador(self, nome):
        if nome not in self.registradores:
            raise ValueError(f"Registrador inválido: {nome}")
        return self.registradores[nome]

    def escrever_registrador(self, nome, valor):
        if nome not in self.registradores:
            raise ValueError(f"Registrador inválido: {nome}")
        self.registradores[nome] = limitar_8bits(valor)

    def executar_instrucao(self, instrucao):

        # Exemplo:
        # "LOAD R0, 5"
        # "ADD R0, R1"
        # "JMP 4"

        partes = instrucao.replace(",", "").split()

        operacao = partes[0]

        # ==============================================
        # LOAD
        # ==============================================
        # LOAD R0, 5
        # R0 <- 5

        if operacao == "LOAD":

            registrador = partes[1]
            valor = int(partes[2])

            self.registradores[registrador] = limitar_8bits(valor)

            self.pc += 1

        # ==============================================
        # STORE
        # ==============================================
        # STORE R0, 15
        # MEM[15] <- R0

        elif operacao == "STORE":
            registrador = partes[1]
            endereco = int(partes[2])

            if endereco < 0 or endereco >= len(self.memoria):
                raise ValueError("Endereço de memória inválido")
            
            self.memoria[endereco] = self.registradores[registrador]
            self.pc += 1

        # ==============================================
        # ADD
        # ==============================================
        # ADD R0, R1
        # R0 <- R0 + R1

        elif operacao == "ADD":
            registrador_1 = partes[1]
            registrador_2 = partes[2]
            ULA_resultado = ula(
                "ADD",
                self.registradores[registrador_1],
                self.registradores[registrador_2]
            )
            self.registradores[registrador_1] = ULA_resultado
            self.pc += 1

        # ==============================================
        # SUB
        # ==============================================

        elif operacao == "SUB":
            registrador_1 = partes[1]
            registrador_2 = partes[2]
            ULA_resultado = ula(
                "SUB",
                self.registradores[registrador_1],
                self.registradores[registrador_2]
            )
            self.registradores[registrador_1] = ULA_resultado
            self.pc += 1
            pass

        # ==============================================
        # AND
        # ==============================================

        elif operacao == "AND":
            registrador_1 = partes[1]
            registrador_2 = partes[2]
            ULA_resultado = ula(
                "AND",
                self.registradores[registrador_1],
                self.registradores[registrador_2]
            )
            self.registradores[registrador_1] = ULA_resultado
            self.pc += 1
            pass

        # ==============================================
        # OR
        # ==============================================

        elif operacao == "OR":
            registrador_1 = partes[1]
            registrador_2 = partes[2]
            ULA_resultado = ula(
                "OR",
                self.registradores[registrador_1],
                self.registradores[registrador_2]
            )
            self.registradores[registrador_1] = ULA_resultado
            self.pc += 1
            pass

        # ==============================================
        # XOR
        # ==============================================

        elif operacao == "XOR":
            registrador_1 = partes[1]
            registrador_2 = partes[2]
            ULA_resultado = ula(
                "XOR",
                self.registradores[registrador_1],
                self.registradores[registrador_2]
            )
            self.registradores[registrador_1] = ULA_resultado
            self.pc += 1
            pass

        # ==============================================
        # JMP
        # ==============================================
        # JMP 8
        # PC <- 8

        elif operacao == "JMP":

            endereco = int(partes[1])

            if endereco < 0 or endereco >= len(self.memoria):
                raise ValueError("Endereço de salto inválido")

            self.pc = endereco

        # ==============================================
        # HALT
        # ==============================================

        elif operacao == "HALT":

            self.halted = True

        else:

            raise ValueError(f"Instrução desconhecida: {operacao}")

    def ciclo(self):

        if self.halted:
            return

        # ==============================================
        # FETCH
        # ==============================================

        instrucao = self.memoria[self.pc]

        print()
        print("--------------------------------")
        print("FETCH")
        print("PC:", self.pc)
        print("Instrução:", instrucao)

        # ==============================================
        # DECODE + EXECUTE
        # ==============================================

        print("DECODE + EXECUTE")

        self.executar_instrucao(instrucao)

        # ==============================================
        # ESTADO
        # ==============================================

        self.mostrar_estado()

    def executar(self, max_ciclos=100):

        ciclos = 0

        while not self.halted:

            if ciclos >= max_ciclos:
                raise RuntimeError(
                    "Número máximo de ciclos atingido. "
                    "Verifique se existe um loop infinito."
                )

            self.ciclo()
            ciclos += 1

    def mostrar_estado(self):

        print("Registradores:")

        for nome, valor in self.registradores.items():
            print(f"  {nome} = {valor:02X} ({valor})")
