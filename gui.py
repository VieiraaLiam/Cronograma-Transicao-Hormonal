import datetime
import customtkinter as ctk
from tkinter import messagebox, Listbox
from tkinter import ttk
from tkcalendar import Calendar
import os
from model import Aplicacao 
from storage import carregar_aplicacoes, adicionar_aplicacao, salvar_aplicacoes

# Configuração do CustomTkinter
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("dark-blue")

def _configure_style(root):
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
    root = ctk.CTk()
    root.title("Cronograma TH")
    root.geometry("900x800")
    
    # ============================================
    # 2. CONFIGURA ESTILO
    # ============================================
    _configure_style(root)
    
    # ============================================
    # 3. CONTROLE DE TELA CHEIA E CALENDÁRIO
    # ============================================
    fullscreen = False
    calendar_frame = None
    
    # ============================================
    # 4. HEADER (saudação e data)
    # ============================================
    header_frame = ctk.CTkFrame(root, fg_color="#0A0000")
    header_frame.pack(fill='x', padx=10, pady=5)
    
    user_name = os.getenv("USERNAME", "USUARIO")
    saudacao = ctk.CTkLabel(header_frame, text=f"Bem-vindo {user_name}!", 
                           text_color="#FFFFFF", font=("Montserrat", 14))
    saudacao.pack(side='left', padx=10)
    
    data_hoje = datetime.datetime.now().strftime("%d/%m/%Y")
    data_label = ctk.CTkLabel(header_frame, text=f"Data de hoje: {data_hoje}",
                              text_color="#FFFFFF", font=("Montserrat", 12))
    data_label.pack(side='right', padx=10)
    
    # ============================================
    # 5. FORMULÁRIO DE REGISTRO
    # ============================================
    form_frame = ctk.CTkFrame(root, fg_color="#0A0000", border_width=2, border_color="#2d2d2d")
    form_frame.pack(fill='x', padx=10, pady=10)
    
    form_title = ctk.CTkLabel(form_frame, text="Registrar nova aplicação", 
                              font=("Montserrat", 14, "bold"), text_color="#FFFFFF")
    form_title.pack(pady=5)
    
    campos_frame = ctk.CTkFrame(form_frame, fg_color="#0A0000")
    campos_frame.pack(padx=20, pady=10)
    
    # Linha 0: Data
    ctk.CTkLabel(campos_frame, text="Data (dd/mm/yyyy):", text_color="#FFFFFF").grid(row=0, column=0, padx=5, pady=5, sticky='w')
    entry_data = ctk.CTkEntry(campos_frame, width=200)
    entry_data.insert(0, data_hoje)
    entry_data.grid(row=0, column=1, padx=10, pady=5)
    
    # Linha 1: Dosagem
    ctk.CTkLabel(campos_frame, text="Dosagem (ml):", text_color="#FFFFFF").grid(row=1, column=0, padx=5, pady=5, sticky='w')
    entry_ml = ctk.CTkEntry(campos_frame, width=200)
    entry_ml.grid(row=1, column=1, padx=10, pady=5)
    
    # Linha 2: Lado
    ctk.CTkLabel(campos_frame, text="Lado:", text_color="#FFFFFF").grid(row=2, column=0, padx=5, pady=5, sticky='w')
    lado_var = ctk.StringVar(value="direito")
    combo_lado = ttk.Combobox(campos_frame, textvariable=lado_var, 
                              values=["direito", "esquerdo"], width=18, state="readonly")
    combo_lado.grid(row=2, column=1, padx=10, pady=5, sticky='w')
    
    # Linha 3: Ciclo
    ctk.CTkLabel(campos_frame, text="Ciclo (dias):", text_color="#FFFFFF").grid(row=3, column=0, padx=5, pady=5, sticky='w')
    entry_ciclo = ctk.CTkEntry(campos_frame, width=200)
    entry_ciclo.insert(0, "7")
    entry_ciclo.grid(row=3, column=1, padx=10, pady=5)
    
    # Linha 4: Notas
    ctk.CTkLabel(campos_frame, text="Notas (opcional):", text_color="#FFFFFF").grid(row=4, column=0, padx=5, pady=5, sticky='w')
    text_notas_form = ctk.CTkTextbox(campos_frame, fg_color="#1a1a1a", text_color="#FFFFFF", height=60, width=300)
    text_notas_form.grid(row=4, column=1, padx=10, pady=5)
    
    # Linha 5: Informação do ciclo
    ciclo_info = ctk.CTkLabel(campos_frame, text="(Ex: 7=semanal, 21=trimestral, 30=mensal)", 
                              text_color="#AAAAAA", font=("Montserrat", 9))
    ciclo_info.grid(row=5, column=0, columnspan=2, pady=5)
    
    # Linha 6: Botão registrar
    btn_registrar = ctk.CTkButton(form_frame, text="Registrar Aplicação", 
                                  fg_color="#FF6B9D", text_color="#FFFFFF", 
                                  font=("Montserrat", 11, "bold"))
    btn_registrar.pack(pady=15)
    
    # ============================================
    # 6. LAYOUT PRINCIPAL (Treeview + detalhes)
    # ============================================
    main_frame = ctk.CTkFrame(root, fg_color="#0A0000")
    main_frame.pack(fill='both', expand=True, padx=10, pady=6)
    
    left_frame = ctk.CTkFrame(main_frame, fg_color="#1a1a1a")
    left_frame.pack(side='left', fill='both', expand=True, padx=(0, 5))
    
    cols = ("Data", "Dosagem", "Lado", "Próxima", "Dias Restantes", "Ciclo")
    tree = ttk.Treeview(left_frame, columns=cols, show="headings", height=12)
    tree.heading("Data", text="Data")
    tree.heading("Dosagem", text="Dosagem (ml)")
    tree.heading("Lado", text="Lado")
    tree.heading("Próxima", text="Próxima Aplicação")
    tree.heading("Dias Restantes", text="Dias Restantes")
    tree.heading("Ciclo", text="Ciclo (dias)")
    tree.pack(fill='both', expand=True, pady=5)
    
    right_frame = ctk.CTkFrame(main_frame, fg_color="#0A0000")
    right_frame.pack(side='right', fill='both', expand=True, padx=(5, 0))
    
    ctk.CTkLabel(right_frame, text="Efeitos / Notas:", text_color="#FFFFFF", font=("Montserrat", 11)).pack(anchor='w')
    txt_notas = ctk.CTkTextbox(right_frame, fg_color="#1a1a1a", text_color="#FFFFFF", height=120)
    txt_notas.pack(fill='both', expand=True, pady=5)
    
    btn_save_note = ctk.CTkButton(right_frame, text="Salvar Nota", fg_color="#4CAF50", text_color="#FFFFFF")
    btn_save_note.pack(pady=5)
    
    # ============================================
    # 7. HISTÓRICO
    # ============================================
    hist_frame = ctk.CTkFrame(root, fg_color="#0A0000")
    hist_frame.pack(fill='both', expand=True, padx=10, pady=10)
    
    hist_label = ctk.CTkLabel(hist_frame, text="Histórico de Aplicações", 
                               font=("Montserrat", 12, "bold"), text_color="#FFFFFF")
    hist_label.pack(anchor='w')
    
    text_historico = ctk.CTkTextbox(hist_frame, fg_color="#1a1a1a", text_color="#FFFFFF", 
                                     font=("Courier", 10), height=150)
    text_historico.pack(fill='both', expand=True, pady=5)
    
    # ============================================
    # 8. FUNÇÕES AUXILIARES
    # ============================================
    def build_event_index():
        idx = {}
        for app in carregar_aplicacoes():
            idx.setdefault(app.data, []).append(app)
        return idx
    
    event_index = build_event_index()
    
    def populate_tree_for_date(date=None):
        tree.delete(*tree.get_children())
        date = date or (calendar_frame.cal.get_date() if calendar_frame else data_hoje)
        apps = event_index.get(date, [])
        for i, app in enumerate(apps):
            tree.insert("", "end", iid=str(i), values=(
                app.data, f"{app.ml}ml", app.lado, 
                app.proxima_aplicacao(), app.dias_restantes(), app.ciclo_dias
            ))
    
    def on_calendar_select(cal, list_events):
        date = cal.get_date()
        populate_tree_for_date(date)
        
        # Atualiza lista de eventos
        list_events.delete(0, "end")
        apps = event_index.get(date, [])
        for app in apps:
            list_events.insert("end", f"{app.data} — {app.ml}ml — {app.lado} — ciclo {app.ciclo_dias}d")
    
    def on_tree_select(event=None):
        sel = tree.selection()
        if not sel:
            txt_notas.delete("1.0", "end")
            return
        idx = sel[0]
        date = calendar_frame.cal.get_date() if calendar_frame else data_hoje
        apps = event_index.get(date, [])
        if not apps or int(idx) >= len(apps):
            txt_notas.delete("1.0", "end")
            return
        app = apps[int(idx)]
        txt_notas.delete("1.0", "end")
        txt_notas.insert("1.0", getattr(app, "notas", ""))
    
    def save_note():
        sel = tree.selection()
        if not sel:
            messagebox.showwarning("⚠️ Salvar Nota", "Selecione um evento para salvar a nota.")
            return
        idx = int(sel[0])
        date = calendar_frame.cal.get_date() if calendar_frame else data_hoje
        apps = event_index.get(date, [])
        if idx < 0 or idx >= len(apps):
            messagebox.showerror("❌ Erro", "Seleção inválida.")
            return
        app = apps[idx]
        app.notas = txt_notas.get("1.0", "end-1c").strip()
        
        all_apps = carregar_aplicacoes()
        for i, a in enumerate(all_apps):
            if (a.data == app.data and a.ml == app.ml and 
                a.lado == app.lado and a.ciclo_dias == app.ciclo_dias):
                all_apps[i] = app
                break
        salvar_aplicacoes(all_apps)
        
        nonlocal_event_index = build_event_index()
        event_index.clear()
        event_index.update(nonlocal_event_index)
        populate_tree_for_date(date)
        messagebox.showinfo("✅ Nota Salva", "Nota salva com sucesso!")
    
    def show_event_detail(evt=None, list_events=None, cal=None):
        sel = list_events.curselection()
        if not sel:
            return
        idx = sel[0]
        date = cal.get_date()
        apps = event_index.get(date, [])
        if not apps or idx >= len(apps):
            return
        app = apps[idx]
        top = ctk.CTkToplevel(root)
        top.title("Detalhes da Aplicação")
        top.geometry("400x300")
        top.attributes('-topmost', True)
        
        ctk.CTkLabel(top, text=f"Data: {app.data}", font=("Arial", 12)).pack(pady=5)
        ctk.CTkLabel(top, text=f"Dosagem: {app.ml}ml", font=("Arial", 12)).pack(pady=5)
        ctk.CTkLabel(top, text=f"Lado: {app.lado}", font=("Arial", 12)).pack(pady=5)
        ctk.CTkLabel(top, text=f"Ciclo: {app.ciclo_dias} dias", font=("Arial", 12)).pack(pady=5)
        ctk.CTkLabel(top, text=f"Próxima: {app.proxima_aplicacao()}", font=("Arial", 12)).pack(pady=5)
    
    def atualizar_historico():
        text_historico.delete("1.0", "end")
        aplicacoes = carregar_aplicacoes()
        if not aplicacoes:
            text_historico.insert("1.0", "Nenhuma aplicação registrada.")
        else:
            for app in aplicacoes[::-1]:
                proxima = app.proxima_aplicacao()
                dias = app.dias_restantes()
                texto = f"📅 {app.data} | 💉 {app.ml}ml | 👤 {app.lado.upper()} | ⏰ Próxima: {proxima} ({dias}d) | Ciclo: {app.ciclo_dias}d\n"
                text_historico.insert("end", texto)
    
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
            
            nonlocal_event_index = build_event_index()
            event_index.clear()
            event_index.update(nonlocal_event_index)
            
            if calendar_frame:
                on_calendar_select(calendar_frame.cal, calendar_frame.list_events)
            populate_tree_for_date()
            
            entry_ml.delete(0, "end")
        except ValueError:
            messagebox.showerror("❌ Erro", "Preencha todos os campos com valores válidos.\n- Data: DD/MM/YYYY\n- Dosagem: número (ex: 5.5)\n- Ciclo: número inteiro (ex: 30)")
    
    # ============================================
    # 9. FUNÇÕES DE TELA CHEIA E CALENDÁRIO
    # ============================================
    def criar_calendario():
        nonlocal calendar_frame
        if calendar_frame is not None:
            return
        
        calendar_frame = ctk.CTkFrame(root, fg_color="#0A0000")
        calendar_frame.pack(fill='both', expand=True, padx=10, pady=6)
        
        # Subframe esquerdo do calendário
        cal_left = ctk.CTkFrame(calendar_frame, fg_color="#0A0000")
        cal_left.pack(side='left', fill='both', expand=True)
        
        cal = Calendar(cal_left, selectmode='day', date_pattern='dd/mm/yyyy', 
                       background="#1a1a1a", foreground="white",
                       headersbackground="#2d2d2d", normalbackground="#2d2d2d",
                       weekendbackground="#3d3d3d")
        cal.pack(fill='both', expand=True)
        
        # Subframe direito do calendário (eventos)
        cal_right = ctk.CTkFrame(calendar_frame, fg_color="#0A0000")
        cal_right.pack(side='right', fill='both', expand=True, padx=(10, 0))
        
        lbl_events = ctk.CTkLabel(cal_right, text="Eventos do dia", 
                                   text_color="#FFFFFF", font=("Montserrat", 11, "bold"))
        lbl_events.pack(anchor='w')
        
        list_events = Listbox(cal_right, bg="#2d2d2d", fg="white", 
                              selectbackground="#FF6B9D", height=8, font=('Arial', 10))
        list_events.pack(fill='both', expand=True, pady=5)
        
        # Salvar referências
        calendar_frame.cal = cal
        calendar_frame.list_events = list_events
        
        # Conectar eventos
        cal.bind("<<CalendarSelected>>", lambda e: on_calendar_select(cal, list_events))
        list_events.bind("<Double-Button-1>", lambda e: show_event_detail(list_events=list_events, cal=cal))
        
        # Inicializar com a data atual
        on_calendar_select(cal, list_events)
    
    def destruir_calendario():
        nonlocal calendar_frame
        if calendar_frame is not None:
            calendar_frame.destroy()
            calendar_frame = None
    
    def toggle_fullscreen(event=None):
        nonlocal fullscreen
        fullscreen = not fullscreen
        root.attributes('-fullscreen', fullscreen)
        
        if fullscreen:
            criar_calendario()
        else:
            destruir_calendario()
    
    root.bind('<F11>', toggle_fullscreen)
    root.bind('<Escape>', lambda e: root.attributes('-fullscreen', False))
    
    # ============================================
    # 10. BINDS E CONFIGURAÇÕES FINAIS
    # ============================================
    tree.bind("<<TreeviewSelect>>", on_tree_select)
    btn_save_note.configure(command=save_note)
    btn_registrar.configure(command=registrar_aplicacao)
    
    # Inicialização
    populate_tree_for_date()
    atualizar_historico()
    
    return root

if __name__ == "__main__":
    janela = create_main_window()
    janela.mainloop()