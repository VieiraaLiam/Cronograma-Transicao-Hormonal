"""Cronograma TH - Ponto de entrada com Google Agenda real"""

import sys
import os

from google import auth

# Adiciona a pasta src ao PATH
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "src"))

from google_auth import GoogleAuth
from aplicacao_service import AplicacaoService
from datetime import datetime
from config_repository import ConfigRepository
from nota_repository import NotaRepository
from google_events_repository import GoogleEventsRepository

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
    print("5. 📝 Adicionar nota ao diário")
    print("6. 🔍 Ver notas de um dia")
    print("7. ⚙️ Configurações (alterar ciclo padrão)")
    print("8. 🚪 Sair")
    print("9. 🗑️  Excluir aplicação")

def registrar_aplicacao(service, auth):
    print("\n📝 NOVA APLICAÇÃO")
    print("-" * 30)
    
    config_repo = ConfigRepository()
    data = input("Data (dd/mm/aaaa) [hoje]: ").strip()
    if not data:
        data = datetime.now().strftime("%d/%m/%Y")
    # Verifica se a data não é futura
    data_obj = datetime.strptime(data, "%d/%m/%Y")
    hoje = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)

    if data_obj > hoje:
        print(f"\n❌ Erro: Não é possível registrar aplicação no futuro!")
        print(f"   Data informada: {data}")
        print(f"   Data atual: {hoje.strftime('%d/%m/%Y')}")
        print("   Use a data de hoje ou uma data passada.\n")
        return  # Sai da função sem registrar

    try:
        ml = float(input("Dosagem (ml): ").strip())
        lado = input("Lado (direito/esquerdo): ").strip().lower()
        ciclo = config_repo.get_ciclo_padrao()
        notas = input("Notas (opcional): ").strip()
        
        # Registrar a aplicação (o service já calcula a proxima_data internamente)
        app = service.registrar(data, ml, lado, notas)
        print(f"\n✅ Aplicação registrada com sucesso!")
        
        # Usar a proxima_data que veio do DTO
        proxima = app.proxima_data
        dias = service.calcular_dias_restantes(data, ciclo)
        print(f"📅 Próxima aplicação: {proxima} (em {dias} dias)")
        
        # Se estiver logado no Google, cria evento na agenda
        if auth and auth.service:
            try:
                # Usa a proxima_data do DTO
                data_evento = datetime.strptime(proxima, "%d/%m/%Y")
                data_inicio = data_evento.strftime("%Y-%m-%d")
                data_fim = data_evento.strftime("%Y-%m-%d")
                
                titulo = f"💉 Próxima aplicação: {app.ml}ml no {app.lado}"
                descricao = f"Ciclo: {app.ciclo_dias} dias"
                
                evento_link = auth.criar_evento(titulo, data_inicio, data_fim, descricao)
                
                # Salva o ID do evento localmente
                if evento_link:
                    events_repo = GoogleEventsRepository()
                    events_repo.salvar_evento(proxima, evento_link)
                    print(f"   📅 Evento criado no Google Agenda para {proxima}")
                
            except Exception as e:
                print(f"   ⚠️ Erro ao criar evento no Google: {e}")
        
    except ValueError as e:
        print(f"\n❌ Erro: {e}")

def excluir_aplicacao(service, auth):
    print("\n🗑️ REMOVER APLICAÇÃO")
    print("-" * 30)
    
    aplicacoes = service.listar_todas()
    if not aplicacoes:
        print("📭 Nenhuma aplicação registrada.")
        return
    
    # Mostra lista numerada
    print("\n📋 Aplicações registradas:")
    for i, app in enumerate(aplicacoes):
        print(f"{i+1}. 📅 {app.data} | 💉 {app.ml}ml | 👤 {app.lado} | 🔄 ciclo {app.ciclo_dias}d")
        if app.notas:
            print(f"   📝 Notas: {app.notas[:50]}...")
    
    try:
        escolha = int(input("\n👉 Número da aplicação a remover: ")) - 1
        if escolha < 0 or escolha >= len(aplicacoes):
            print("❌ Número inválido.")
            return
        
        app_remover = aplicacoes[escolha]
        
        # Confirmação
        print(f"\n⚠️ ATENÇÃO: Você está removendo:")
        print(f"   📅 Data: {app_remover.data}")
        print(f"   💉 Dosagem: {app_remover.ml}ml")
        print(f"   👤 Lado: {app_remover.lado}")
        
        confirmar = input("\n❓ Confirmar exclusão? (s/n): ").strip().lower()
        if confirmar != 's':
            print("❌ Exclusão cancelada.")
            return
        
        # Se for a ÚLTIMA aplicação (mais recente), deletar evento futuro no Google
        if app_remover == aplicacoes[-1] and auth and auth.service:
            from google_events_repository import GoogleEventsRepository
            events_repo = GoogleEventsRepository()
            evento_id = events_repo.buscar_evento_por_data(app_remover.proxima_data)
            if evento_id:
                print(f"\n🗑️ Deletando evento do Google Agenda...")
                auth.deletar_evento(evento_id)
                events_repo.deletar_evento_por_data(app_remover.proxima_data)
                print(f"   ✅ Evento removido do Google Agenda")
        
        # Remove do repositório local
        service.repositorio.remover(app_remover)
        print(f"\n✅ Aplicação removida com sucesso!")
        
    except ValueError:
        print("❌ Valor inválido. Digite um número.")

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
    
