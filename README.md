# CPU Simulada de 8 bits

Trabalho prático de Arquitetura de Computadores (2026.2), Universidade Federal do Ceará, Campus Sobral.
Professor: Wendley S. Silva.

Autoria: [NOME COMPLETO DO(A) ALUNO(A) OU DA DUPLA]

Vídeo de apresentação: [LINK DO VÍDEO]

## 1. Visão geral

Este projeto implementa, em Python, uma CPU didática de 8 bits que integra os conceitos de ULA, registradores, memória, instruções e ciclo de execução. O objetivo não é criar um processador real, mas um modelo executável que permita observar o funcionamento de uma CPU passo a passo: a cada ciclo, o programa mostra o PC, a instrução atual e o conteúdo dos registradores.

## 2. Arquitetura

| Componente | Especificação | Onde está no código |
|------------|---------------|---------------------|
| Tamanho dos dados | 8 bits | função `limitar_8bits` em `ula.py` |
| Registradores | R0, R1, R2 e R3 | dicionário `self.registradores` em `cpu.py` |
| Contador de programa | PC | atributo `self.pc` |
| Memória | 16 posições (0 a 15) | lista `self.memoria` |
| ULA | ADD, SUB, AND, OR e XOR | função `ula` em `ula.py` |
| Execução | Fetch, Decode e Execute | métodos `ciclo` e `executar_instrucao` |
| Estado da CPU | em execução ou parada | atributo `self.halted` |

Visão conceitual:

```
      MEMÓRIA (16 x 8 bits)                 CPU
    +----------------------+      +---------------------------+
    | [00] instrução       |      |  Unidade de Controle      |
    | [01] instrução       |<---->|  (ciclo, executar_instr.) |
    | ...                  |      |                           |
    | [14] dado            |      |  R0   R1   R2   R3   PC   |
    | [15] dado            |      |                           |
    +----------------------+      |  ULA: ADD SUB AND OR XOR  |
                                  +---------------------------+
```

## 3. Representação dos dados

Todos os valores de registradores e da ULA ficam entre 0 e 255. A máscara `valor & 0xFF` mantém apenas os 8 bits menos significativos, o que reproduz o comportamento de um circuito de 8 bits:

Estouro na soma: 200 + 100 = 300, que vira 44.

Resultado negativo na subtração: 5 - 8 = -3, que vira 253 (complemento de dois em 8 bits).

Cada posição da memória guarda uma instrução (como texto, por exemplo `"ADD R0, R1"`) ou um valor inteiro gravado por `STORE`. Por isso, os dados são gravados em posições depois do código do programa, que o PC nunca alcança, pois o `HALT` encerra antes.

## 4. Conjunto de instruções

| Instrução | Exemplo | Efeito | PC depois |
|-----------|---------|--------|-----------|
| LOAD | `LOAD R0, 5` | R0 recebe o valor 5 (limitado a 8 bits) | PC + 1 |
| STORE | `STORE R0, 15` | MEM[15] recebe o conteúdo de R0 | PC + 1 |
| ADD | `ADD R0, R1` | R0 = R0 + R1 | PC + 1 |
| SUB | `SUB R0, R1` | R0 = R0 - R1 | PC + 1 |
| AND | `AND R0, R1` | R0 = R0 AND R1 | PC + 1 |
| OR | `OR R0, R1` | R0 = R0 OR R1 | PC + 1 |
| XOR | `XOR R0, R1` | R0 = R0 XOR R1 | PC + 1 |
| JMP | `JMP 8` | PC recebe 8 | endereço informado |
| HALT | `HALT` | encerra a execução (`halted` vira verdadeiro) | não avança |

Nas instruções da ULA, o primeiro registrador é origem e destino, e o segundo é apenas origem.

## 5. Ciclo Fetch, Decode e Execute

Cada chamada de `ciclo()` executa as três etapas:

FETCH: lê `memoria[pc]`. Antes da leitura, a CPU confere se o PC está dentro da memória e, depois dela, se a posição contém uma instrução (texto) e não um dado.

DECODE: `executar_instrucao` separa o texto da instrução em partes e identifica a operação e os operandos.

EXECUTE: o ramo correspondente à operação atualiza registradores, memória ou PC. Em seguida, `mostrar_estado()` imprime os registradores.

Exemplo de um ciclo na saída (ADD com R0 = 200 e R1 = 100):

```
--------------------------------
FETCH
PC: 2
Instrução: ADD R0, R1
DECODE + EXECUTE
Registradores:
  R0 = 2C (44)
  R1 = 64 (100)
  R2 = 00 (0)
  R3 = 00 (0)
```

## 6. Estrutura dos arquivos

```
.
├── cpu.py       classe CPU: registradores, memória, PC, ciclo e instruções
├── ula.py       limitar_8bits e a função ula (ADD, SUB, AND, OR, XOR)
├── main.py      programa de demonstração e execução (completa ou passo a passo)
├── testes.py    testes automáticos
└── README.md    esta documentação
```

## 7. Como executar

Requisito: Python 3.6 ou superior. Não há dependências externas.

Demonstração:

```
python main.py
```

