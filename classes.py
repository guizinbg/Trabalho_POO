from datetime import datetime
from typing import List, Optional
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

    def atender(self):
        print(f"\n👨‍⚕️ Dr(a). {self.nome} ({self.espec}) iniciou o atendimento.")

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
        elif self._temperatura >= 38.0 or self._nivel_dor >= 5:
            self._cor_risco = "Amarelo (Urgência)"
            self._peso_prioridade = 2
        else:
            self._cor_risco = "Verde (Pouco Urgente)"
            self._peso_prioridade = 3

    def exibir_triagem(self):
        print(f"Temp: {self._temperatura}°C | Pressão: {self._pressaoSistolica} mmHg | Dor: {self._nivel_dor}/10 | Classificação: {self._cor_risco}")

class Paciente(Pessoa, ABC):
    def __init__(self, nome: str, cpf: str, idade: int, sintomas: str):
        super().__init__(nome, cpf, idade)
        self._sintomas = sintomas

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
        print(f"💳 Fatura encaminhada ao convênio {self._nomePlano} (Carteirinha: {self._numeroCarteirinha})")
        return 0.0

class Consulta:
    def __init__(self, data_hora: datetime, paciente: Paciente, medico: Medico, triagem: Optional[Triagem] = None, diagnostico: str = "", receita: str = ""):
        self._data_hora = data_hora
        self._paciente = paciente
        self._medico = medico
        self._triagem = triagem
        self._diagnostico = diagnostico
        self._receita = receita

    def exibir_resumo(self):
        print("\n" + "="*45)
        print("           RESUMO DA CONSULTA")
        print("="*45)
        print(f"Data/Hora: {self._data_hora.strftime('%d/%m/%Y %H:%M')}")
        print(f"Paciente: {self._paciente.nome} | CPF: {self._paciente.get_cpf()} | Idade: {self._paciente.idade}")
        print(f"Sintomas: {self._paciente._sintomas}")
        print(f"Médico: Dr(a). {self._medico.nome} ({self._medico.espec}) - CRM: {self._medico._crm}")
        if self._triagem:
            print("Triagem: ", end="")
            self._triagem.exibir_triagem()
        print(f"Diagnóstico: {self._diagnostico}")
        print(f"Receita: {self._receita}")
        
        valor = self._paciente.gerar_conta()
        if valor > 0:
            print(f"Valor a pagar: R$ {valor:.2f}")
        print("="*45 + "\n")