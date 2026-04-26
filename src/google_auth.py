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
    
    def criar_evento(self, titulo, data_inicio, data_fim, descricao=""):
        """Cria um evento no Google Calendar"""
        if not self.service:
            self.autenticar()
        
        evento = {
            'summary': titulo,
            'description': descricao,
            'start': {
                'dateTime': data_inicio,
                'timeZone': 'America/Sao_Paulo',
            },
            'end': {
                'dateTime': data_fim,
                'timeZone': 'America/Sao_Paulo',
            },
        }
        
        evento_criado = self.service.events().insert(calendarId='primary', body=evento).execute()
        print(f"   📅 Evento criado: {evento_criado.get('htmlLink')}")
        return evento_criado.get('htmlLink')
    
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