def configuracoes(auth):
    from aplicacao_service import AplicacaoService
    from google_events_repository import GoogleEventsRepository
    from datetime import datetime, timedelta
    
    config_repo = ConfigRepository()
    ciclo_atual = config_repo.get_ciclo_padrao()
    print(f"\n⚙️ CONFIGURAÇÕES")
    print(f"Ciclo padrão atual: {ciclo_atual} dias")
    resposta = input("Deseja alterar? (s/n): ").strip().lower()
    
    if resposta == 's':
        novo_ciclo = int(input("Novo ciclo padrão (dias): "))
        
        # Verifica se há aplicações registradas
        service = AplicacaoService()
        aplicacoes = service.listar_todas()
        
        if aplicacoes:
            # Pega a última aplicação (mais recente)
            ultima_app = aplicacoes[-1]
            data_ultima = ultima_app.data
            
            # Calcula a nova próxima data
            data_obj = datetime.strptime(data_ultima, "%d/%m/%Y")
            nova_proxima_data = (data_obj + timedelta(days=novo_ciclo)).strftime("%d/%m/%Y")
            
            print(f"\n📅 Última aplicação: {data_ultima}")
            print(f"   Próxima dose ANTIGA: {ultima_app.proxima_data}")
            print(f"   Próxima dose NOVA: {nova_proxima_data}")
            
            # Busca o evento antigo pelo ID
            events_repo = GoogleEventsRepository()
            evento_id_antigo = events_repo.buscar_evento_por_data(ultima_app.proxima_data)
            
            if evento_id_antigo and auth and auth.service:
                # Deleta o evento antigo no Google
                print(f"\n🗑️ Deletando evento antigo do Google Agenda...")
                auth.deletar_evento(evento_id_antigo)
                events_repo.deletar_evento_por_data(ultima_app.proxima_data)
                
                # Cria novo evento com a nova data
                data_inicio = nova_proxima_data.replace("/", "-")  # "dd/mm/yyyy" -> "dd-mm-yyyy"
                data_inicio_formatada = datetime.strptime(nova_proxima_data, "%d/%m/%Y").strftime("%Y-%m-%d")
                
                titulo = f"💉 Próxima aplicação: {ultima_app.ml}ml no {ultima_app.lado}"
                descricao = f"Ciclo: {novo_ciclo} dias"
                
                print(f"📅 Criando novo evento para {nova_proxima_data}...")
                novo_evento_id = auth.criar_evento(titulo, data_inicio_formatada, data_inicio_formatada, descricao)
                
                if novo_evento_id:
                    events_repo.salvar_evento(nova_proxima_data, novo_evento_id)
                    print(f"   ✅ Novo evento criado com sucesso!")
            else:
                print(f"\n⚠️ Nenhum evento encontrado no Google para atualizar.")
            
            # Atualiza a proxima_data na última aplicação
            ultima_app.proxima_data = nova_proxima_data
            service.repositorio.atualizar(ultima_app)
            print(f"\n✅ Próxima data atualizada no histórico local.")
        
        # Altera o ciclo padrão
        config_repo.set_ciclo_padrao(novo_ciclo)
        print(f"\n✅ Ciclo padrão alterado para {novo_ciclo} dias")
    
def adicionar_nota():
    print("\n📝 ADICIONAR NOTA")
    print("-" * 30)
    
    data = input("Data (dd/mm/aaaa) [hoje]: ").strip()
    if not data:
        data = datetime.now().strftime("%d/%m/%Y")
    
    texto = input("Nota: ").strip()
    if texto:
        repo = NotaRepository()
        repo.adicionar(data, texto)
        print("✅ Nota adicionada com sucesso!")
    else:
        print("❌ Nota vazia, não foi salva.")
    

def ver_notas_do_dia():
    print("\n🔍 VER NOTAS DO DIA")
    print("-" * 30)
    
    data = input("Data (dd/mm/aaaa): ").strip()
    if not data:
        print("❌ Data não informada.")
        return
    
    repo = NotaRepository()
    notas = repo.listar_por_data(data)
    
    if not notas:
        print(f"📭 Nenhuma nota encontrada para {data}")
        return
    
    print(f"\n📝 Notas de {data}:")
    for i, nota in enumerate(notas, 1):
        print(f"  {i}. {nota.horario} - {nota.texto}")

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
            adicionar_nota()
        
        elif opcao == "6":
            ver_notas_do_dia()
        
        elif opcao == "7":
            configuracoes(auth)
        
        elif opcao == "8":
            print("\n👋 Saindo... Até a próxima!")
            break
        elif opcao == "9":
            excluir_aplicacao(app_service, auth)

        input("\n⏎ Pressione Enter para continuar...")
        limpar_terminal()

if __name__ == "__main__":
    main()