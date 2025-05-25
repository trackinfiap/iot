import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
import requests
import json
import time
import random
from datetime import datetime

FIREBASE_URL = "https://trackin-dashboard-default-rtdb.firebaseio.com/"
API_URL = "http://localhost:5007/api/rfid"

rfids = [
    "ECAAAAAAAAAAAAAAAAAAAAAAMOTTU20293",
    "EC04ABC10000", 
    "string",
    "E200001161072C05"
]

class RFIDSimulator:
    def __init__(self):
        self.rfid_index = 0
        self.total_leituras = 0
        self.leituras_sucesso = 0
        self.leituras_erro = 0
        self.init_firebase()
        
    def init_firebase(self):
        """Inicializa conexão com Firebase usando token de acesso"""
        try:
            cred = credentials.Certificate({
                "type": "service_account",
                "project_id": "trackin-dashboard",
                "private_key_id": "dummy",
                "private_key": "-----BEGIN PRIVATE KEY-----\nMIIEvQIBADANBgkqhkiG9w0BAQEFAASCBKcwggSjAgEAAoIBAQC7VJTUt9Us8cKB\n-----END PRIVATE KEY-----\n",
                "client_email": "dummy@trackin-dashboard.iam.gserviceaccount.com",
                "client_id": "dummy",
                "auth_uri": "https://accounts.google.com/o/oauth2/auth",
                "token_uri": "https://oauth2.googleapis.com/token"
            })
            
            firebase_admin.initialize_app(options={
                'databaseURL': FIREBASE_URL,
                'databaseAuthVariableOverride': {
                    'uid': 'python-simulator'
                }
            })
            
            print("✅ Firebase inicializado com sucesso!")
            
        except Exception as e:
            print(f"❌ Erro ao inicializar Firebase: {e}")
            print("🔧 Usando método alternativo...")
            self.use_direct_requests = True
    
    def get_current_timestamp(self):
        """Retorna timestamp atual em milissegundos"""
        return int(time.time() * 1000)
    
    def send_to_api(self, rfid, sensor_id, potencia):
        """Envia dados para a API (simula o comportamento do ESP32)"""
        try:
            payload = {
                "rfid": rfid,
                "sensorId": sensor_id,
                "potenciaSinal": potencia
            }
            
            print(f"📤 Enviando para API: {json.dumps(payload)}")
            
            response = requests.post(
                API_URL,
                json=payload,
                headers={"Content-Type": "application/json"},
                timeout=10
            )
            
            print(f"📊 Código de resposta HTTP: {response.status_code}")
            
            if 200 <= response.status_code < 300:
                print(f"✅ Resposta da API: {response.text}")
                return True
            else:
                print(f"❌ Erro no envio! Código: {response.status_code}")
                return False
                
        except requests.exceptions.RequestException as e:
            print(f"❌ Erro de conexão com API: {e}")
            return False
        except Exception as e:
            print(f"❌ Erro inesperado na API: {e}")
            return False
    
    def send_to_firebase_direct(self, rfid, sensor_id, potencia, api_success, timestamp):
        """Envia dados para Firebase usando requests direto"""
        try:
            reading_data = {
                "rfid": rfid,
                "sensorId": sensor_id,
                "potenciaSinal": potencia,
                "timestamp": timestamp,
                "apiSuccess": api_success,
                "status": "sucesso" if api_success else "erro"
            }
            
            reading_url = f"{FIREBASE_URL}leituras/{timestamp}.json?auth=ItLES2ylxrUzMOGBC1Vp5jajZxrHpr5eHFDMYbKP"
            
            response = requests.put(reading_url, json=reading_data)
            
            if response.status_code == 200:
                print("✅ Leitura enviada para Firebase!")
                return True
            else:
                print(f"❌ Erro ao enviar leitura: {response.status_code}")
                return False
                
        except Exception as e:
            print(f"❌ Erro ao enviar para Firebase: {e}")
            return False
    
    def send_to_firebase(self, rfid, sensor_id, potencia, api_success):
        """Envia dados para Firebase"""
        timestamp = self.get_current_timestamp()
        
        try:
            # tentativa de usar o SDK do Firebase primeiro
            ref = db.reference('leituras')
            
            reading_data = {
                "rfid": rfid,
                "sensorId": sensor_id,
                "potenciaSinal": potencia,
                "timestamp": timestamp,
                "apiSuccess": api_success,
                "status": "sucesso" if api_success else "erro"
            }
            
            ref.child(str(timestamp)).set(reading_data)
            print("✅ Dados enviados para Firebase com sucesso!")
            return True
            
        except Exception as e:
            print(f"⚠️ SDK Firebase falhou, usando método direto: {e}")
            # fallback para requests direto
            return self.send_to_firebase_direct(rfid, sensor_id, potencia, api_success, timestamp)
    
    def update_metrics_direct(self):
        """Atualiza métricas usando requests direto"""
        try:
            taxa_sucesso = (self.leituras_sucesso / self.total_leituras * 100) if self.total_leituras > 0 else 0
            
            metrics_data = {
                "totalLeituras": self.total_leituras,
                "leiturasSucesso": self.leituras_sucesso,
                "leiturasErro": self.leituras_erro,
                "taxaSucesso": round(taxa_sucesso, 2),
                "ultimaAtualizacao": self.get_current_timestamp()
            }
            
            metrics_url = f"{FIREBASE_URL}metricas.json?auth=ItLES2ylxrUzMOGBC1Vp5jajZxrHpr5eHFDMYbKP"
            
            response = requests.put(metrics_url, json=metrics_data)
            
            if response.status_code == 200:
                print("📊 Métricas atualizadas no Firebase!")
                return True
            else:
                print(f"❌ Erro ao atualizar métricas: {response.status_code}")
                return False
                
        except Exception as e:
            print(f"❌ Erro ao atualizar métricas: {e}")
            return False
    
    def update_metrics(self):
        """Atualiza métricas no Firebase"""
        try:
            # tenta usar o SDK primeiro
            ref = db.reference('metricas')
            
            taxa_sucesso = (self.leituras_sucesso / self.total_leituras * 100) if self.total_leituras > 0 else 0
            
            metrics_data = {
                "totalLeituras": self.total_leituras,
                "leiturasSucesso": self.leituras_sucesso,  
                "leiturasErro": self.leituras_erro,
                "taxaSucesso": round(taxa_sucesso, 2),
                "ultimaAtualizacao": self.get_current_timestamp()
            }
            
            ref.set(metrics_data)
            print("📊 Métricas atualizadas no Firebase!")
            
        except Exception as e:
            print(f"⚠️ SDK Firebase falhou para métricas, usando método direto: {e}")
            self.update_metrics_direct()
    
    def simulate_reading(self):
        """Simula uma leitura RFID"""
        current_rfid = rfids[self.rfid_index]
        self.rfid_index = (self.rfid_index + 1) % len(rfids)
        
        sensor_id = 1
        potencia = random.randint(-60, -30)
        
        print(f"\n🔍 Nova leitura RFID: {current_rfid}")
        print(f"📡 Potência do sinal: {potencia} dBm")
        
        api_success = self.send_to_api(current_rfid, sensor_id, potencia)
        
        firebase_success = self.send_to_firebase(current_rfid, sensor_id, potencia, api_success)
        
        self.total_leituras += 1
        if api_success:
            self.leituras_sucesso += 1
        else:
            self.leituras_erro += 1
            
        self.update_metrics()
        
        if api_success:
            print("✅ Status: SUCESSO")
        else:
            print("❌ Status: ERRO")
        
        print(f"📈 Métricas: {self.leituras_sucesso}/{self.total_leituras} sucessos ({(self.leituras_sucesso/self.total_leituras*100):.1f}%)")
    
    def run_simulation(self, interval=3, max_readings=None):
        """Executa simulação contínua"""
        print("🚀 Iniciando simulação RFID...")
        print(f"⏱️ Intervalo entre leituras: {interval}s")
        
        if max_readings:
            print(f"🎯 Máximo de leituras: {max_readings}")
        else:
            print("♾️ Simulação contínua (Ctrl+C para parar)")
        
        reading_count = 0
        
        try:
            while True:
                self.simulate_reading()
                reading_count += 1
                
                if max_readings and reading_count >= max_readings:
                    print(f"\n🏁 Simulação concluída! {reading_count} leituras realizadas.")
                    break
                
                print(f"\n⏳ Aguardando {interval}s para próxima leitura...")
                time.sleep(interval)
                
        except KeyboardInterrupt:
            print(f"\n⏹️ Simulação interrompida pelo usuário!")
            print(f"📊 Total de leituras realizadas: {reading_count}")
        except Exception as e:
            print(f"\n❌ Erro na simulação: {e}")

def main():
    """Função principal"""
    print("=" * 50)
    print("🏍️  SIMULADOR RFID - FIREBASE")
    print("=" * 50)
    
    simulator = RFIDSimulator()
    
    print("\n⚙️ Configurações:")
    print("1. Simulação contínua (padrão)")
    print("2. Número específico de leituras")
    print("3. Teste único")
    
    try:
        choice = input("\nEscolha uma opção (1-3) [1]: ").strip()
        
        if choice == "2":
            max_readings = int(input("Quantas leituras? "))
            interval = float(input("Intervalo entre leituras (segundos) [3]: ") or "3")
            simulator.run_simulation(interval=interval, max_readings=max_readings)
        elif choice == "3":
            simulator.simulate_reading()
        else:
            interval = float(input("Intervalo entre leituras (segundos) [3]: ") or "3")
            simulator.run_simulation(interval=interval)
            
    except KeyboardInterrupt:
        print("\n👋 Simulação encerrada!")
    except ValueError:
        print("❌ Valor inválido! Usando configuração padrão...")
        simulator.run_simulation()

if __name__ == "__main__":
    main()