O programa pergunta "Executar passo a passo? (s/n)". Respondendo `s`, a CPU executa um ciclo por vez e espera um Enter entre eles. Respondendo `n`, executa tudo de uma vez. Nos dois casos, o resultado final mostra o PC, os registradores e as posições de memória usadas.

Testes automáticos:

```
python testes.py
```

Cada teste imprime `[OK]` ao passar. Se algum falhar, o Python mostra o `AssertionError` com o caso responsável.

## 8. Programa de demonstração

O programa do `main.py` usa as nove instruções e os quatro registradores. As posições 0 a 13 guardam o código e as posições 14 e 15 recebem os dados gravados por `STORE`.

```
[00] LOAD R0, 200
[01] LOAD R1, 100
[02] ADD R0, R1        estouro de 8 bits: 300 vira 44
[03] SUB R0, R1        44 - 100 negativo: vira 200
[04] JMP 6             pula a posição 5
[05] LOAD R0, 99       nunca é executado
[06] LOAD R2, 12
[07] LOAD R3, 10
[08] AND R2, R3        12 AND 10 = 8
[09] XOR R0, R3        200 XOR 10 = 194
[10] OR R1, R2         100 OR 8 = 108
[11] STORE R2, 14      MEM[14] = 8
[12] STORE R0, 15      MEM[15] = 194
[13] HALT
```

Evolução do PC e dos registradores:

| PC | Instrução | R0 | R1 | R2 | R3 | Memória |
|----|-----------|----|----|----|----|---------|
| 0 | LOAD R0, 200 | 200 | 0 | 0 | 0 | |
| 1 | LOAD R1, 100 | 200 | 100 | 0 | 0 | |
| 2 | ADD R0, R1 | 44 | 100 | 0 | 0 | |
| 3 | SUB R0, R1 | 200 | 100 | 0 | 0 | |
| 4 | JMP 6 | 200 | 100 | 0 | 0 | |
| 6 | LOAD R2, 12 | 200 | 100 | 12 | 0 | |
| 7 | LOAD R3, 10 | 200 | 100 | 12 | 10 | |
| 8 | AND R2, R3 | 200 | 100 | 8 | 10 | |
| 9 | XOR R0, R3 | 194 | 100 | 8 | 10 | |
| 10 | OR R1, R2 | 194 | 108 | 8 | 10 | |
| 11 | STORE R2, 14 | 194 | 108 | 8 | 10 | MEM[14] = 8 |
| 12 | STORE R0, 15 | 194 | 108 | 8 | 10 | MEM[15] = 194 |
| 13 | HALT | 194 | 108 | 8 | 10 | |

Resultado final esperado: R0 = 194, R1 = 108, R2 = 8, R3 = 10, MEM[14] = 8, MEM[15] = 194 e PC = 13.

O `LOAD R0, 99` da posição 5 serve como prova do `JMP`: se ele fosse executado, o XOR daria 105 em vez de 194.

O programa de exemplo do enunciado (`LOAD R0, 5`, `LOAD R1, 8`, `ADD R0, R1`, `STORE R0, 15`, `HALT`) também é verificado nos testes e termina com MEM[15] = 13.

## 9. Testes

| Teste | O que verifica |
|-------|----------------|
| `teste_load` | LOAD coloca o valor no registrador |
| `teste_jmp` | JMP altera o PC e pula instruções |
| `teste_halt` | HALT interrompe a execução |
| `teste_ula` | operações da ULA, estouro de 8 bits e operação inválida |
| `teste_store` | STORE grava na memória, não altera o registrador e rejeita endereço fora de 0 a 15 |
| `teste_registradores` | estado inicial, independência dos quatro registradores, LOAD em 8 bits e ADD, SUB, AND, OR e XOR executados na CPU |
| `teste_pc` | PC avança a cada instrução, HALT o mantém parado e JMP o altera |
| `teste_fetch` | erro claro para PC fora da memória e para posição sem instrução |
| `teste_programa_exemplo` | programa do enunciado termina com MEM[15] = 13 |
| `teste_programa_proprio` | programa de demonstração termina com o estado esperado |

## 10. Tratamento de erros

| Situação | Comportamento |
|----------|---------------|
| Instrução desconhecida | `ValueError` |
| Operação inválida na ULA | `ValueError` |
| `JMP` para endereço fora de 0 a 15 | `ValueError` |
| `STORE` em endereço fora de 0 a 15 | `ValueError` |
| PC fora da memória | `RuntimeError` no FETCH |
| Posição sem instrução (dado ou zero) | `RuntimeError` no FETCH |
| Programa sem `HALT` ou com laço infinito | `RuntimeError` ao atingir o limite de 100 ciclos |

## 11. Decisões e limitações

As instruções são guardadas como texto na memória, o que simplifica o decode e deixa a execução fácil de acompanhar, em vez de usar uma codificação binária.

A CPU não possui flags (como carry ou zero) nem instruções de desvio condicional, pois o conjunto mínimo do enunciado não os inclui.

Os nomes de registradores não são validados: usar um nome inexistente (por exemplo `R5`) gera um erro do Python.

`STORE` em uma posição de código sobrescreve a instrução. Por isso o programa de demonstração grava os dados nas posições 14 e 15, depois do `HALT`.