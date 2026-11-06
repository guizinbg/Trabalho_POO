import tkinter as tk
from tkinter import messagebox
from datetime import datetime
from classes import *
import re

def enfileirar_paciente():
    try:
        nome = ent_nome.get().strip()
        cpf = ent_cpf.get().strip() or "000.000.000-00"
        idade = int(ent_idade.get().strip())
        sintomas = ent_sintomas.get().strip()
        temp = float(ent_temp.get().strip())
        pressao = int(ent_pressao.get().strip())
        dor = int(ent_dor.get().strip())

        if not nome or not sintomas:
            messagebox.showerror("Erro", "Preencha o Nome e os Sintomas!")
            return

        if not validar_cpf(cpf):
            messagebox.showerror("Erro", "CPF inválido!")
            return

        if dor < 0 or dor > 10:
            messagebox.showerror("Erro", "Valor de Dor deve estar entre 0 e 10!")
            return

        paciente = PacienteParticular(nome, cpf, idade, sintomas, 150.0)
        triagem = Triagem(temp, pressao, dor)
        item = fila.enfileirar(paciente, triagem)

        txt_saida.insert(tk.END, f"ENFILEIRADO: {nome} ({idade} anos)\n")
        txt_saida.insert(tk.END, f"Risco: {triagem._cor_risco} | Prioridade: {item.desc_idade}\n")
        txt_saida.insert(tk.END, "-"*50 + "\n")

        ent_nome.delete(0, tk.END)
        ent_cpf.delete(0, tk.END)
        ent_idade.delete(0, tk.END)
        ent_sintomas.delete(0, tk.END)

    except ValueError:
        messagebox.showerror("Erro", "Valores numéricos inválidos para Idade, Temp, Pressão ou Dor!")


def chamar_proximo():
    if fila.esta_vazia():
        txt_saida.insert(tk.END, "Fila vazia!\n" + "-"*50 + "\n")
        return

    item = fila.desenfileirar()
    consulta = Consulta(
        data_hora=datetime.now(),
        paciente=item.paciente,
        medico=medico,
        triagem=item.triagem,
        diagnostico="Atendimento concluído",
        receita="Medicação conforme prescrição"
    )

    txt_saida.insert(tk.END, f"CHAMANDO PRÓXIMO DA FILA:\n")
    txt_saida.insert(tk.END, consulta.obter_resumo_texto())


def exibir_fila():
    txt_saida.insert(tk.END, "FILA DE ESPERA ATUAL:\n")
    if fila.esta_vazia():
        txt_saida.insert(tk.END, "Nenhum paciente na fila.\n")
    else:
        for pos, item in enumerate(fila.obter_lista(), 1):
            txt_saida.insert(
                tk.END,
                f"{pos}º - {item.paciente.nome} ({item.paciente.idade} anos) | "
                f"{item.triagem._cor_risco} | {item.desc_idade}\n"
            )
    txt_saida.insert(tk.END, "-"*50 + "\n")

def validar_cpf(cpf: str) -> bool:
    cpf = re.sub(r'\D', '', cpf)

    if len(cpf) != 11:
        return False

    if cpf == cpf[0] * 11:
        return False

    soma_1 = sum(int(cpf[i]) * (10 - i) for i in range(9))
    resto_1 = soma_1 % 11
    digito_1 = 0 if resto_1 < 2 else 11 - resto_1

    soma_2 = sum(int(cpf[i]) * (11 - i) for i in range(10))
    resto_2 = soma_2 % 11
    digito_2 = 0 if resto_2 < 2 else 11 - resto_2

    return int(cpf[9]) == digito_1 and int(cpf[10]) == digito_2

if __name__ == "__main__":
    fila = FilaConsultas()
    medico = Medico("Ana Costa", "529.982.247-25", 42, "CRM/SP 123456", "Clínica Geral")
    root = tk.Tk()
    root.title("Sistema Hospitalar")
    root.geometry("560x520")

    frame_inputs = tk.Frame(root)
    frame_inputs.pack(pady=10)

    tk.Label(frame_inputs, text="Nome:").grid(row=0, column=0, sticky="e", padx=5, pady=2)
    ent_nome = tk.Entry(frame_inputs, width=20)
    ent_nome.grid(row=0, column=1, padx=5, pady=2)

    tk.Label(frame_inputs, text="CPF:").grid(row=0, column=2, sticky="e", padx=5, pady=2)
    ent_cpf = tk.Entry(frame_inputs, width=15)
    ent_cpf.grid(row=0, column=3, padx=5, pady=2)

    tk.Label(frame_inputs, text="Idade:").grid(row=1, column=0, sticky="e", padx=5, pady=2)
    ent_idade = tk.Entry(frame_inputs, width=8)
    ent_idade.grid(row=1, column=1, sticky="w", padx=5, pady=2)

    tk.Label(frame_inputs, text="Sintomas:").grid(row=1, column=2, sticky="e", padx=5, pady=2)
    ent_sintomas = tk.Entry(frame_inputs, width=20)
    ent_sintomas.grid(row=1, column=3, padx=5, pady=2)

    tk.Label(frame_inputs, text="Temp (°C):").grid(row=2, column=0, sticky="e", padx=5, pady=2)
    ent_temp = tk.Entry(frame_inputs, width=8)
    ent_temp.insert(0, "37.0")
    ent_temp.grid(row=2, column=1, sticky="w", padx=5, pady=2)

    tk.Label(frame_inputs, text="Pressão:").grid(row=2, column=2, sticky="e", padx=5, pady=2)
    ent_pressao = tk.Entry(frame_inputs, width=8)
    ent_pressao.insert(0, "120")
    ent_pressao.grid(row=2, column=3, sticky="w", padx=5, pady=2)

    tk.Label(frame_inputs, text="Dor (0-10):").grid(row=3, column=0, sticky="e", padx=5, pady=2)
    ent_dor = tk.Entry(frame_inputs, width=8)
    ent_dor.insert(0, "2")
    ent_dor.grid(row=3, column=1, sticky="w", padx=5, pady=2)

    frame_btns = tk.Frame(root)
    frame_btns.pack(pady=10)

    tk.Button(frame_btns, text="Cadastrar e Enfileirar", command=enfileirar_paciente).pack(side="left", padx=5)
    tk.Button(frame_btns, text="Chamar Próximo", command=chamar_proximo).pack(side="left", padx=5)
    tk.Button(frame_btns, text="Exibir Fila", command=exibir_fila).pack(side="left", padx=5)

    txt_saida = tk.Text(root, height=14, width=62)
    txt_saida.pack(padx=10, pady=5)

    root.mainloop()
