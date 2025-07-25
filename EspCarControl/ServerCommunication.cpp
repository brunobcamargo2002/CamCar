#include "ServerCommunication.h"

WebServer* ServerCommunication::server = new WebServer(80);
MoveController* ServerCommunication::moveController = nullptr;

ServerCommunication::ServerCommunication(){
  setup();
}

void ServerCommunication::setup(){
  Serial.begin(115200);
  WiFi.begin(ssid, password);
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }
  Serial.println("");
  Serial.println("Connected");
  Serial.println(WiFi.localIP());

  server->on("/line", HTTP_POST, handleLine);
  server->on("/stop", HTTP_POST, handleStop);
  server->on("/rotation", HTTP_POST, handleRotation);

  server->begin();
  Serial.println("Server initialized");
}

void ServerCommunication::handleLine(){
  if (server->method() == HTTP_POST) {
    String body = server->arg("plain");

    StaticJsonDocument<512> doc;
    DeserializationError error = deserializeJson(doc, body);

    if (error) {
      Serial.print("Parse Error");
      Serial.println(error.c_str());
      server->send(400, "application/json", "{\"erro\":\"Invalid JSON\"}");
      return;
    }

    if (doc.containsKey("forward")) {
      bool forward = doc["forward"];

      moveController->moveLine(forward);

    } else {
      Serial.println("field away");
    }

    server->send(200, "application/json", "{\"status\":\"ok\"}");
  }
  else {
    server->send(405, "text/plain", "Denied");
  }
}

void ServerCommunication::handleStop(){
  if (server->method() == HTTP_POST) {
    moveController->stop();

    server->send(200, "application/json", "{\"status\":\"ok\"}");
  }
  else {
    server->send(405, "text/plain", "Denied");
  } 
}

void ServerCommunication::handleRotation(){
  if (server->method() == HTTP_POST) {
    String body = server->arg("plain");

    StaticJsonDocument<512> doc;
    DeserializationError error = deserializeJson(doc, body);

    if (error) {
      Serial.print("Parse Error");
      Serial.println(error.c_str());
      server->send(400, "application/json", "{\"erro\":\"Invalid JSON\"}");
      return;
    }

    if (doc.containsKey("clockwise")) {
      bool clockwise = doc["clockwise"];
      moveController->rotate(clockwise);

    } else {
      Serial.println("field away");
    }
    server->send(200, "application/json", "{\"status\":\"ok\"}");
  }
  else {
    server->send(405, "text/plain", "Denied");
  }
}

void ServerCommunication::handleClient(){
  server->handleClient();
}
