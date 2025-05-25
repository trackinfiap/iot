#include <WiFi.h>
#include <HTTPClient.h>
#include <ArduinoJson.h>

// config wifi
const char* ssid = "Wokwi-GUEST";
const char* password = "";

const char* apiUrl = "http://172.178.12.27:8080/api/rfid";

// pinos
const int botaoSensor = 0;  
const int ledStatus = 2;    

// rfids mockados de motos existentes no banco de dados
String rfids[] = {
  "ECAAAAAAAAAAAAAAAAAAAAAAMOTTU20293", 
  "EC04ABC10000", 
  "string",
  "E200001161072C05"
};

int totalRFIDs = sizeof(rfids) / sizeof(rfids[0]);
int rfidIndex = 0;

void setup() {
  Serial.begin(115200);
  pinMode(botaoSensor, INPUT_PULLUP);
  pinMode(ledStatus, OUTPUT);
  digitalWrite(ledStatus, LOW);
  
  // conexao com wifi
  WiFi.begin(ssid, password);
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    digitalWrite(ledStatus, HIGH);
    delay(500);
    digitalWrite(ledStatus, LOW);
  }
  digitalWrite(ledStatus, HIGH);      // se led aceso = conectado
  Serial.println("Conectado ao Wi-Fi!");
}

void loop() {
  if (digitalRead(botaoSensor) == LOW) { // botao pressionado
    String currentRFID = rfids[rfidIndex];
    rfidIndex = (rfidIndex + 1) % totalRFIDs; 
    
    sendRFIDData(currentRFID, 1, random(-30, -60));
    
    delay(1000);
  }
}

void sendRFIDData(String rfid, int sensorId, int potencia) {
  if (WiFi.status() == WL_CONNECTED) {
    StaticJsonDocument<200> doc;
    doc["rfid"] = rfid;
    doc["sensorId"] = sensorId;
    doc["potenciaSinal"] = potencia;
    
    String json;
    serializeJson(doc, json);
    
    HTTPClient http;
    http.begin(apiUrl);
    http.addHeader("Content-Type", "application/json");
    
    Serial.print("Enviando: ");
    Serial.println(json);
    
    int httpCode = http.POST(json);
    Serial.print("Código de resposta HTTP: ");
    Serial.println(httpCode);
    if (httpCode > 0) {
      String response = http.getString();
      Serial.println("Resposta da API: " + response);
      digitalWrite(ledStatus, LOW);
      delay(100);
      digitalWrite(ledStatus, HIGH);
    } else {
      Serial.println("Erro no envio! Código: " + String(httpCode));
    }
    http.end();
  }
}