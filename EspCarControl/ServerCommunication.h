#ifndef SERVER_COMMUNICATION_H
#define SERVER_COMMUNICATION_H

#include "MoveController.h"

#include <WiFi.h>
#include <WebServer.h>
#include <ArduinoJson.h>

class ServerCommunication{
  private:
    const char* ssid = "Camargo";
    const char* password = "Soy5001150011@";

    static WebServer* server;
    
  public:
    ServerCommunication();
    static MoveController* moveController;
    
  private:
    void setup();
    static void handleLine();
    static void handleStop();
    static void handleRotation();
    static void handleCalibration();
    
  public:
    void handleClient();
    ~ServerCommunication();
};

#endif