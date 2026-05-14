"""Cronograma TH - Interface gráfica com Flet (Login e Registro)"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "src"))

import flet as ft
from auth_service import AuthService

# ======================================================
# FUNÇÕES AUXILIARES
# ======================================================

def validar_email(email: str) -> bool:
    if not email:
        return False
    if "@" not in email:
        return False
    partes = email.split("@")
    if len(partes) != 2:
        return False
    dominio = partes[1]
    return "." in dominio and len(dominio.split(".")[-1]) >= 2


# ======================================================
# APLICAÇÃO PRINCIPAL
# ======================================================

def main(page: ft.Page):
    page.title = "Cronograma TH"
    page.theme_mode = ft.ThemeMode.DARK
    page.padding = 20
    page.window_width = 420
    page.window_height = 600
    page.window_resizable = False
    page.bgcolor = ft.colors.BLACK
    
    auth = AuthService()
    usuario_logado = None
    campo_email = None
    campo_senha = None
    texto_erro = None
    senha_visivel = False
    
    # ==================================================
    # TELA DE LOGIN
    # ==================================================
    
    def atualizar_visibilidade_senha():
        nonlocal senha_visivel
        senha_visivel = not senha_visivel
        campo_senha.password = not senha_visivel
        page.update()
    
    def fazer_login(e):
        email = campo_email.value.strip()
        senha = campo_senha.value.strip()
        
        if not validar_email(email):
            texto_erro.value = "❌ Email inválido"
            texto_erro.visible = True
            page.update()
            return
        
        if not senha:
            texto_erro.value = "❌ Senha não pode estar vazia"
            texto_erro.visible = True
            page.update()
            return
        
        usuario = auth.login(email, senha)
        if usuario:
            nonlocal usuario_logado
            usuario_logado = usuario
            texto_erro.visible = False
            page.update()
            mostrar_menu_principal()
        else:
            texto_erro.value = "❌ Email ou senha incorretos"
            texto_erro.visible = True
            page.update()
    
    def abrir_janela_registro(e):
        abrir_janela_registro_dialog()
    
    def mostrar_tela_login():
        nonlocal campo_email, campo_senha, texto_erro
        
        campo_email = ft.TextField(
            label="Email",
            hint_text="usuario@email.com",
            width=300,
            autofocus=True,
        )
        
        campo_senha = ft.TextField(
            label="Senha",
            hint_text="Digite sua senha",
            width=300,
            password=True,
        )
        
        olho_icone = ft.IconButton(
            icon=ft.icons.VISIBILITY,
            on_click=lambda e: atualizar_visibilidade_senha(),
        )
        
        row_senha = ft.Row(
            controls=[campo_senha, olho_icone],
            alignment=ft.MainAxisAlignment.CENTER,
        )
        
        botao_login = ft.ElevatedButton(
            text="ENTRAR",
            width=300,
            height=45,
            on_click=fazer_login,
        )
        
        botao_registrar = ft.TextButton(
            text="Criar nova conta",
            on_click=abrir_janela_registro,
        )
        
        texto_erro = ft.Text(
            color=ft.colors.RED,
            size=12,
            visible=False,
        )
        
        coluna = ft.Column(
            controls=[
                ft.Text("🏥 CRONOGRAMA TH", size=30, weight=ft.FontWeight.BOLD),
                ft.Container(height=40),
                campo_email,
                ft.Container(height=10),
                row_senha,
                ft.Container(height=20),
                botao_login,
                ft.Container(height=10),
                botao_registrar,
                ft.Container(height=20),
                texto_erro,
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        )
        
        page.controls.clear()
        page.add(coluna)
        page.update()
    
    # ==================================================
    # JANELA DE REGISTRO
    # ==================================================
    
    def abrir_janela_registro_dialog():
        campo_email_reg = ft.TextField(
            label="Email",
            hint_text="usuario@email.com",
            width=300,
        )
        
        campo_senha_reg = ft.TextField(
            label="Senha",
            hint_text="Mínimo 8 caracteres",
            width=300,
            password=True,
        )
        
        campo_confirmar_reg = ft.TextField(
            label="Confirmar senha",
            hint_text="Digite a senha novamente",
            width=300,
            password=True,
        )
        
        texto_erro_reg = ft.Text(color=ft.colors.RED, size=12, visible=False)
        
        def alternar_senha(e):
            campo_senha_reg.password = not campo_senha_reg.password
            dialog.update()
        
        def alternar_confirmar(e):
            campo_confirmar_reg.password = not campo_confirmar_reg.password
            dialog.update()
        
        olho_senha = ft.IconButton(icon=ft.icons.VISIBILITY, on_click=alternar_senha)
        olho_confirmar = ft.IconButton(icon=ft.icons.VISIBILITY, on_click=alternar_confirmar)
        
        row_senha_reg = ft.Row([campo_senha_reg, olho_senha], alignment=ft.MainAxisAlignment.CENTER)
        row_confirmar_reg = ft.Row([campo_confirmar_reg, olho_confirmar], alignment=ft.MainAxisAlignment.CENTER)
        
        def criar_conta(e):
            email = campo_email_reg.value.strip()
            senha = campo_senha_reg.value.strip()
            confirmar = campo_confirmar_reg.value.strip()
            
            if not validar_email(email):
                texto_erro_reg.value = "❌ Email inválido"
                texto_erro_reg.visible = True
                dialog.update()
                return
            
            if len(senha) < 8:
                texto_erro_reg.value = "❌ Senha deve ter no mínimo 8 caracteres"
                texto_erro_reg.visible = True
                dialog.update()
                return
            
            if senha != confirmar:
                texto_erro_reg.value = "❌ As senhas não conferem"
                texto_erro_reg.visible = True
                dialog.update()
                return
            
            sucesso = auth.registrar(email, senha)
            if sucesso:
                dialog.open = False
                page.update()
                usuario = auth.login(email, senha)
                if usuario:
                    nonlocal usuario_logado
                    usuario_logado = usuario
                    mostrar_menu_principal()
                else:
                    mostrar_tela_login()
                    texto_erro.value = "✅ Conta criada! Faça login"
                    texto_erro.visible = True
                    page.update()
            else:
                texto_erro_reg.value = "❌ Email já cadastrado"
                texto_erro_reg.visible = True
                dialog.update()
        
        def cancelar(e):
            dialog.open = False
            page.update()
        
        dialog_content = ft.Column(
            controls=[
                ft.Text("📝 CRIAR CONTA", size=20, weight=ft.FontWeight.BOLD),
                ft.Container(height=20),
                campo_email_reg,
                ft.Container(height=10),
                row_senha_reg,
                ft.Container(height=10),
                row_confirmar_reg,
                ft.Container(height=20),
                ft.Row(
                    controls=[
                        ft.ElevatedButton("CRIAR", on_click=criar_conta),
                        ft.TextButton("CANCELAR", on_click=cancelar),
                    ],
                    alignment=ft.MainAxisAlignment.CENTER,
                    spacing=20,
                ),
                ft.Container(height=10),
                texto_erro_reg,
            ],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        )
        
        dialog = ft.AlertDialog(
            title=ft.Text(""),
            content=dialog_content,
            actions_alignment=ft.MainAxisAlignment.CENTER,
        )
        
        page.dialog = dialog
        dialog.open = True
        page.update()
    
    # ==================================================
    # MENU PRINCIPAL
    # ==================================================
    
    def mostrar_menu_principal():
        page.controls.clear()
        
        titulo = ft.Text(f"👤 {usuario_logado.email}", size=16, weight=ft.FontWeight.BOLD)
        
        coluna = ft.Column(
            controls=[
                ft.Text("🏥 CRONOGRAMA TH", size=30, weight=ft.FontWeight.BOLD),
                ft.Container(height=30),
                titulo,
                ft.Text("✅ Logado com sucesso!", color=ft.colors.GREEN),
                ft.Container(height=30),
                ft.ElevatedButton(
                    text="🚪 Sair",
                    on_click=lambda e: mostrar_tela_login(),
                    width=200,
                ),
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        )
        
        page.add(coluna)
        page.update()
    
    # ==================================================
    # INICIALIZA
    # ==================================================
    mostrar_tela_login()


if __name__ == "__main__":
    ft.app(target=main)