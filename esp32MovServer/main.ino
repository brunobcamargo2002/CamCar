// Define a biblioteca para funções matemáticas como pow()
#include <cmath>

// Define os pinos GPIO do ESP32 que serão usados para PWM
// ATENÇÃO: Se o GPIO 12 ainda for problemático, troque-o por outro pino de teste (ex: 23, 25, 26, 27)
const int PWM_PIN_A = 22;
const int PWM_PIN_B = 23; // Mudei para GPIO 23 para evitar o GPIO 12 por precaução.

// Pinos de controle de direção (não serão usados neste teste de PWM isolado)
const int IN1 = 2;
const int IN2 = 4;
const int IN3 = 5;
const int IN4 = 18;

// Define os canais PWM (o ESP32 tem 16 canais de 0 a 15)
const int PWM_CHANNEL_A = 0; // Canal PWM 0
const int PWM_CHANNEL_B = 1; // Canal PWM 1

// Define a frequência do PWM
// MUITO IMPORTANTE: Mantenha a frequência baixa para medição com multímetro
const int PWM_FREQ = 100; // Hz (Cem Hertz - Ideal para multímetro)

// Define a resolução do PWM em bits (ex: 8 bits = 0 a 255 valores)
const int PWM_RESOLUTION_BITS = 8; // 8 bits

// Calcula o valor máximo do duty cycle com base na resolução
const int MAX_DUTY_CYCLE = (int)(pow(2, PWM_RESOLUTION_BITS) - 1); // 255

// Variável para armazenar o duty cycle atual
int currentDutyCycle = 0;

// Variável para controlar a direção da variação do duty cycle
int dutyCycleDirection = 1; // 1 para aumentar, -1 para diminuir

void setup() {
  // Inicia a comunicação serial para depuração
  Serial.begin(115200);
  Serial.println("\n--- TESTE DE GERACAO DE PWM NO ESP32 - FREQUENCIA BAIXA ---");
  Serial.print("Frequencia do PWM: "); Serial.print(PWM_FREQ); Serial.println(" Hz (IDEAL PARA MULTIMETRO)");
  Serial.print("Resolucao do PWM: "); Serial.print(PWM_RESOLUTION_BITS); Serial.println(" bits");
  Serial.print("Valor maximo do Duty Cycle: "); Serial.println(MAX_DUTY_CYCLE);

  // Configura o canal PWM A
  if(ledcAttachChannel(PWM_PIN_A, PWM_FREQ, PWM_RESOLUTION_BITS, PWM_CHANNEL_A)){
    Serial.print("SUCESSO: Pino PWM_PIN_A (GPIO "); Serial.print(PWM_PIN_A);
    Serial.print(") anexado ao Canal "); Serial.print(PWM_CHANNEL_A);
    Serial.println(" com Freq e Resolucao.");
  } else {
    Serial.print("FALHA: Nao foi possivel anexar o Pino PWM_PIN_A (GPIO "); Serial.print(PWM_PIN_A);
    Serial.print(") ao Canal "); Serial.println(PWM_CHANNEL_A);
  }

  // Configura o canal PWM B
  if(ledcAttachChannel(PWM_PIN_B, PWM_FREQ, PWM_RESOLUTION_BITS, PWM_CHANNEL_B)){
    Serial.print("SUCESSO: Pino PWM_PIN_B (GPIO "); Serial.print(PWM_PIN_B);
    Serial.print(") anexado ao Canal "); Serial.print(PWM_CHANNEL_B);
    Serial.println(" com Freq e Resolucao.");
  } else {
    Serial.print("FALHA: Nao foi possivel anexar o Pino PWM_PIN_B (GPIO "); Serial.print(PWM_PIN_B);
    Serial.print(") ao Canal "); Serial.println(PWM_CHANNEL_B);
  }

  Serial.println("--- Setup Completo. Iniciando Loop de Teste ---");
  Serial.println("Verifique os pinos GPIO 22 e 23 (ou os que voce usou) com um multimetro em DC Voltagem.");
  Serial.println("A leitura deve variar de 0V a ~3.3V a cada segundo.");

  // Não configuramos os pinos de motor nem os acionamos neste teste isolado
  // para focar APENAS na saída PWM.
   pinMode(IN1, OUTPUT);
   pinMode(IN2, OUTPUT);
   pinMode(IN3, OUTPUT);
   pinMode(IN4, OUTPUT);
   digitalWrite(IN1, HIGH);
   digitalWrite(IN2, LOW);
   digitalWrite(IN3, HIGH);
   digitalWrite(IN4, LOW);
}

void loop() {
  // Ajusta o duty cycle
  currentDutyCycle += dutyCycleDirection * (MAX_DUTY_CYCLE / 10); // Aumenta/diminui em 10 passos

  // Inverte a direção quando atinge os limites
  if (currentDutyCycle >= MAX_DUTY_CYCLE) {
    currentDutyCycle = MAX_DUTY_CYCLE;
    dutyCycleDirection = -1;
  } else if (currentDutyCycle <= 0) {
    currentDutyCycle = 0;
    dutyCycleDirection = 1;
  }

  // Aplica o duty cycle aos canais PWM
  ledcWrite(PWM_CHANNEL_A, currentDutyCycle);
  ledcWrite(PWM_CHANNEL_B, currentDutyCycle);

  // Calcula a tensão média esperada (aproximada para ESP32 3.3V)
  float expectedVoltage = (float)currentDutyCycle / MAX_DUTY_CYCLE * 3.3;

  // Imprime o status no Serial Monitor
  Serial.print("Duty Cycle: "); Serial.print(currentDutyCycle);
  Serial.print(" ("); Serial.print((float)currentDutyCycle / MAX_DUTY_CYCLE * 100, 1); Serial.print("%)");
  Serial.print(" -> Tensao Media Esperada (aprox): "); Serial.print(expectedVoltage, 2); Serial.println("V");

  delay(1000); // Espera 1 segundo antes de mudar o duty cycle novamente
}