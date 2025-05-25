Sistema de Triangulação de Motos - IoT Prototype
================================================

📋 Descrição do Projeto
-----------------------

Este protótipo simula um sistema de gerenciamento inteligente de motos utilizando tecnologia IoT e sensores RFID para triangulação de posição. O sistema detecta a presença de motos em diferentes pontos de um pátio através de sensores RFID simulados e envia os dados para uma API.

🎯 Problema Resolvido
---------------------

**Desafio**: Localização precisa e monitoramento em tempo real de motos em pátios da Mottu.

**Solução**: Sistema de triangulação usando múltiplos sensores RFID estrategicamente posicionados que coletam dados de intensidade de sinal para determinar a posição aproximada de cada veículo.

🛠 Tecnologias Utilizadas
-------------------------

### Hardware (Simulado no Wokwi)

-   **ESP32**: Microcontrolador principal com conectividade WiFi
-   **Sensores RFID RC522** (simulados com botões): Detecção de tags RFID das motos
-   **LEDs**: Feedback visual das detecções
-   **Resistores**: Proteção dos LEDs

### Software e Protocolos

-   **C++ (Arduino IDE)**: Linguagem de programação
-   **WiFi**: Conectividade sem fio
-   **HTTP/REST API**: Comunicação com servidor
-   **JSON**: Formato de dados
-   **Firebase**: Montagem do dashboard

🔧 Como Usar no Wokwi
---------------------

### 1\. Link do Projeto

1.  Acesse [Wokwi.com](https://wokwi.com/projects/431893375220118529)

### 2\. Configurar API

No código, altere as seguintes variáveis:

```
const char* apiUrl = "http://172.178.12.27:8080/api/rfid"; // No momento em que está lendo, essa VM foi desativada

```
Clone a API em: linkapi

E substitua por:
```
http://localhost:5007/api/rfid // ou a porta configurada
```
Agora é só rodar!

Obs: o Wokwi sofre com alguns problemas de conexão, então, no início você pode receber códigos de erro -11.

📊 Dados Enviados para API
--------------------------

O sistema envia dados no formato JSON:

```
{
  "rfid": "A1B2C3D4E5F6G7H8",
  "sensorId": 1,
  "potenciaSinal": 13
}

```

🔄 Funcionamento do Sistema
---------------------------

### Fluxo de Operação

1.  **Detecção**: Sensor RFID detecta presença de moto (simulado por botão)
2.  **Coleta**: ESP32 coleta dados (ID RFID, ID do sensor, potência do sinal)
3.  **Processamento**: Dados são formatados em JSON
4.  **Transmissão**: Envio via HTTP POST para API na nuvem
5.  **Feedback**: LEDs indicam status da operação

### Algoritmo de Triangulação (Conceito)

-   Múltiplos sensores captam o mesmo RFID com intensidades diferentes
-   API calcula posição baseada na intensidade do sinal (RSSI)
-   Triangulação matemática determina localização de acordo com a localização do sensor

📡 Protocolo de Comunicação
---------------------------

### Requisição HTTP

```
POST /api/rfid
Content-Type: application/json

{
  "rfid": "string",
  "sensorId": number,
  "potenciaSinal": number
}

```

### Feedback Visual

-   LED aceso: indica conexão com wifi
-   Ao realizar leitura, caso pisque: sucesso

🏗 Arquitetura do Sistema
-------------------------

```
[Motos c/ RFID] → [Sensores RC522] → [ESP32] → [WiFi] → [API Cloud] → [Dashboard]

```

📊 Dashboard
----------------
Para a montagem do dashboard (análise de leituras) foi utilizado o Firebase para captação dos dados em tempo real com Realtime Database + Web App para visualização de dados.

### Métricas e funcionalidades
- Leituras bem sucedidas ou não
- Total de leituras
- Taxa de sucesso
- Gráfico de leitura por tempo
- Histórico de leituras

### Como ver o dashboard?
- Para visualização do dashboard você precisa clonar o projeto, abrir o Index HTML
- Instale a extensão Live Server
- Inicie o servidor
- Acesse a URL disponibilizada (provavelmente localhost:5500)

🔮 Aplicações Futuras
---------------------

### Expandibilidade

-   Algoritmos de ML para previsão de demanda
-   Notificações push para usuários
-   Análise de padrões de uso

### Melhorias Técnicas

-   Protocolo MQTT para menor latência
-   Criptografia de dados
-   Bateria e energia solar
-   Sensores adicionais (GPS, acelerômetro)

📋 Resultados Parciais
----------------------

✅ **Concluído**:

-   Simulação funcional no Wokwi
-   Comunicação HTTP com API
-   Dados mockados realistas
-   Feedback visual adequado
-   Estrutura modular e expansível
-   Simulação de dados em tempo real com Firebase

🔄 **Em Desenvolvimento**:

-   Algoritmo de triangulação refinado
-   Testes de campo com hardware real

🚀 Próximos Passos
------------------

1.  Testes com hardware real
2.  Algoritmo de triangulação mais preciso
3.  API de consulta de histórico

* * * * *

**Desenvolvido para**: DISRUPTIVE ARCHITECTURES: IOT, IOB & GENERATIVE IA\
**Tecnologias**: IoT, ESP32, RFID, HTTP, JSON, Wokwi\
**Objetivo**: Protótipo funcional de sistema de triangulação de motos
