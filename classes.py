from datetime import datetime
from typing import List, Optional, Tuple
from abc import ABC, abstractmethod


class Pessoa(ABC):
    def __init__(self, nome: str, cpf: str, idade: int):
        self.nome = nome
        self._cpf = cpf
        self.idade = idade

    def get_cpf(self) -> str:
        return self._cpf


class Medico(Pessoa):
    def __init__(self, nome: str, cpf: str, idade: int, crm: str, espec: str):
        super().__init__(nome, cpf, idade)
        self._crm = crm
        self.espec = espec

    def atender(self) -> str:
        return f"Dr(a). {self.nome} ({self.espec}) - CRM: {self._crm}"


class Triagem:
    def __init__(self, temperatura: float, pressaoSistolica: int, nivel_dor: int):
        self._temperatura = temperatura
        self._pressaoSistolica = pressaoSistolica
        self._nivel_dor = nivel_dor
        self._cor_risco = ""
        self._peso_prioridade = 0
        self.calcular_risco()

    def calcular_risco(self):
        if self._temperatura >= 39.0 or self._pressaoSistolica >= 180 or self._nivel_dor >= 8:
            self._cor_risco = "Vermelho (Emergência)"
            self._peso_prioridade = 1
        elif self._temperatura >= 38.0 or self._pressaoSistolica >= 140 or self._nivel_dor >= 5:
            self._cor_risco = "Amarelo (Urgência)"
            self._peso_prioridade = 2
        else:
            self._cor_risco = "Verde (Pouco Urgente)"
            self._peso_prioridade = 3

    def exibir_triagem(self) -> str:
        return f"Temp: {self._temperatura}°C | Pressão: {self._pressaoSistolica} mmHg | Dor: {self._nivel_dor}/10 | Risco: {self._cor_risco}"


class Paciente(Pessoa, ABC):
    def __init__(self, nome: str, cpf: str, idade: int, sintomas: str):
        super().__init__(nome, cpf, idade)
        self._sintomas = sintomas

    def get_prioridade_faixa_etaria(self) -> Tuple[int, str]:
        if self.idade >= 80:
            return (1, "80+ (Super Idoso)")
        elif self.idade >= 60:
            return (2, "Idoso (60+)")
        elif 1 <= self.idade <= 6:
            return (3, "Criança (1 a 6 anos)")
        else:
            return (4, "Geral / Adulto")

    @abstractmethod
    def gerar_conta(self) -> float:
        pass


class PacienteParticular(Paciente):
    def __init__(self, nome: str, cpf: str, idade: int, sintomas: str, valor_consulta: float, eh_retorno: bool = False):
        super().__init__(nome, cpf, idade, sintomas)
        self._valor_consulta = valor_consulta
        self._eh_retorno = eh_retorno

    def gerar_conta(self) -> float:
        if self._eh_retorno:
            return 0.0
        return self._valor_consulta


class PacienteConvenio(Paciente):
    def __init__(self, nome: str, cpf: str, idade: int, sintomas: str, nomePlano: str, numeroCarteirinha: str):
        super().__init__(nome, cpf, idade, sintomas)
        self._nomePlano = nomePlano
        self._numeroCarteirinha = numeroCarteirinha

    def gerar_conta(self) -> float:
        return 0.0


class Consulta:
    def __init__(self, data_hora: datetime, paciente: Paciente, medico: Medico, triagem: Optional[Triagem] = None, diagnostico: str = "", receita: str = ""):
        self._data_hora = data_hora
        self._paciente = paciente
        self._medico = medico
        self._triagem = triagem
        self._diagnostico = diagnostico
        self._receita = receita

    def obter_resumo_texto(self) -> str:
        resumo = "="*40 + "\n"
        resumo += "        RESUMO DA CONSULTA MÉDICA\n"
        resumo += "="*40 + "\n"
        resumo += f"Data/Hora: {self._data_hora.strftime('%d/%m/%Y %H:%M')}\n"
        resumo += f"Paciente: {self._paciente.nome} | CPF: {self._paciente.get_cpf()} | Idade: {self._paciente.idade} anos\n"
        resumo += f"Sintomas: {self._paciente._sintomas}\n"
        resumo += f"Médico: {self._medico.atender()}\n"
        if self._triagem:
            resumo += f"Triagem: {self._triagem.exibir_triagem()}\n"
        resumo += f"Diagnóstico: {self._diagnostico}\n"
        resumo += f"Receita: {self._receita}\n"
        
        valor = self._paciente.gerar_conta()
        if valor > 0:
            resumo += f"Valor a Pagar: R$ {valor:.2f}\n"
        elif isinstance(self._paciente, PacienteConvenio):
            resumo += f"Plano: {self._paciente._nomePlano} (Conveniado)\n"
        else:
            resumo += "Consulta de Retorno (Isento)\n"
        resumo += "="*40 + "\n"
        return resumo


class ItemFila:
    _contador_chegada = 0

    def __init__(self, paciente: Paciente, triagem: Triagem):
        ItemFila._contador_chegada += 1
        self.ordem_chegada = ItemFila._contador_chegada
        self.paciente = paciente
        self.triagem = triagem
        
        peso_idade, self.desc_idade = paciente.get_prioridade_faixa_etaria()
        self.chave_prioridade = (triagem._peso_prioridade, peso_idade, self.ordem_chegada)


class FilaConsultas:
    def __init__(self):
        self._fila: List[ItemFila] = []

    def enfileirar(self, paciente: Paciente, triagem: Triagem) -> ItemFila:
        item = ItemFila(paciente, triagem)
        self._fila.append(item)
        self._ordenar()
        return item

    def _ordenar(self):
        self._fila.sort(key=lambda item: item.chave_prioridade)

    def desenfileirar(self) -> Optional[ItemFila]:
        if not self.esta_vazia():
            return self._fila.pop(0)
        return None

    def esta_vazia(self) -> bool:
        return len(self._fila) == 0

    def obter_lista(self) -> List[ItemFila]:
        return self._fila
