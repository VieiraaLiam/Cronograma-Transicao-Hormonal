"""GoogleAuth - Autenticação real com Google Agenda"""

import os
import pickle
from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

# Escopo: permissão para gerenciar eventos do Google Calendar
SCOPES = ['https://www.googleapis.com/auth/calendar.events']

class GoogleAuth:
    def __init__(self, credenciais_arquivo="credentials.json", token_arquivo="data/token.pickle"):
        self.credenciais_arquivo = credenciais_arquivo
        self.token_arquivo = token_arquivo
        self.creds = None
        self.service = None
    
    def autenticar(self):
        """Autentica com Google e retorna o serviço do Calendar"""
        # Carrega token salvo
        if os.path.exists(self.token_arquivo):
            with open(self.token_arquivo, 'rb') as token:
                self.creds = pickle.load(token)
        
        # Se token não existe ou expirou, faz login
        if not self.creds or not self.creds.valid:
            if self.creds and self.creds.expired and self.creds.refresh_token:
                self.creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    self.credenciais_arquivo, SCOPES)
                self.creds = flow.run_local_server(port=0)
            
            # Salva token para próxima vez
            with open(self.token_arquivo, 'wb') as token:
                pickle.dump(self.creds, token)
        
        # Cria o serviço do Google Calendar
        self.service = build('calendar', 'v3', credentials=self.creds)
        return self.service
    
    def esta_logado(self):
        """Verifica se existe token salvo (usuário já autenticou antes)"""
        if os.path.exists(self.token_arquivo):
            return True
        return False
    
    def criar_evento(self, titulo, data_inicio, data_fim, descricao=""):
        """Cria um evento de dia inteiro no Google Calendar"""
        if not self.service:
            self.autenticar()
    
        evento = {
            'summary': titulo,
            'description': descricao,
            'start': {
                'date': data_inicio,
            },
            'end': {
                'date': data_fim,
            },
        }
    
        evento_criado = self.service.events().insert(calendarId='primary', body=evento).execute()
        print(f"   📅 Evento de dia inteiro criado: {evento_criado.get('htmlLink')}")
        return evento_criado.get('id')
    
    def deletar_evento(self, event_id):
        if not self.service:
            self.autenticar()
    
        try:
            self.service.events().delete(
            calendarId='primary',
            eventId=event_id
        ).execute()
            return True
        except Exception as e:
            print(f"Erro ao deletar evento: {e}")
        return False
    
    def atualizar_evento(self, event_id, nova_data_inicio, nova_data_fim, titulo=None, descricao=None):
        if not self.service:
            self.autenticar()
    
        try:
            # Busca o evento existente
            evento = self.service.events().get(
                calendarId='primary',
                eventId=event_id
            ).execute()
            
            # Atualiza os campos
            evento['start']['dateTime'] = nova_data_inicio
            evento['end']['dateTime'] = nova_data_fim
            
            if titulo:
                evento['summary'] = titulo
            if descricao:
                evento['description'] = descricao
            
            # Envia a atualização
            evento_atualizado = self.service.events().update(
                calendarId='primary',
                eventId=event_id,
                body=evento
            ).execute()
            
            return evento_atualizado
                
        except Exception as e:
            print(f"Erro ao atualizar evento: {e}")
        return None
    
    def fazer_login(self):
        """Método principal para login"""
        try:
            self.autenticar()
            print("\n✅ Autenticado com sucesso no Google!")
            
            # Tenta obter email da conta
            try:
                email = self.creds.id_token.get('email', 'Google Account')
                print(f"   Conta: {email}")
            except:
                pass
            
            return True
        except Exception as e:
            print(f"\n❌ Erro na autenticação: {e}")
            print("\n⚠️ Verifique se:")
            print("   1. O arquivo credentials.json está na pasta correta")
            print("   2. Você ativou a Google Calendar API no Google Cloud")
            print("   3. O escopo correto foi adicionado")
            return False