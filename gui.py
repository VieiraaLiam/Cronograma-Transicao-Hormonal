import datetime
import tkinter as Tk
from tkinter import ttk, messagebox, Label, Button
from tkcalendar import Calendar
import os
from model import Aplicacao 
from storage import carregar_aplicacoes, adicionar_aplicacao, salvar_aplicacoes

def _configure_style(root):
    # (seu código existente - não muda nada)
    bg = "#0A0000"
    accent = "#3b82f6"
    style = ttk.Style(root)
    try:
        style.theme_use("clam")
    except:
        pass
    style.configure("TFrame", background=bg)
    style.configure("TLabel", background=bg, foreground="#FFFFFF")
    style.configure("Accent.TButton", background=accent, foreground="#FFFFFF")
    style.configure("Treeview", background="#1a1a1a", foreground="#FFFFFF", fieldbackground="#1a1a1a")
    style.map("Accent.TButton", background=[("active", "#2563eb")])

def create_main_window():
    """Cria e retorna a janela principal do aplicativo."""
    
    # ============================================
    # 1. CRIA A JANELA PRINCIPAL
    # ============================================
    root = Tk.Tk()
    root.title("Cronograma TH")
    root.geometry("600x700")
    root.configure(bg="#0A0000")
    
    # ============================================
    # 2. CONFIGURA ESTILO
    # ============================================
    _configure_style(root)
    
    # ============================================
    # 3. HEADER (saudação e data)
    # ============================================
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
    
    # ============================================
    # 4. FORMULÁRIO DE REGISTRO
    # ============================================
    form_frame = Tk.LabelFrame(root, text="Registrar nova aplicação", bg="#0A0000", 
                               fg="#FFFFFF", font=("Montserrat", 12))
    form_frame.pack(fill=Tk.X, padx=10, pady=10)

    # Linha 0: Data
    Tk.Label(form_frame, text="Data (dd/mm/yyyy):", bg="#0A0000", fg="#FFFFFF", 
             font=("Montserrat", 10)).grid(row=0, column=0, padx=5, pady=5, sticky=Tk.W)
    entry_data = Tk.Entry(form_frame, width=20)
    entry_data.insert(0, data_hoje)
    entry_data.grid(row=0, column=1, sticky=Tk.W, padx=10)

    # Linha 1: Dosagem
    Tk.Label(form_frame, text="Dosagem (ml):", bg="#0A0000", fg="#FFFFFF").grid(
        row=1, column=0, sticky=Tk.W, pady=5)
    entry_ml = Tk.Entry(form_frame, width=20)
    entry_ml.grid(row=1, column=1, sticky=Tk.W, padx=10)

    # Linha 2: Lado
    Tk.Label(form_frame, text="Lado:", bg="#0A0000", fg="#FFFFFF").grid(
        row=2, column=0, sticky=Tk.W, pady=5)
    lado_var = Tk.StringVar(value="direito")
    combo_lado = ttk.Combobox(form_frame, textvariable=lado_var, 
                              values=["direito", "esquerdo"], width=18, state="readonly")
    combo_lado.grid(row=2, column=1, sticky=Tk.W, padx=10)

    # Linha 3: Ciclo
    Tk.Label(form_frame, text="Ciclo (dias):", bg="#0A0000", fg="#FFFFFF").grid(
        row=3, column=0, sticky=Tk.W, pady=5)
    entry_ciclo = Tk.Entry(form_frame, width=20)
    entry_ciclo.insert(0, "7")
    entry_ciclo.grid(row=3, column=1, sticky=Tk.W, padx=10)

    # Linha 4: Notas (CORRIGIDO - agora em linha própria!)
    Tk.Label(form_frame, text="Notas (opcional):", bg="#0a0000", fg="#FFFFFF").grid(
        row=4, column=0, sticky=Tk.W, padx=6, pady=4)
    text_notas_form = Tk.Text(form_frame, bg="#1a1a1a", fg="#FFFFFF", height=3, width=60)
    text_notas_form.grid(row=4, column=1, columnspan=3, sticky=Tk.W, padx=10)

    # Linha 5: Informação do ciclo
    ciclo_info = Tk.Label(form_frame, text="(Ex: 7=semanal, 21=trimestral, 30=mensal)", 
                          bg="#0A0000", fg="#AAAAAA", font=("Montserrat", 9))
    ciclo_info.grid(row=5, column=0, columnspan=2, sticky=Tk.W, padx=5)

    # Linha 6: Botão registrar
    btn_registrar = Button(form_frame, text="Registrar Aplicação", bg="#FF6B9D", 
                          fg="#FFFFFF", font=("Montserrat", 11, "bold"), 
                          command=lambda: registrar_aplicacao(), padx=10, pady=5)
    btn_registrar.grid(row=6, column=0, columnspan=2, pady=15)
    
    # ============================================
    # 5. LAYOUT PRINCIPAL (Treeview + detalhes)
    # ============================================
    main_frame = Tk.Frame(root)
    main_frame.pack(fill=Tk.BOTH, expand=True, padx=10, pady=6)
    main_frame.columnconfigure(0, weight=1)
    main_frame.columnconfigure(1, weight=2)
    main_frame.rowconfigure(0, weight=1)

    right_frame = Tk.Frame(main_frame)
    right_frame.grid(row=0, column=1, sticky=Tk.NSEW)
    right_frame.rowconfigure(0, weight=1)
    right_frame.rowconfigure(1, weight=0)
    right_frame.columnconfigure(0, weight=1)

    cols = ("Data", "Dosagem", "Lado", "Próxima", "Dias Restantes", "Ciclo")
    tree = ttk.Treeview(right_frame, columns=cols, show="headings", height=12)
    tree.heading("Data", text="Data")
    tree.heading("Dosagem", text="Dosagem (ml)")
    tree.heading("Lado", text="Lado")
    tree.heading("Próxima", text="Próxima Aplicação")
    tree.heading("Dias Restantes", text="Dias Restantes")
    tree.heading("Ciclo", text="Ciclo (dias)")
    tree.grid(row=0, column=0, sticky=Tk.NSEW, pady=(0,8))

    # Detalhes notas
    detail_frame = ttk.Frame(right_frame)
    detail_frame.grid(row=1, column=0, sticky=Tk.EW)
    ttk.Label(detail_frame, text="Efeitos:").grid(row=0, column=0, sticky=Tk.W)
    txt_notas = Tk.Text(detail_frame, height=6, bg="#1a1a1a", fg="#FFFFFF")
    txt_notas.grid(row=1, column=0, sticky=Tk.EW, pady=6)
    btn_save_note = ttk.Button(detail_frame, text="Salvar Nota", style="Accent.TButton")
    btn_save_note.grid(row=2, column=0, sticky="e")
    
    # ============================================
    # 6. CALENDÁRIO (ANTES ERA FORA DA FUNÇÃO - AGORA DENTRO!)
    # ============================================
    calendar_frame = Tk.LabelFrame(root, text="Calendário de Aplicações", bg="#0A0000", 
                                   fg="#FFFFFF", padx=8, pady=8)
    calendar_frame.pack(fill=Tk.BOTH, expand=True, padx=10, pady=6)

    cal = Calendar(calendar_frame, selectmode='day', date_pattern='dd/mm/yyyy', 
                   background="#1a1a1a")
    cal.pack(side=Tk.LEFT, padx=(0,10))

    events_frame = Tk.Frame(calendar_frame, bg="#0A0000")
    events_frame.pack(side=Tk.LEFT, fill=Tk.BOTH, expand=True)

    lbl_events = Label(events_frame, text="Eventos do dia", bg="#0A0000", fg="#FFFFFF", 
                       font=("Montserrat", 11, "bold"))
    lbl_events.pack(anchor=Tk.NW)

    list_events = Tk.Listbox(events_frame, bg="#1a1a1a", fg="#FFFFFF", height=8, width=50)
    list_events.pack(fill=Tk.BOTH, expand=True, pady=6)
    
    # ============================================
    # 7. FUNÇÕES AUXILIARES (que usam os widgets)
    # ============================================
    def build_event_index():
        idx = {}
        for app in carregar_aplicacoes():
            idx.setdefault(app.data, []).append(app)
        return idx
    
    event_index = build_event_index()

    def populate_tree_for_date(date=None):
        tree.delete(*tree.get_children())
        date = date or cal.get_date()
        apps = event_index.get(date, [])
        for i, app in enumerate(apps):
            tree.insert("", Tk.END, iid=str(i), values=(
                app.data, f"{app.ml}ml", app.lado, 
                app.proxima_aplicacao(), app.dias_restantes(), app.ciclo_dias
            ))

    def on_calendar_select(event=None):
        populate_tree_for_date(cal.get_date())
        on_date_select()  # Atualiza a lista de eventos

    def on_tree_select(event=None):
        sel = tree.selection()
        if not sel:
            txt_notas.delete(1.0, Tk.END)
            return
        idx = sel[0]
        date = cal.get_date()
        apps = event_index.get(date, [])
        if idx < 0 or idx >= len(apps):
            txt_notas.delete("1.0", Tk.END)
            return
        app = apps[idx]
        txt_notas.delete("1.0", Tk.END)
        txt_notas.insert(Tk.END, getattr(app, "notas", ""))

    def save_note():
        sel = tree.selection()
        if not sel:
            messagebox.showwarning("⚠️ Salvar Nota", "Selecione um evento para salvar a nota.")
            return
        idx = int(sel[0])
        date = cal.get_date()
        apps = event_index.get(date, [])
        if idx < 0 or idx >= len(apps):
            messagebox.showerror("❌ Erro", "Seleção inválida.")
            return
        app = apps[idx]
        app.notas = txt_notas.get("1.0", Tk.END).strip()

        all_apps = carregar_aplicacoes()
        for i, a in enumerate(all_apps):
            if a.data == app.data and a.ml == app.ml and a.lado == app.lado and a.ciclo_dias == app.ciclo_dias:
                all_apps[i] = app
                break
        salvar_aplicacoes(all_apps)
        
        # Reconstroi o index
        nonlocal_event_index = build_event_index()
        event_index.clear()
        event_index.update(nonlocal_event_index)
        populate_tree_for_date(date)
        messagebox.showinfo("✅ Nota Salva", "Nota salva com sucesso!")

    # ============================================
    # 8. FUNÇÕES DO CALENDÁRIO
    # ============================================
    def on_date_select(event=None):
        sel = cal.get_date()
        list_events.delete(0, Tk.END)
        apps = event_index.get(sel, [])
        for app in apps:
            list_events.insert(Tk.END, f"{app.data} — {app.ml}ml — {app.lado} — ciclo {app.ciclo_dias}d")

    def show_event_detail(evt=None):
        sel = list_events.curselection()
        if not sel:
            return
        idx = sel[0]
        date = cal.get_date()
        app = event_index.get(date, [])[idx]
        top = Tk.Toplevel(root)
        top.title("Detalhes da Aplicação")
        top.geometry("420x320")
        top.configure(bg="#0A0000")
        # Aqui você pode adicionar mais detalhes
    
    # ============================================
    # 9. BINDS (conectam eventos às funções)
    # ============================================
    cal.bind("<<CalendarSelected>>", on_calendar_select)
    tree.bind("<<TreeviewSelect>>", on_tree_select)
    btn_save_note.config(command=save_note)
    list_events.bind("<<ListboxSelect>>", show_event_detail)
    
    # ============================================
    # 10. INICIALIZAÇÃO
    # ============================================
    on_date_select()  # Mostra eventos do dia atual
    populate_tree_for_date()  # Popula treeview
    
    # ============================================
    # 11. HISTÓRICO (SEU CÓDIGO ORIGINAL)
    # ============================================
    hist_frame = Tk.LabelFrame(root, text="Histórico de Aplicações", bg="#0A0000", 
                               fg="#FFFFFF", font=("Montserrat", 12))
    hist_frame.pack(fill=Tk.BOTH, expand=True, padx=10, pady=10)

    text_historico = Tk.Text(hist_frame, bg="#1a1a1a", fg="#FFFFFF", font=("Courier", 9),
                             height=12, width=70)
    text_historico.pack(fill=Tk.BOTH, expand=True)

    def atualizar_historico():
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
            
            # Atualiza calendário e treeview
            nonlocal_event_index = build_event_index()
            event_index.clear()
            event_index.update(nonlocal_event_index)
            on_date_select()
            populate_tree_for_date()
            
            entry_ml.delete(0, Tk.END)
        except ValueError:
            messagebox.showerror("❌ Erro", "Preencha todos os campos com valores válidos.\n- Data: DD/MM/YYYY\n- Dosagem: número (ex: 5.5)\n- Ciclo: número inteiro (ex: 30)")

    # Atualiza botão registrar para usar a função correta
    btn_registrar.config(command=registrar_aplicacao)
    
    # Inicializa histórico
    atualizar_historico()
    
    # ============================================
    # 12. RETORNA A JANELA
    # ============================================
    return root

# ============================================
# 13. EXECUTA O APP (FORA DA FUNÇÃO)
# ============================================
if __name__ == "__main__":
    janela = create_main_window()
    janela.mainloop()