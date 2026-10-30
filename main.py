from classes import *

def menu():
    pacientes: List[Paciente] = []
    medicos: List[Medico] = [
        Medico("Ana Costa", "12345678900", 42, "CRM/SP 123456", "Clínica Geral"),
        Medico("Carlos Andrade", "98765432100", 50, "CRM/SP 654321", "Cardiologia")
    ]
    consultas: List[Consulta] = []

    while True:
        print("\n" + "="*40)
        print("   SISTEMA DE TRIAGEM E CONSULTAS MÉDICAS")
        print("="*40)
        print("1. Cadastrar Paciente")
        print("2. Realizar Triagem e Consulta")
        print("3. Listar Consultas Realizadas")
        print("0. Sair")
        opcao = input("Escolha uma opção: ")

        if opcao == "1":
            print("\n--- CADASTRO DE PACIENTE ---")
            nome = input("Nome do paciente: ")
            cpf = input("CPF: ")
            idade = int(input("Idade: "))
            sintomas = input("Sintomas relatados: ")
            tipo = input("Tipo de paciente (1 - Particular / 2 - Convênio): ")

            if tipo == "1":
                valor = float(input("Valor da consulta (R$): "))
                retorno = input("É consulta de retorno? (s/n): ").strip().lower() == 's'
                p = PacienteParticular(nome, cpf, idade, sintomas, valor, retorno)
            else:
                plano = input("Nome do Plano de Saúde: ")
                carteirinha = input("Número da Carteirinha: ")
                p = PacienteConvenio(nome, cpf, idade, sintomas, plano, carteirinha)

            pacientes.append(p)
            print(f"\n✅ Paciente '{nome}' cadastrado com sucesso!")

        elif opcao == "2":
            if not pacientes:
                print("\n❌ Nenhum paciente cadastrado. Cadastre um paciente primeiro (Opção 1).")
                continue

            print("\n--- SELEÇÃO DE PACIENTE ---")
            for idx, p in enumerate(pacientes):
                print(f"{idx + 1}. {p.nome} (CPF: {p.get_cpf()})")
            idx_p = int(input("Escolha o número do paciente: ")) - 1
            paciente_sel = pacientes[idx_p]

            print("\n--- TRIAGEM MÉDICA ---")
            temp = float(input("Temperatura (°C): "))
            pressao = int(input("Pressão Sistólica (mmHg): "))
            dor = int(input("Nível de dor (0 a 10): "))
            triagem = Triagem(temp, pressao, dor)
            print("Resultado da Triagem: ", end="")
            triagem.exibir_triagem()

            print("\n--- SELEÇÃO DE MÉDICO ---")
            for idx, m in enumerate(medicos):
                print(f"{idx + 1}. Dr(a). {m.nome} ({m.espec})")
            idx_m = int(input("Escolha o número do médico: ")) - 1
            medico_sel = medicos[idx_m]
            medico_sel.atender()

            print("\n--- REGISTRO DA CONSULTA ---")
            diagnostico = input("Diagnóstico médico: ")
            receita = input("Receita/Medicamentos: ")

            consulta = Consulta(
                data_hora=datetime.now(),
                paciente=paciente_sel,
                medico=medico_sel,
                triagem=triagem,
                diagnostico=diagnostico,
                receita=receita
            )
            consultas.append(consulta)
            print("\n✅ Consulta registrada com sucesso!")
            consulta.exibir_resumo()

        elif opcao == "3":
            if not consultas:
                print("\n❌ Nenhuma consulta registrada até o momento.")
            else:
                for c in consultas:
                    c.exibir_resumo()

        elif opcao == "0":
            print("\nSaindo do sistema... Até logo!")
            break
        else:
            print("\n❌ Opção inválida. Tente novamente.")

if __name__ == "__main__":
    menu()
