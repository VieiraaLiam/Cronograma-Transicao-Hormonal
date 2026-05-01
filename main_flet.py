"""Cronograma TH - Interface gráfica com Flet"""

import sys
import os
import threading

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "src"))

import flet as ft
from datetime import datetime
from aplicacao_service import AplicacaoService
from config_repository import ConfigRepository
from nota_repository import NotaRepository
from google_auth import GoogleAuth
from google_events_repository import GoogleEventsRepository

def main(page: ft.Page):
    print("✅ App iniciado!")
    print(f"🔗 Acesse em: http://localhost:{8080}")
    # ========== CONFIGURAÇÕES MOBILE ==========
    page.title = "Cronograma TH"
    page.theme_mode = ft.ThemeMode.DARK
    page.padding = 16
    page.spacing = 16
    page.scroll = ft.ScrollMode.AUTO  # Permite rolar a tela
    
    # Configurações de janela (desktop)
    page.window_width = 420
    page.window_height = 780
    page.window_resizable = False
    
    # Inicializa serviços
    app_service = AplicacaoService()
    config_repo = ConfigRepository()
    nota_repo = NotaRepository()
    auth = GoogleAuth()
    events_repo = GoogleEventsRepository()
    
    # Estado do app
    db = {
        "service": app_service,
        "config": config_repo,
        "notas": nota_repo,
        "auth": auth,
        "events": events_repo,
        "logado": auth.esta_logado()
    }
    
    # Área de conteúdo
    content_area = ft.Column(spacing=20)
    
    # Título
    titulo = ft.Text("🏥 CRONOGRAMA TH", size=30, weight=ft.FontWeight.BOLD)
    page.add(titulo)
    page.add(content_area)
    
    # ========== FUNÇÕES DAS TELAS ==========
    
    def atualizar_status():
        """Atualiza status do login"""
        db["logado"] = db["auth"].esta_logado()
        return db["logado"]
    
    def mostrar_mensagem(titulo, texto, eh_erro=False):
        """Mostra mensagem para o usuário"""
        cor = ft.Colors.RED if eh_erro else ft.Colors.GREEN
        page.snack_bar = ft.SnackBar(
            content=ft.Text(texto),
            bgcolor=cor,
            action="Fechar"
        )
        page.snack_bar.open = True
        page.update()
    
    # ========== TELA INICIAL ==========
    def mostrar_tela_inicial():
        content_area.controls.clear()
        
        logado = atualizar_status()
        logado_status = "✅ Logado" if logado else "❌ Não logado"
        
        status_text = ft.Text(
            f"Status Google: {logado_status}",
            size=14,
            color=ft.Colors.GREEN if logado else ft.Colors.RED
        )
        
        if logado:
            botoes = ft.Column([
                ft.ElevatedButton("📝 Registrar aplicação", on_click=registrar_click, width=300),
                ft.ElevatedButton("📋 Ver histórico", on_click=historico_click, width=300),
                ft.ElevatedButton("🔍 Buscar por data", on_click=buscar_click, width=300),
                ft.ElevatedButton("📝 Adicionar nota", on_click=adicionar_nota_click, width=300),
                ft.ElevatedButton("🔍 Ver notas do dia", on_click=ver_notas_click, width=300),
                ft.ElevatedButton("⚙️ Configurações", on_click=configuracoes_click, width=300),
                ft.ElevatedButton("🗑️ Remover aplicação", on_click=remover_click, width=300),
                ft.ElevatedButton("🚪 Sair", on_click=sair_click, width=300),
            ], spacing=10, horizontal_alignment=ft.CrossAxisAlignment.CENTER)
        else:
            botoes = ft.Column([
                ft.ElevatedButton("🔐 Fazer login no Google", on_click=login_click, width=300),
            ], spacing=10, horizontal_alignment=ft.CrossAxisAlignment.CENTER)
        
        content_area.controls.append(status_text)
        content_area.controls.append(botoes)
        page.update()
    
    # ========== TELA DE LOGIN ==========
    def login_click(e):
        def login_task():
            try:
                resultado = db["auth"].fazer_login()
                db["logado"] = resultado
                page.run_coroutine(login_callback)
            except Exception as err:
                page.run_coroutine(lambda: mostrar_mensagem("Erro", str(err), True))
        
        async def login_callback():
            if db["logado"]:
                mostrar_mensagem("Sucesso", "Login realizado com sucesso!", False)
                mostrar_tela_inicial()
            else:
                mostrar_mensagem("Erro", "Falha na autenticação.", True)
        
        # Mostra diálogo de carregamento
        loading = ft.AlertDialog(
            title=ft.Text("Conectando..."),
            content=ft.Text("Aguardando autenticação no Google..."),
            modal=True
        )
        page.dialog = loading
        loading.open = True
        page.update()
        
        threading.Thread(target=login_task, daemon=True).start()
    
    # ========== TELA DE REGISTRO ==========
    def registrar_click(e):
        content_area.controls.clear()
        
        titulo_tela = ft.Text("📝 Registrar nova aplicação", size=20, weight=ft.FontWeight.BOLD)
        
        data_field = ft.TextField(label="Data (dd/mm/aaaa)", hint_text="Deixe em branco para hoje")
        ml_field = ft.TextField(label="Dosagem (ml)", keyboard_type=ft.KeyboardType.NUMBER)
        lado_dropdown = ft.Dropdown(
            label="Lado",
            options=[
                ft.dropdown.Option("direito"),
                ft.dropdown.Option("esquerdo"),
            ]
        )
        notas_field = ft.TextField(label="Notas (opcional)", multiline=True, min_lines=2, max_lines=4)
        
        voltar_btn = ft.ElevatedButton("◀ Voltar", on_click=lambda e: mostrar_tela_inicial())
        
        def salvar_click(e):
            try:
                data = data_field.value.strip()
                if not data:
                    data = datetime.now().strftime("%d/%m/%Y")
                
                # Valida data futura
                data_obj = datetime.strptime(data, "%d/%m/%Y")
                hoje = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
                if data_obj > hoje:
                    mostrar_mensagem("Erro", "Não é possível registrar no futuro!", True)
                    return
                
                ml = float(ml_field.value)
                lado = lado_dropdown.value
                notas = notas_field.value
                
                if not lado:
                    mostrar_mensagem("Erro", "Selecione um lado!", True)
                    return
                
                app = db["service"].registrar(data, ml, lado, notas)
                
                # Criar evento no Google se logado
                if db["logado"] and db["auth"].service:
                    try:
                        data_evento = datetime.strptime(app.proxima_data, "%d/%m/%Y")
                        data_inicio = data_evento.strftime("%Y-%m-%d")
                        
                        titulo = f"💉 Próxima aplicação: {app.ml}ml no {app.lado}"
                        descricao = f"Ciclo: {app.ciclo_dias} dias"
                        
                        evento_link = db["auth"].criar_evento(titulo, data_inicio, data_inicio, descricao)
                        if evento_link:
                            db["events"].salvar_evento(app.proxima_data, evento_link)
                    except Exception as err:
                        print(f"Erro ao criar evento: {err}")
                
                mostrar_mensagem("Sucesso", f"Aplicação registrada! Próxima dose: {app.proxima_data}", False)
                mostrar_tela_inicial()
                
            except ValueError as err:
                mostrar_mensagem("Erro", str(err), True)
        
        salvar_btn = ft.ElevatedButton("💾 Salvar aplicação", on_click=salvar_click)
        
        content_area.controls.clear()
        content_area.controls.append(titulo_tela)
        content_area.controls.append(data_field)
        content_area.controls.append(ml_field)
        content_area.controls.append(lado_dropdown)
        content_area.controls.append(notas_field)
        content_area.controls.append(ft.Row([salvar_btn, voltar_btn], spacing=10))
        page.update()
    
    # ========== TELA DE HISTÓRICO ==========
    def historico_click(e):
        content_area.controls.clear()
        
        titulo_tela = ft.Text("📋 Histórico de aplicações", size=20, weight=ft.FontWeight.BOLD)
        
        aplicacoes = db["service"].listar_todas()
        
        if not aplicacoes:
            content_area.controls.append(titulo_tela)
            content_area.controls.append(ft.Text("Nenhuma aplicação registrada ainda."))
        else:
            # Cria uma tabela
            table = ft.DataTable(
                columns=[
                    ft.DataColumn(ft.Text("Data")),
                    ft.DataColumn(ft.Text("Dosagem")),
                    ft.DataColumn(ft.Text("Lado")),
                    ft.DataColumn(ft.Text("Próxima")),
                    ft.DataColumn(ft.Text("Ciclo")),
                ],
                rows=[]
            )
            
            for app in aplicacoes[::-1]:  # Mais recente primeiro
                table.rows.append(
                    ft.DataRow(
                        cells=[
                            ft.DataCell(ft.Text(app.data)),
                            ft.DataCell(ft.Text(f"{app.ml}ml")),
                            ft.DataCell(ft.Text(app.lado)),
                            ft.DataCell(ft.Text(app.proxima_data)),
                            ft.DataCell(ft.Text(f"{app.ciclo_dias}d")),
                        ]
                    )
                )
            
            content_area.controls.append(titulo_tela)
            content_area.controls.append(table)
        
        voltar_btn = ft.ElevatedButton("◀ Voltar", on_click=lambda e: mostrar_tela_inicial())
        content_area.controls.append(voltar_btn)
        page.update()
    
    # ========== TELA DE BUSCA ==========
    def buscar_click(e):
        content_area.controls.clear()
        
        titulo_tela = ft.Text("🔍 Buscar por data", size=20, weight=ft.FontWeight.BOLD)
        data_field = ft.TextField(label="Data (dd/mm/aaaa)", width=200)
        
        resultado_text = ft.Column()
        
        def realizar_busca(e):
            resultado_text.controls.clear()
            data = data_field.value.strip()
            if not data:
                mostrar_mensagem("Aviso", "Digite uma data", True)
                return
            
            aplicacoes = db["service"].buscar_por_data(data)
            if not aplicacoes:
                resultado_text.controls.append(ft.Text(f"📭 Nenhuma aplicação encontrada em {data}"))
            else:
                resultado_text.controls.append(ft.Text(f"📅 Aplicações em {data}:"))
                for app in aplicacoes:
                    resultado_text.controls.append(ft.Text(f"   💉 {app.ml}ml | 👤 {app.lado} | 🔄 ciclo {app.ciclo_dias}d"))
            page.update()
        
        buscar_btn = ft.ElevatedButton("🔍 Buscar", on_click=realizar_busca)
        voltar_btn = ft.ElevatedButton("◀ Voltar", on_click=lambda e: mostrar_tela_inicial())
        
        content_area.controls.append(titulo_tela)
        content_area.controls.append(data_field)
        content_area.controls.append(ft.Row([buscar_btn, voltar_btn], spacing=10))
        content_area.controls.append(resultado_text)
        page.update()
    
    # ========== TELA DE ADICIONAR NOTA ==========
    def adicionar_nota_click(e):
        content_area.controls.clear()
        
        titulo_tela = ft.Text("📝 Adicionar nota ao diário", size=20, weight=ft.FontWeight.BOLD)
        
        data_field = ft.TextField(label="Data (dd/mm/aaaa)", hint_text="Deixe em branco para hoje")
        texto_field = ft.TextField(label="Nota", multiline=True, min_lines=3, max_lines=6)
        
        voltar_btn = ft.ElevatedButton("◀ Voltar", on_click=lambda e: mostrar_tela_inicial())
        
        def salvar_nota(e):
            data = data_field.value.strip()
            if not data:
                data = datetime.now().strftime("%d/%m/%Y")
            
            texto = texto_field.value.strip()
            if not texto:
                mostrar_mensagem("Erro", "A nota não pode estar vazia!", True)
                return
            
            db["notas"].adicionar(data, texto)
            mostrar_mensagem("Sucesso", "Nota adicionada com sucesso!", False)
            mostrar_tela_inicial()
        
        salvar_btn = ft.ElevatedButton("💾 Salvar nota", on_click=salvar_nota)
        
        content_area.controls.append(titulo_tela)
        content_area.controls.append(data_field)
        content_area.controls.append(texto_field)
        content_area.controls.append(ft.Row([salvar_btn, voltar_btn], spacing=10))
        page.update()
    
    # ========== TELA DE VER NOTAS ==========
    def ver_notas_click(e):
        content_area.controls.clear()
        
        titulo_tela = ft.Text("🔍 Ver notas do dia", size=20, weight=ft.FontWeight.BOLD)
        data_field = ft.TextField(label="Data (dd/mm/aaaa)", width=200)
        
        resultado_text = ft.Column()
        
        def realizar_busca(e):
            resultado_text.controls.clear()
            data = data_field.value.strip()
            if not data:
                mostrar_mensagem("Aviso", "Digite uma data", True)
                return
            
            notas = db["notas"].listar_por_data(data)
            if not notas:
                resultado_text.controls.append(ft.Text(f"📭 Nenhuma nota encontrada para {data}"))
            else:
                resultado_text.controls.append(ft.Text(f"📝 Notas de {data}:"))
                for i, nota in enumerate(notas, 1):
                    resultado_text.controls.append(ft.Text(f"  {i}. {nota.horario} - {nota.texto}"))
            page.update()
        
        buscar_btn = ft.ElevatedButton("🔍 Buscar", on_click=realizar_busca)
        voltar_btn = ft.ElevatedButton("◀ Voltar", on_click=lambda e: mostrar_tela_inicial())
        
        content_area.controls.append(titulo_tela)
        content_area.controls.append(data_field)
        content_area.controls.append(ft.Row([buscar_btn, voltar_btn], spacing=10))
        content_area.controls.append(resultado_text)
        page.update()
    
    # ========== TELA DE CONFIGURAÇÕES ==========
    def configuracoes_click(e):
        content_area.controls.clear()
        
        titulo_tela = ft.Text("⚙️ Configurações", size=20, weight=ft.FontWeight.BOLD)
        
        ciclo_atual = db["config"].get_ciclo_padrao()
        ciclo_field = ft.TextField(label="Ciclo padrão (dias)", value=str(ciclo_atual), width=200)
        
        voltar_btn = ft.ElevatedButton("◀ Voltar", on_click=lambda e: mostrar_tela_inicial())
        
        def salvar_config(e):
            try:
                novo_ciclo = int(ciclo_field.value)
                if novo_ciclo <= 0:
                    mostrar_mensagem("Erro", "Ciclo deve ser maior que zero", True)
                    return
                
                db["config"].set_ciclo_padrao(novo_ciclo)
                mostrar_mensagem("Sucesso", f"Ciclo alterado para {novo_ciclo} dias", False)
                mostrar_tela_inicial()
            except ValueError:
                mostrar_mensagem("Erro", "Digite um número válido", True)
        
        salvar_btn = ft.ElevatedButton("💾 Salvar", on_click=salvar_config)
        
        content_area.controls.append(titulo_tela)
        content_area.controls.append(ciclo_field)
        content_area.controls.append(ft.Row([salvar_btn, voltar_btn], spacing=10))
        page.update()
    
    # ========== TELA DE REMOVER APLICAÇÃO ==========
    def remover_click(e):
        content_area.controls.clear()
        
        titulo_tela = ft.Text("🗑️ Remover aplicação", size=20, weight=ft.FontWeight.BOLD)
        
        aplicacoes = db["service"].listar_todas()
        
        if not aplicacoes:
            content_area.controls.append(titulo_tela)
            content_area.controls.append(ft.Text("📭 Nenhuma aplicação registrada."))
            voltar_btn = ft.ElevatedButton("◀ Voltar", on_click=lambda e: mostrar_tela_inicial())
            content_area.controls.append(voltar_btn)
            page.update()
            return
        
        # Criar dropdown com aplicações
        opcoes = []
        for i, app in enumerate(aplicacoes):
            opcoes.append(ft.dropdown.Option(f"{i+1}. {app.data} - {app.ml}ml - {app.lado}"))
        
        app_dropdown = ft.Dropdown(
            label="Selecione a aplicação",
            options=opcoes,
            width=400
        )
        
        voltar_btn = ft.ElevatedButton("◀ Voltar", on_click=lambda e: mostrar_tela_inicial())
        
        def confirmar_remocao(e):
            if not app_dropdown.value:
                mostrar_mensagem("Aviso", "Selecione uma aplicação", True)
                return
            
            idx = int(app_dropdown.value.split(".")[0]) - 1
            app_remover = aplicacoes[idx]
            
            # Confirmação
            def deletar(e):
                # Remove evento do Google se for a última aplicação
                if app_remover == aplicacoes[-1] and db["logado"] and db["auth"].service:
                    evento_id = db["events"].buscar_evento_por_data(app_remover.proxima_data)
                    if evento_id:
                        db["auth"].deletar_evento(evento_id)
                        db["events"].deletar_evento_por_data(app_remover.proxima_data)
                
                db["service"].repositorio.remover(app_remover)
                mostrar_mensagem("Sucesso", "Aplicação removida!", False)
                mostrar_tela_inicial()
            
            # Diálogo de confirmação
            confirmar_dialog = ft.AlertDialog(
                title=ft.Text("Confirmar exclusão"),
                content=ft.Text(f"Tem certeza que deseja remover {app_remover.data} - {app_remover.ml}ml?"),
                actions=[
                    ft.TextButton("Cancelar", on_click=lambda e: page.close_dialog()),
                    ft.TextButton("Excluir", on_click=deletar),
                ],
                actions_alignment=ft.MainAxisAlignment.END
            )
            page.dialog = confirmar_dialog
            confirmar_dialog.open = True
            page.update()
        
        remover_btn = ft.ElevatedButton("🗑️ Remover", on_click=confirmar_remocao, bgcolor=ft.Colors.RED)
        
        content_area.controls.append(titulo_tela)
        content_area.controls.append(app_dropdown)
        content_area.controls.append(ft.Row([remover_btn, voltar_btn], spacing=10))
        page.update()
    
    # ========== SAIR ==========
    def sair_click(e):
        page.window_close()
    
    # ========== INICIALIZA ==========
    mostrar_tela_inicial()

if __name__ == "__main__":
    ft.app(target=main, port=8555, view=ft.AppView.FLET_APP)