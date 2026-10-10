# CPU Simulada — Código-base
## AOC 2026.2

### 1. Objetivo

Este pacote contém o código-base para o projeto de CPU Simulada.

A CPU possui:

- dados de 8 bits;
- quatro registradores: R0, R1, R2 e R3;
- memória com 16 posições;
- PC (Program Counter);
- ULA;
- ciclo Fetch → Decode → Execute.

### 2. Arquivos

- `ula.py` — ULA e operações aritméticas/lógicas.
- `cpu.py` — estrutura principal da CPU.
- `main.py` — programa de demonstração.
- `testes.py` — testes das partes já implementadas.

### 3. O que já está implementado

No código-base, estão implementados:

- registradores;
- memória;
- PC;
- limitação para 8 bits;
- `LOAD`;
- `JMP`;
- `HALT`;
- estrutura do ciclo Fetch → Decode → Execute.

### 4. O que deve ser implementado pela dupla

Os alunos deverão completar:

- `STORE`;
- `ADD`;
- `SUB`;
- `AND`;
- `OR`;
- `XOR`;
- operações da ULA em `ula.py`;
- testes adicionais.

### 5. Como executar

No terminal, dentro da pasta:

```bash
python main.py
```

Para executar os testes:

```bash
python testes.py
```

### 6. Exemplo

O `main.py` contém:

```text
0: LOAD R0, 5
1: JMP 4
2: LOAD R0, 99
3: HALT
4: LOAD R1, 8
5: HALT
```

A instrução `JMP 4` faz a CPU saltar da posição 1 para a posição 4.

Portanto:

```text
R0 = 5
R1 = 8
```

A instrução `LOAD R0, 99` não será executada.

### 7. Regras

Não alterar:

- os nomes dos arquivos;
- a assinatura da função `ula()`;
- a estrutura dos registradores;
- o tamanho da memória;
- a representação de 8 bits.

O grupo pode acrescentar funções auxiliares e melhorar a visualização, desde que preserve a interface definida pelo professor.
