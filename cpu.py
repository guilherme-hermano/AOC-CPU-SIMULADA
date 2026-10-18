"""
CPU SIMULADA — Código-base
AOC 2026.2

CPU de 8 bits:
- 4 registradores: R0, R1, R2, R3
- memória com 16 posições
- PC (Program Counter)
- ULA
- instruções LOAD, STORE, ADD, SUB, AND, OR, XOR, JMP e HALT

Todas as instruções estão implementadas. O FETCH valida o PC e o
conteúdo da posição lida antes de executar.
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

        # Estado da CPU (vira True quando o HALT é executado)
        self.halted = False

    def executar_instrucao(self, instrucao):

        # Exemplo:
        # "LOAD R0, 5"
        # "ADD R0, R1"
        # "JMP 4"

        # Remove as vírgulas e separa o texto em partes:
        # "ADD R0, R1" vira ["ADD", "R0", "R1"]
        partes = instrucao.replace(",", "").split()

        operacao = partes[0]

        # Convenção do PC: cada instrução avança o PC em 1,
        # exceto o JMP (define o PC) e o HALT (não o altera).

        # ==============================================
        # LOAD
        # ==============================================
        # LOAD R0, 5
        # R0 <- 5

        if operacao == "LOAD":
            registrador = partes[1]

            # Sem esta validação, escrever em um nome inexistente
            # criaria um novo registrador no dicionário
            if registrador not in self.registradores:
                raise ValueError(f"Registrador inválido: {registrador}")

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

            # Grava um inteiro: o endereço deve ficar fora da região de código
            self.memoria[endereco] = self.registradores[registrador]
            self.pc += 1

        # ==============================================
        # ADD
        # ==============================================
        # ADD R0, R1
        # R0 <- R0 + R1

        elif operacao == "ADD":
            # O primeiro registrador é origem e destino; o segundo é só origem.
            # SUB, AND, OR e XOR seguem o mesmo molde.
            registrador_1 = partes[1]
            registrador_2 = partes[2]

            # A ULA já limita o resultado a 8 bits
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

            # Não há pc += 1: o salto define diretamente o próximo PC
            self.pc = endereco

        # ==============================================
        # HALT
        # ==============================================

        elif operacao == "HALT":

            # Só liga a flag; o PC não avança e continua na posição do HALT
            self.halted = True

        else:

            raise ValueError(f"Instrução desconhecida: {operacao}")

    def ciclo(self):

        if self.halted:
            return

        # ==============================================
        # FETCH
        # ==============================================

        # Valida o PC antes de ler, para não gerar IndexError
        if self.pc < 0 or self.pc >= len(self.memoria):
            raise RuntimeError(f"PC fora da memória: {self.pc}")

        instrucao = self.memoria[self.pc]

        # Instruções são texto; um inteiro na posição é um dado (ou vazio)
        if not isinstance(instrucao, str):
            raise RuntimeError(
                f"Posição {self.pc} não contém uma instrução: {instrucao}"
            )

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

            # Proteção contra laço infinito (por exemplo, JMP para si mesmo)
            if ciclos >= max_ciclos:
                raise RuntimeError(
                    "Número máximo de ciclos atingido. "
                    "Verifique se existe um loop infinito."
                )

            self.ciclo()
            ciclos += 1

    def mostrar_estado(self):

        print("Registradores:")

        # {valor:02X}: hexadecimal com 2 dígitos; entre parênteses, o decimal
        for nome, valor in self.registradores.items():
            print(f"  {nome} = {valor:02X} ({valor})")