# Sistema de Triagem e Gestão Hospitalar

Trabalho prático desenvolvido para a disciplina de **Programação Orientada a Objetos (POO)** dos cursos de **Ciência da Computação** e **Sistemas de Informação** da **Universidade Católica de Santos (UniSantos)**.

## 📌 Sobre o Projeto

O objetivo deste projeto é modelar e implementar um fluxo simplificado de atendimento hospitalar com fila de prioridades, baseado no Protocolo de Manchester (gravidade clínica) combinado com a legislação de prioridade etária (Estatuto do Idoso).

O sistema conta com:
* Cadastro de pacientes e coleta de sinais vitais (triagem).
* Cálculo automático de risco e classificação em fila prioritária.
* Chamada de pacientes para consulta médica com geração de resumo clínico e financeiro.
* Interface gráfica intuitiva construída com a biblioteca padrão `tkinter`.

## 🏛️ Aplicação dos Pilares de POO

O sistema foi concebido a partir de um diagrama de classes UML estrito, cobrindo os conceitos centrais de POO:

1. **Abstração & Herança:**
   * `Pessoa` é uma classe abstrata base que unifica dados comuns (`nome`, `idade`, `_cpf`).
   * `Medico` e `Paciente` herdam de `Pessoa`.
   * `Paciente` também é abstrata e serve de base para as especializações `PacienteParticular` e `PacienteConvenio`.

2. **Polimorfismo:**
   * O método abstrato `gerar_conta()` é definido em `Paciente` e implementado de formas diferentes:
     * Em `PacienteParticular`: calcula o custo conforme o valor da consulta e regras de retorno.
     * Em `PacienteConvenio`: fatura zero diretamente ao paciente (faturamento via operadora).

3. **Encapsulamento:**
   * Atributos sensíveis e de controle interno (como `_cpf`, `_crm`, `_cor_risco`, `_fila`) utilizam visibilidade protegida/privada, sendo acessados e modificados por métodos específicos de negócio (`get_cpf()`, `atender()`, `exibir_triagem()`).

4. **Associação e Agregação:**
   * `Consulta` associa instâncias de `Medico`, `Paciente` e `Triagem`.
   * `FilaConsultas` agrega múltiplos objetos do tipo `ItemFila`.

## ⚖️ Critérios de Prioridade da Fila

A ordenação da fila não é estritamente por ordem de chegada (FIFO), mas sim por uma tupla de ordenação `(peso_risco, peso_idade, ordem_chegada)`:

1. **Nível Clínico (Triagem):**
   * **Vermelho (Emergência - Peso 1):** Temperatura $\ge 39^\circ\text{C}$, Pressão sistólica $\ge 180\text{ mmHg}$ ou Dor $\ge 8$.
   * **Amarelo (Urgência - Peso 2):** Temperatura $\ge 38^\circ\text{C}$, Pressão sistólica $\ge 140\text{ mmHg}$ ou Dor $\ge 5$.
   * **Verde (Pouco Urgente - Peso 3):** Demais casos.

2. **Faixa Etária (Desempate 1):**
   * 80+ anos (Super Idoso) $\rightarrow$ Peso 1
   * 60+ anos (Idoso) $\rightarrow$ Peso 2
   * 1 a 6 anos (Criança) $\rightarrow$ Peso 3
   * Adultos / Geral $\rightarrow$ Peso 4

3. **Ordem de Chegada (Desempate 2):**
   * Mantém a justiça cronológica em caso de mesmo risco e mesma prioridade de idade.

## 📁 Estrutura de Arquivos

```
├── classes.py      # Modelagem das classes, regras de negócio e fila
├── main.py         # Interface gráfica (Tkinter) e validações de entrada (CPF)
├── UML.png         # Diagrama de classes UML do sistema
└── README.md       # Documentação do projeto
```

## 🚀 Como Executar

### Pré-requisitos
* Python 3.10 ou superior instalado.
* Nenhuma dependência externa é necessária (utiliza apenas bibliotecas nativas: `tkinter`, `datetime`, `re`, `abc`).

### Execução
No terminal, na pasta raiz do projeto, execute:
```bash
python main.py
```

## 👥 Integrantes / Autores

* **Guilherme Borges da Veiga**
* **Leonardo Silva dos Santos**
* **Miguel Rezende Silva**

* **Curso:** Bacharelado em Ciência da Computação / Bacharelado em Sistemas de Informação
* **Instituição:** Universidade Católica de Santos (UniSantos)
* **Disciplina:** Programação Orientada a Objetos (POO)
* **Ano:** 2026