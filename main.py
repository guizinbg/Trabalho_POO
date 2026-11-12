import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime
from typing import Optional, List
from classes import (
    Medico, Paciente, PacienteParticular, PacienteConvenio,
    Triagem, Consulta, Prontuario, FilaConsultas, ItemFila
)


class AppHospitalTkinter:
    def __init__(self, root: tk.Tk):
        self.root = root
        self.root.title("Sistema Triagem Hospitalar")
        self.root.geometry("950x700")
        self.root.configure(bg="#f4f6f8")

        self.fila_consultas = FilaConsultas()
        self.medicos = [
            Medico("Ana Costa", "12345678900", 42, "CRM/SP 123456", "Clínica Geral"),
            Medico("Carlos Andrade", "98765432100", 50, "CRM/SP 654321", "Cardiologia")
        ]
        self.todos_pacientes: List[Paciente] = []
        self.consultas_realizadas: List[Consulta] = []

        self._construir_interface()

    def _construir_interface(self):
        header = tk.Label(
            self.root,
            text="🏥 Sistema Triagem Hospitalar",
            font=("Helvetica", 14, "bold"),
            bg="#0056b3",
            fg="white",
            pady=10
        )
        header.pack(fill=tk.X)

        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        self.frame_triagem = ttk.Frame(self.notebook)
        self.notebook.add(self.frame_triagem, text="1. Cadastro & Triagem")
        self._criar_aba_triagem()

        self.frame_atendimento = ttk.Frame(self.notebook)
        self.notebook.add(self.frame_atendimento, text="2. Fila de Espera & Consulta")
        self._criar_aba_atendimento()

        self.frame_prontuario = ttk.Frame(self.notebook)
        self.notebook.add(self.frame_prontuario, text="3. Consulta Prontuários/Histórico")
        self._criar_aba_prontuario()

    def _criar_aba_triagem(self):
        form_frame = ttk.LabelFrame(self.frame_triagem, text=" Cadastro do Paciente ")
        form_frame.pack(fill=tk.BOTH, expand=True, padx=15, pady=10)

        for i in range(4):
            form_frame.columnconfigure(i, weight=1)

        self.var_tem_cadastro = tk.BooleanVar(value=False)
        chk_cadastro = ttk.Checkbutton(
            form_frame,
            text="Tem cadastro no sistema?",
            variable=self.var_tem_cadastro,
            command=self._on_toggle_tem_cadastro
        )
        chk_cadastro.grid(row=0, column=0, columnspan=2, sticky=tk.W, padx=10, pady=6)

        ttk.Label(form_frame, text="Selecionar Paciente:").grid(row=0, column=2, sticky=tk.W, padx=10, pady=6)
        self.cb_pacientes_cadastrados = ttk.Combobox(form_frame, state="disabled")
        self.cb_pacientes_cadastrados.grid(row=0, column=3, sticky=tk.EW, padx=10, pady=6)
        self.cb_pacientes_cadastrados.bind("<<ComboboxSelected>>", self._on_selecionar_paciente_cadastrado)

        ttk.Label(form_frame, text="Nome Completo:").grid(row=1, column=0, sticky=tk.W, padx=10, pady=6)
        self.txt_nome = ttk.Entry(form_frame)
        self.txt_nome.grid(row=1, column=1, sticky=tk.EW, padx=10, pady=6)

        ttk.Label(form_frame, text="CPF:").grid(row=1, column=2, sticky=tk.W, padx=10, pady=6)
        self.txt_cpf = ttk.Entry(form_frame)
        self.txt_cpf.grid(row=1, column=3, sticky=tk.EW, padx=10, pady=6)

        ttk.Label(form_frame, text="Idade (anos):").grid(row=2, column=0, sticky=tk.W, padx=10, pady=6)
        self.txt_idade = ttk.Entry(form_frame)
        self.txt_idade.grid(row=2, column=1, sticky=tk.EW, padx=10, pady=6)

        ttk.Label(form_frame, text="Sintomas Principais:").grid(row=2, column=2, sticky=tk.W, padx=10, pady=6)
        self.txt_sintomas = ttk.Entry(form_frame)
        self.txt_sintomas.grid(row=2, column=3, sticky=tk.EW, padx=10, pady=6)

        ttk.Label(form_frame, text="Tipo de Atendimento:").grid(row=3, column=0, sticky=tk.W, padx=10, pady=6)
        self.var_tipo = tk.StringVar(value="Particular")
        cb_tipo = ttk.Combobox(form_frame, textvariable=self.var_tipo, values=["Particular", "Convênio"], state="readonly")
        cb_tipo.grid(row=3, column=1, sticky=tk.EW, padx=10, pady=6)

        ttk.Label(form_frame, text="Valor (R$) / Convênio:").grid(row=3, column=2, sticky=tk.W, padx=10, pady=6)
        self.txt_plano_valor = ttk.Entry(form_frame)
        self.txt_plano_valor.insert(0, "150.0")
        self.txt_plano_valor.grid(row=3, column=3, sticky=tk.EW, padx=10, pady=6)

        ttk.Label(form_frame, text="É Consulta de Retorno?:").grid(row=4, column=0, sticky=tk.W, padx=10, pady=6)
        self.var_retorno = tk.StringVar(value="Não")
        self.cb_retorno = ttk.Combobox(form_frame, textvariable=self.var_retorno, values=["Não", "Sim"], state="readonly")
        self.cb_retorno.grid(row=4, column=1, sticky=tk.EW, padx=10, pady=6)

        triagem_frame = ttk.LabelFrame(self.frame_triagem, text=" Sinais Vitais / Triagem de Manchester ")
        triagem_frame.pack(fill=tk.BOTH, expand=True, padx=15, pady=10)

        for i in range(4):
            triagem_frame.columnconfigure(i, weight=1)

        ttk.Label(triagem_frame, text="🌡️ Temperatura (°C):").grid(row=0, column=0, sticky=tk.W, padx=10, pady=8)
        self.txt_temp = ttk.Entry(triagem_frame)
        self.txt_temp.insert(0, "37.0")
        self.txt_temp.grid(row=0, column=1, sticky=tk.EW, padx=10, pady=8)

        ttk.Label(triagem_frame, text="🩺 Pressão Sistólica (mmHg):").grid(row=0, column=2, sticky=tk.W, padx=10, pady=8)
        self.txt_pressao = ttk.Entry(triagem_frame)
        self.txt_pressao.insert(0, "120")
        self.txt_pressao.grid(row=0, column=3, sticky=tk.EW, padx=10, pady=8)

        ttk.Label(triagem_frame, text="⚡ Nível de Dor (0 a 10):").grid(row=1, column=0, sticky=tk.W, padx=10, pady=8)
        self.txt_dor = ttk.Entry(triagem_frame)
        self.txt_dor.insert(0, "2")
        self.txt_dor.grid(row=1, column=1, sticky=tk.EW, padx=10, pady=8)

        btn_cadastrar = tk.Button(
            triagem_frame,
            text="➕ Realizar Triagem e Enfileirar Paciente",
            font=("Helvetica", 11, "bold"),
            bg="#28a745",
            fg="white",
            pady=8,
            command=self._adicionar_paciente_fila
        )
        btn_cadastrar.grid(row=2, column=0, columnspan=4, pady=12, sticky="ew", padx=10)

    def _on_toggle_tem_cadastro(self):
        if self.var_tem_cadastro.get():
            if not self.todos_pacientes:
                messagebox.showwarning("Aviso", "Nenhum paciente cadastrado anteriormente no sistema.")
                self.var_tem_cadastro.set(False)
                return
            
            lista_opcoes = [f"{p.nome} (CPF: {p.get_cpf()})" for p in self.todos_pacientes]
            self.cb_pacientes_cadastrados.config(state="readonly", values=lista_opcoes)
            if lista_opcoes:
                self.cb_pacientes_cadastrados.current(0)
                self._on_selecionar_paciente_cadastrado(None)
        else:
            self.cb_pacientes_cadastrados.config(state="disabled")
            self.cb_pacientes_cadastrados.set("")
            self.txt_nome.delete(0, tk.END)
            self.txt_cpf.delete(0, tk.END)
            self.txt_idade.delete(0, tk.END)
            self.var_retorno.set("Não")

    def _on_selecionar_paciente_cadastrado(self, event):
        idx = self.cb_pacientes_cadastrados.current()
        if idx >= 0 and idx < len(self.todos_pacientes):
            paciente_sel = self.todos_pacientes[idx]
            self.txt_nome.delete(0, tk.END)
            self.txt_nome.insert(0, paciente_sel.nome)
            self.txt_cpf.delete(0, tk.END)
            self.txt_cpf.insert(0, paciente_sel.get_cpf())
            self.txt_idade.delete(0, tk.END)
            self.txt_idade.insert(0, str(paciente_sel.idade))
            self.var_retorno.set("Sim")

    def _adicionar_paciente_fila(self):
        try:
            nome = self.txt_nome.get().strip()
            cpf = self.txt_cpf.get().strip()
            idade = int(self.txt_idade.get().strip())
            sintomas = self.txt_sintomas.get().strip()
            tipo = self.var_tipo.get()
            eh_retorno = (self.var_retorno.get() == "Sim")

            if not nome or not cpf or not sintomas:
                messagebox.showerror("Erro", "Por favor, preencha todos os campos obrigatórios.")
                return

            paciente_existente = None
            for p in self.todos_pacientes:
                if p.get_cpf() == cpf or p.nome.lower() == nome.lower():
                    paciente_existente = p
                    break

            if paciente_existente:
                paciente = paciente_existente
                paciente._sintomas = sintomas
                paciente._eh_retorno = eh_retorno
            else:
                val_or_plano = self.txt_plano_valor.get().strip()
                if tipo == "Particular":
                    valor = float(val_or_plano) if val_or_plano else 150.0
                    paciente = PacienteParticular(nome, cpf, idade, sintomas, valor, eh_retorno)
                else:
                    paciente = PacienteConvenio(nome, cpf, idade, sintomas, val_or_plano or "Unimed", "123456", eh_retorno)
                self.todos_pacientes.append(paciente)

            temp = float(self.txt_temp.get().strip())
            pressao = int(self.txt_pressao.get().strip())
            dor = int(self.txt_dor.get().strip())
            triagem = Triagem(temp, pressao, dor)

            item = self.fila_consultas.enfileirar(paciente, triagem)
            minutos, est_horario = item.calcular_tempo_estimado(self.fila_consultas.tamanho())

            messagebox.showinfo(
                "Sucesso",
                f"Paciente '{nome}' enfileirado com sucesso!\n"
                f"Classificação: {triagem._cor_risco}\n"
                f"Prioridade Etária: {item.desc_idade}\n"
                f"É Retorno: {'Sim' if eh_retorno else 'Não'}\n"
                f"Horário de Chegada: {item.data_hora_chegada.strftime('%H:%M')}\n"
                f"Estimativa de Atendimento: {est_horario} ({minutos} min de espera)"
            )

            self._limpar_campos_triagem()
            self._atualizar_tabela_fila()
            self.notebook.select(self.frame_atendimento)

        except ValueError:
            messagebox.showerror("Erro", "Valores numéricos inválidos para Idade, Temperatura, Pressão ou Dor.")

    def _limpar_campos_triagem(self):
        self.txt_nome.delete(0, tk.END)
        self.txt_cpf.delete(0, tk.END)
        self.txt_idade.delete(0, tk.END)
        self.txt_sintomas.delete(0, tk.END)
        self.var_tem_cadastro.set(False)
        self.cb_pacientes_cadastrados.config(state="disabled")
        self.cb_pacientes_cadastrados.set("")

    def _criar_aba_atendimento(self):
        lbl_frame_fila = ttk.LabelFrame(self.frame_atendimento, text=" Fila de Espera por Ordem de Prioridade ")
        lbl_frame_fila.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)

        colunas = ("pos", "nome", "idade", "faixa", "risco", "retorno", "chegada", "est_espera", "sintomas")
        self.tree_fila = ttk.Treeview(lbl_frame_fila, columns=colunas, show="headings", height=6)
        self.tree_fila.heading("pos", text="Posição")
        self.tree_fila.heading("nome", text="Paciente")
        self.tree_fila.heading("idade", text="Idade")
        self.tree_fila.heading("faixa", text="Prioridade Etária")
        self.tree_fila.heading("risco", text="Risco Manchester")
        self.tree_fila.heading("retorno", text="Retorno?")
        self.tree_fila.heading("chegada", text="Chegada")
        self.tree_fila.heading("est_espera", text="Est. Atendimento")
        self.tree_fila.heading("sintomas", text="Sintomas")

        self.tree_fila.column("pos", width=55, anchor="center")
        self.tree_fila.column("nome", width=140)
        self.tree_fila.column("idade", width=45, anchor="center")
        self.tree_fila.column("faixa", width=130)
        self.tree_fila.column("risco", width=140)
        self.tree_fila.column("retorno", width=65, anchor="center")
        self.tree_fila.column("chegada", width=65, anchor="center")
        self.tree_fila.column("est_espera", width=110, anchor="center")
        self.tree_fila.column("sintomas", width=150)

        self.tree_fila.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

        btn_ver_prontuario_fila = tk.Button(
            lbl_frame_fila,
            text="📂 Redirecionar ao Prontuário do Paciente Selecionado",
            font=("Helvetica", 9, "bold"),
            bg="#17a2b8",
            fg="white",
            command=self._redirecionar_prontuario_selecionado
        )
        btn_ver_prontuario_fila.pack(anchor="w", padx=5, pady=3)

        call_frame = ttk.LabelFrame(self.frame_atendimento, text=" Atendimento Médico da Consulta ")
        call_frame.pack(fill=tk.X, padx=10, pady=5)

        self.lbl_status_atendimento = tk.Label(
            call_frame,
            text="👤 NENHUM PACIENTE EM CONSULTA NO MOMENTO",
            font=("Helvetica", 10, "bold"),
            bg="#e2e3e5",
            fg="#383d41",
            pady=6
        )
        self.lbl_status_atendimento.grid(row=0, column=0, columnspan=4, sticky="ew", padx=5, pady=5)

        ttk.Label(call_frame, text="Médico Atendente:").grid(row=1, column=0, padx=5, pady=5)
        self.var_medico = tk.StringVar(value=self.medicos[0].nome)
        cb_medico = ttk.Combobox(
            call_frame,
            textvariable=self.var_medico,
            values=[m.nome for m in self.medicos],
            state="readonly",
            width=20
        )
        cb_medico.grid(row=1, column=1, padx=5, pady=5)

        btn_chamar = tk.Button(
            call_frame,
            text="📢 Chamar Próximo Paciente",
            font=("Helvetica", 9, "bold"),
            bg="#007bff",
            fg="white",
            command=self._chamar_proximo_paciente
        )
        btn_chamar.grid(row=1, column=2, padx=10, pady=5)

        ttk.Label(call_frame, text="Diagnóstico:").grid(row=2, column=0, padx=5, pady=5)
        self.txt_diag = ttk.Entry(call_frame, width=30)
        self.txt_diag.grid(row=2, column=1, padx=5, pady=5)

        ttk.Label(call_frame, text="Receita / Relatório:").grid(row=2, column=2, padx=5, pady=5)
        self.txt_receita = ttk.Entry(call_frame, width=30)
        self.txt_receita.grid(row=2, column=3, padx=5, pady=5)

        btn_finalizar = tk.Button(
            call_frame,
            text="✅ Finalizar Consulta e Salvar no Prontuário",
            font=("Helvetica", 9, "bold"),
            bg="#28a745",
            fg="white",
            command=self._finalizar_consulta
        )
        btn_finalizar.grid(row=3, column=0, columnspan=4, pady=8)

        self.txt_resumo = tk.Text(self.frame_atendimento, height=5, bg="#ffffff")
        self.txt_resumo.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)

        self.paciente_em_atendimento: Optional[ItemFila] = None

    def _atualizar_tabela_fila(self):
        for row in self.tree_fila.get_children():
            self.tree_fila.delete(row)

        for idx, item in enumerate(self.fila_consultas.obter_lista(), 1):
            minutos, est_horario = item.calcular_tempo_estimado(idx)
            self.tree_fila.insert(
                "",
                "end",
                values=(
                    f"{idx}º",
                    item.paciente.nome,
                    item.paciente.idade,
                    item.desc_idade,
                    item.triagem._cor_risco,
                    "Sim" if item.paciente.is_retorno() else "Não",
                    item.data_hora_chegada.strftime("%H:%M"),
                    f"{est_horario} ({minutos}m)",
                    item.paciente._sintomas
                )
            )

    def _redirecionar_prontuario_selecionado(self):
        selected = self.tree_fila.selection()
        if not selected:
            messagebox.showwarning("Aviso", "Selecione um paciente na tabela da fila primeiro.")
            return

        values = self.tree_fila.item(selected, "values")
        nome_paciente = values[1]

        self.txt_busca_prontuario.delete(0, tk.END)
        self.txt_busca_prontuario.insert(0, nome_paciente)
        self.notebook.select(self.frame_prontuario)
        self._buscar_prontuario()

    def _chamar_proximo_paciente(self):
        if self.fila_consultas.esta_vazia():
            messagebox.showwarning("Fila Vazia", "Não há nenhum paciente aguardando na fila.")
            return

        self.paciente_em_atendimento = self.fila_consultas.desenfileirar()
        self._atualizar_tabela_fila()

        item = self.paciente_em_atendimento
        medico_nome = self.var_medico.get()
        medico_sel = next(m for m in self.medicos if m.nome == medico_nome)

        self.lbl_status_atendimento.config(
            text=f"👤 EM CONSULTA: {item.paciente.nome} (CPF: {item.paciente.get_cpf()}) | Médico: Dr(a). {medico_sel.nome}",
            bg="#d4edda",
            fg="#155724"
        )

        msg_retorno = " [PACIENTE DE RETORNO]" if item.paciente.is_retorno() else ""
        messagebox.showinfo(
            "Em Atendimento",
            f"Chamando Paciente: {item.paciente.nome}{msg_retorno}\n"
            f"Classificação: {item.triagem._cor_risco}\n"
            f"Sintomas: {item.paciente._sintomas}"
        )

    def _finalizar_consulta(self):
        if not self.paciente_em_atendimento:
            messagebox.showwarning("Aviso", "Clique em 'Chamar Próximo Paciente' antes de finalizar.")
            return

        medico_nome = self.var_medico.get()
        medico_sel = next(m for m in self.medicos if m.nome == medico_nome)

        diagnostico = self.txt_diag.get().strip() or "Consulta de rotina sem alterações"
        receita = self.txt_receita.get().strip() or "Repouso e hidratação"

        consulta = Consulta(
            data_hora=datetime.now(),
            paciente=self.paciente_em_atendimento.paciente,
            medico=medico_sel,
            triagem=self.paciente_em_atendimento.triagem,
            diagnostico=diagnostico,
            receita=receita
        )

        self.paciente_em_atendimento.paciente.prontuario.adicionar_consulta(consulta)
        self.consultas_realizadas.append(consulta)

        self.txt_resumo.delete("1.0", tk.END)
        self.txt_resumo.insert(tk.END, consulta.obter_resumo_texto())

        self.paciente_em_atendimento = None
        self.txt_diag.delete(0, tk.END)
        self.txt_receita.delete(0, tk.END)

        self.lbl_status_atendimento.config(
            text="👤 NENHUM PACIENTE EM CONSULTA NO MOMENTO",
            bg="#e2e3e5",
            fg="#383d41"
        )

        messagebox.showinfo("Sucesso", "Consulta realizada e registrada com sucesso no Prontuário do Paciente!")

    def _criar_aba_prontuario(self):
        busca_frame = ttk.LabelFrame(self.frame_prontuario, text=" Busca e Consulta de Prontuários ")
        busca_frame.pack(fill=tk.X, padx=10, pady=10)

        ttk.Label(busca_frame, text="Nome do Paciente:").grid(row=0, column=0, padx=8, pady=8)
        self.txt_busca_prontuario = ttk.Entry(busca_frame, width=30)
        self.txt_busca_prontuario.grid(row=0, column=1, padx=8, pady=8)

        btn_buscar = tk.Button(
            busca_frame,
            text="🔍 Buscar Prontuário",
            font=("Helvetica", 9, "bold"),
            bg="#007bff",
            fg="white",
            command=self._buscar_prontuario
        )
        btn_buscar.grid(row=0, column=2, padx=8, pady=8)

        btn_listar_todos = tk.Button(
            busca_frame,
            text="📋 Listar Todos os Prontuários",
            font=("Helvetica", 9, "bold"),
            bg="#6c757d",
            fg="white",
            command=self._listar_todos_prontuarios
        )
        btn_listar_todos.grid(row=0, column=3, padx=8, pady=8)

        self.txt_exibicao_prontuario = tk.Text(self.frame_prontuario, bg="#ffffff", font=("Courier", 10))
        self.txt_exibicao_prontuario.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)

    def _buscar_prontuario(self):
        nome_busca = self.txt_busca_prontuario.get().strip().lower()
        if not nome_busca:
            messagebox.showwarning("Aviso", "Digite o nome do paciente para buscar.")
            return

        encontrados = [p for p in self.todos_pacientes if nome_busca in p.nome.lower()]

        self.txt_exibicao_prontuario.delete("1.0", tk.END)
        if not encontrados:
            self.txt_exibicao_prontuario.insert(tk.END, f"Nenhum paciente encontrado com o nome '{nome_busca}'.\n")
        else:
            for p in encontrados:
                self.txt_exibicao_prontuario.insert(tk.END, p.prontuario.exibir_prontuario_texto() + "\n\n")

    def _listar_todos_prontuarios(self):
        self.txt_exibicao_prontuario.delete("1.0", tk.END)
        if not self.todos_pacientes:
            self.txt_exibicao_prontuario.insert(tk.END, "Nenhum paciente cadastrado no sistema até o momento.\n")
        else:
            for p in self.todos_pacientes:
                self.txt_exibicao_prontuario.insert(tk.END, p.prontuario.exibir_prontuario_texto() + "\n\n")


def iniciar_interface():
    root = tk.Tk()
    app = AppHospitalTkinter(root)
    root.mainloop()


if __name__ == "__main__":
    iniciar_interface()
