"""Cronograma TH - Ponto de entrada com Google Agenda real"""

import sys
import os

# Adiciona a pasta src ao PATH
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "src"))

from google_auth import GoogleAuth
from aplicacao_service import AplicacaoService
from datetime import datetime

def limpar_terminal():
    print("\n" * 2)

def mostrar_menu_principal(esta_logado: bool):
    print(f"\n{'='*50}")
    print(f"🏥 CRONOGRAMA TH")
    print(f"{'='*50}")
    status = "✅ Logado" if esta_logado else "❌ Não logado"
    print(f"Status Google: {status}")
    print("-" * 50)
    print("1. 🔐 Fazer login no Google")
    print("2. 📝 Registrar nova aplicação")
    print("3. 📋 Ver histórico")
    print("4. 🔍 Buscar por data")
    print("5. 🚪 Sair")

def registrar_aplicacao(service, auth):
    print("\n📝 NOVA APLICAÇÃO")
    print("-" * 30)
    
    data = input("Data (dd/mm/aaaa) [hoje]: ").strip()
    if not data:
        data = datetime.now().strftime("%d/%m/%Y")
    
    try:
        ml = float(input("Dosagem (ml): ").strip())
        lado = input("Lado (direito/esquerdo): ").strip().lower()
        ciclo = int(input("Ciclo (dias): ").strip())
        notas = input("Notas (opcional): ").strip()
        
        app = service.registrar(data, ml, lado, ciclo, notas)
        print(f"\n✅ Aplicação registrada com sucesso!")
        
        proxima = service.calcular_proxima_data(data, ciclo)
        dias = service.calcular_dias_restantes(data, ciclo)
        print(f"📅 Próxima aplicação: {proxima} (em {dias} dias)")
        
        # Se estiver logado no Google, cria evento na agenda
        if auth and auth.service:
            try:
                data_evento = datetime.strptime(app.data, "%d/%m/%Y")
                data_inicio = data_evento.strftime("%Y-%m-%dT09:00:00")
                data_fim = data_evento.strftime("%Y-%m-%dT09:30:00")
                
                titulo = f"💉 Aplicação hormonal: {app.ml}ml no {app.lado}"
                descricao = f"Ciclo: {app.ciclo_dias} dias"
                
                auth.criar_evento(titulo, data_inicio, data_fim, descricao)
            except Exception as e:
                print(f"   ⚠️ Erro ao criar evento no Google: {e}")
        
    except ValueError as e:
        print(f"\n❌ Erro: {e}")

def ver_historico(service):
    aplicacoes = service.listar_todas()
    
    if not aplicacoes:
        print("\n📭 Nenhuma aplicação registrada ainda.")
        return
    
    print("\n📋 HISTÓRICO DE APLICAÇÕES")
    print("-" * 50)
    
    for app in aplicacoes[::-1]:
        print(f"📅 {app.data} | 💉 {app.ml}ml | 👤 {app.lado} | 🔄 {app.ciclo_dias}d")
        if app.notas:
            print(f"   📝 Notas: {app.notas}")
        print("-" * 30)

def buscar_por_data(service):
    data = input("\n🔍 Digite a data (dd/mm/aaaa): ").strip()
    aplicacoes = service.buscar_por_data(data)
    
    if not aplicacoes:
        print(f"📭 Nenhuma aplicação encontrada em {data}")
        return
    
    print(f"\n📅 Aplicações em {data}:")
    for app in aplicacoes:
        print(f"   💉 {app.ml}ml | 👤 {app.lado} | 🔄 ciclo {app.ciclo_dias}d")

def main():
    auth = GoogleAuth()
    app_service = AplicacaoService()
    logado = False
    
    while True:
        mostrar_menu_principal(logado)
        opcao = input("\n👉 Escolha uma opção: ").strip()
        
        if opcao == "1":
            logado = auth.fazer_login()
        
        elif opcao == "2":
            if not logado:
                print("\n⚠️ Você precisa fazer login no Google primeiro!")
                print("   Opção 1 do menu")
            else:
                registrar_aplicacao(app_service, auth)
        
        elif opcao == "3":
            ver_historico(app_service)
        
        elif opcao == "4":
            buscar_por_data(app_service)
        
        elif opcao == "5":
            print("\n👋 Até logo!")
            break
        
        else:
            print("\n❌ Opção inválida!")
        
        input("\n⏎ Pressione Enter para continuar...")
        limpar_terminal()

if __name__ == "__main__":
    main()