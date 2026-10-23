from datetime import datetime
from typing import List, Optional
from abc import ABC, abstractmethod

class Pessoa(ABC):
    def __init__(self, nome: str, cpf: str, idade: int):
        self.nome = nome
        self._cpf = cpf
        self.idade = idade

    def get_cpf(self) -> str:
        pass


class Medico(Pessoa):
    def __init__(self, nome: str, cpf: str, idade: int, crm: str, espec: str):
        super().__init__(nome, cpf, idade)
        self._crm = crm
        self.espec = espec

    def atender(self):
        pass


class Consulta:
    def __init__(self, data_hora: datetime, medico: Medico, diagnostico: str, receita: str):
        self._data_hora = data_hora
        self._medico = medico
        self._diagnostico = diagnostico
        self._receita = receita

    def exibir_resumo(self):
        pass


class Prontuario:
    def __init__(self):
        self._historicoConsulta: List[Consulta] = []

    def adicionar_consulta(self, consulta: Consulta):
        pass

    def exibir_historico(self):
        pass


class Triagem:
    def __init__(self, temperatura: float, pressaoSistolica: int, nivel_dor: int, cor_risco: str, peso_prioridade: int):
        self._temperatura = temperatura
        self._pressaoSistolica = pressaoSistolica
        self._nivel_dor = nivel_dor
        self._cor_risco = cor_risco
        self._peso_prioridade = peso_prioridade

    def calcular_risco(self):
        pass


class Paciente(Pessoa, ABC):
    def __init__(self, nome: str, cpf: str, idade: int, sintomas: str, triagem: Optional[Triagem] = None):
        super().__init__(nome, cpf, idade)
        self._sintomas = sintomas
        self._triagem = triagem
        self._prontuario = Prontuario()
    
    @abstractmethod
    def gerar_conta(self):
        pass


class PacienteParticular(Paciente):
    def __init__(self, nome: str,
    cpf: str,
    idade: int, sintomas: str, valor_consulta: float, eh_retorno: bool, triagem: Optional[Triagem] = None):
        super().__init__(nome, cpf, idade, sintomas, triagem)
        self._valor_consulta = valor_consulta
        self._eh_retorno = eh_retorno

    def gerar_conta(self):
        pass


class PacienteConvenio(Paciente):
    def __init__(self, nome: str,
    cpf: str, idade: int, sintomas: str, nomePlano: str, numeroCarteirinha: str, triagem: Optional[Triagem] = None):
        super().__init__(nome, cpf, idade, sintomas, triagem)
        self._nomePlano = nomePlano
        self._numeroCarteirinha = numeroCarteirinha

    def gerar_conta(self):
        pass
    