import datetime
import tkinter as Tk
from tkinter import ttk, messagebox, Label, Entry, Button
import os
from model import Aplicacao 
from storage import carregar_aplicacoes, adicionar_aplicacao


def create_main_window():
    """Cria e retorna a janela principal do aplicativo."""
    root = Tk.Tk()
    root.title("Cronograma TH")
    root.geometry("600x700")
    root.configure(bg="#0A0000")

    header_frame = Tk.Frame(root, bg="#0A0000")
    header_frame.pack(fill=Tk.X, padx=10, pady=10)

    user_name = os.getenv("USERNAME", "USUARIO")
    saudacao = Label(header_frame, bg="#0A0000", fg="#FFFFFF", font=("Montserrat", 14), 
                     text=f"Bem-vindo {user_name}!")
    saudacao.pack()

    data_hoje = datetime.datetime.now().strftime("%d/%m/%Y")
    data_label = Label(header_frame, bg="#0A0000", fg="#FFFFFF", font=("Montserrat", 12), 
                       text=f"Data de hoje: {data_hoje}")
    data_label.pack()

    form_frame = Tk.LabelFrame(root, text="Registrar nova aplicação", bg="#0A0000", 
                               fg="#FFFFFF", font=("Montserrat", 12))
    form_frame.pack(fill=Tk.X, padx=10, pady=10)

    Tk.Label(form_frame, text="Data (dd/mm/yyyy):", bg="#0A0000", fg="#FFFFFF", 
             font=("Montserrat", 10)).grid(row=0, column=0, padx=5, pady=5, sticky=Tk.W)
    entry_data = Tk.Entry(form_frame, width=20)
    entry_data.insert(0, data_hoje)
    entry_data.grid(row=0, column=1, sticky=Tk.W, padx=10)

    Tk.Label(form_frame, text="Dosagem (ml):", bg="#0A0000", fg="#FFFFFF").grid(
        row=1, column=0, sticky=Tk.W, pady=5)
    entry_ml = Tk.Entry(form_frame, width=20)
    entry_ml.grid(row=1, column=1, sticky=Tk.W, padx=10)

    Tk.Label(form_frame, text="Lado:", bg="#0A0000", fg="#FFFFFF").grid(
        row=2, column=0, sticky=Tk.W, pady=5)
    lado_var = Tk.StringVar(value="direito")
    combo_lado = ttk.Combobox(form_frame, textvariable=lado_var, 
                              values=["direito", "esquerdo"], width=18, state="readonly")
    combo_lado.grid(row=2, column=1, sticky=Tk.W, padx=10)

    Tk.Label(form_frame, text="Ciclo (dias):", bg="#0A0000", fg="#FFFFFF").grid(
        row=3, column=0, sticky=Tk.W, pady=5)
    entry_ciclo = Tk.Entry(form_frame, width=20)
    entry_ciclo.insert(0, "7")
    entry_ciclo.grid(row=3, column=1, sticky=Tk.W, padx=10)
    
    ciclo_info = Tk.Label(form_frame, text="(Ex: 7=semanal, 21=trimestral, 30=mensal)", 
                          bg="#0A0000", fg="#AAAAAA", font=("Montserrat", 9))
    ciclo_info.grid(row=4, column=0, columnspan=2, sticky=Tk.W, padx=5)

    hist_frame = Tk.LabelFrame(root, text="Histórico de Aplicações", bg="#0A0000", 
                               fg="#FFFFFF", font=("Montserrat", 12))
    hist_frame.pack(fill=Tk.BOTH, expand=True, padx=10, pady=10)

    text_historico = Tk.Text(hist_frame, bg="#1a1a1a", fg="#FFFFFF", font=("Courier", 9),
                             height=12, width=70)
    text_historico.pack(fill=Tk.BOTH, expand=True)

    def atualizar_historico():
        """Carrega e exibe o histórico de aplicações."""
        text_historico.config(state=Tk.NORMAL)
        text_historico.delete(1.0, Tk.END)
        aplicacoes = carregar_aplicacoes()
        if not aplicacoes:
            text_historico.insert(1.0, "Nenhuma aplicação registrada.")
        else:
            for app in aplicacoes[::-1]:
                proxima = app.proxima_aplicacao()
                dias = app.dias_restantes()
                texto = f"📅 {app.data} | 💉 {app.ml}ml | 👤 {app.lado.upper()} | ⏰ Próxima: {proxima} ({dias}d) | Ciclo: {app.ciclo_dias}d\n"
                text_historico.insert(Tk.END, texto)
        text_historico.config(state=Tk.DISABLED)

    def registrar_aplicacao():
        """Registra uma nova aplicação e atualiza o histórico."""
        try:
            app = Aplicacao(
                data=entry_data.get(),
                ml=float(entry_ml.get()),
                lado=lado_var.get(),
                ciclo_dias=int(entry_ciclo.get())
            )
            adicionar_aplicacao(app)
            proxima = app.proxima_aplicacao()
            dias = app.dias_restantes()
            messagebox.showinfo("✅ Sucesso", f"Aplicação registrada!\n\nPróxima: {proxima}\nDias restantes: {dias}")
            atualizar_historico()
            entry_ml.delete(0, Tk.END)
        except ValueError:
            messagebox.showerror("❌ Erro", "Preencha todos os campos com valores válidos.\n- Data: DD/MM/YYYY\n- Dosagem: número (ex: 5.5)\n- Ciclo: número inteiro (ex: 30)")

    btn_registrar = Button(form_frame, text="Registrar Aplicação", bg="#FF6B9D", 
                          fg="#FFFFFF", font=("Montserrat", 11, "bold"), 
                          command=registrar_aplicacao, padx=10, pady=5)
    btn_registrar.grid(row=5, column=0, columnspan=2, pady=15)

    atualizar_historico()
    
    return root