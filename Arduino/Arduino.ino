//TO IMPLEMENT:
//-mm to adc range converter
//-setpoint 0 = adc 512

// RC Netwerk PID Regelaar - Arduino MEGA 2560
// Seriële communicatie: 9600 baud
// Ontvangen: setpoint, Kp, Kd, Ki, regelaar_ingeschakeld, MANUAL
#include <Servo.h>

Servo servo;

const int servoPin = 12;
const int servoUp = 50;
const int servoDown = 0;

const int dir1 = 4;
const int dir2 = 5;

const int analogPin = A0;
const int PWM_PIN = 3;

const float Vref = 5.0;

// PID parameters (defaults)
int setpoint = 512;
float Kp = 0.025;
float Kd = 0.00025;
float Ki = 0.00001;
bool regelaar_ingeschakeld = true;

// PID interne staat
float vorige_fout = 0.0;
float vorige_afgeleide = 0.0;
float integraal = 0.0;
float output = 0.0;  // globaal zodat seriële sectie er altijd bij kan

unsigned long vorigeTijd = 0;
unsigned long vorigeSerialTijd = 0;

String input = "";
float x = 0;
float y = 0;

void setup() {
  Serial.begin(115200);
  pinMode(PWM_PIN, OUTPUT);
  pinMode(dir1, OUTPUT);
  pinMode(dir2, OUTPUT);
  analogWrite(PWM_PIN, 0);
  servo.attach(servoPin);
  servo.write(servoUp);
}

void changeDirRight(){
  digitalWrite(dir1, HIGH);
  digitalWrite(dir2, LOW);
}
void changeDirLeft(){
  digitalWrite(dir1, LOW);
  digitalWrite(dir2, HIGH);  
}

float mmToAdc(float input){
  float sliderLength = 60.0;
  float temp = 1024 / sliderLength;
  float adc = ((temp * input) + 512.0);
  return constrain(adc, 0, 1023);
}

void loop() {
  unsigned long huidigeTijd = millis();

  // Lees seriële data
  while (Serial.available()) {

    char c = Serial.read();

    // End of message
    if (c == '\n') {

      // Determine coordinate type
      if (input.startsWith("x:")) {
        x = input.substring(2).toFloat();
        setpoint = mmToAdc(x);
        // Serial.print("X received: ");
        // Serial.println(x);
      }
      if (input.startsWith("s:")){
        if(input.substring(2).toFloat() == 1){
          servo.write(servoDown);
          //delay?
        }
        else{
          servo.write(servoUp);
          //delay?
        }
      // Clear buffer
      }
      input = "";
    }

    else {
      input += c;
    }
  }


  // PID regelaar
  if (regelaar_ingeschakeld) {
    float dt = (huidigeTijd - vorigeTijd) / 1000.0;
    if (dt > 0) {
      float fout  = setpoint - analogRead(analogPin);
      
      if(fout < 0){
        changeDirRight();
      }
      if(fout > 0){
        changeDirLeft();
      }



      // Integraal met anti-windup
      integraal += fout * dt;
      integraal = constrain(integraal, -5.0, 5.0);

      // Afgeleide
      float afgeleide = 0.8 * vorige_afgeleide + 0.2 * ((fout - vorige_fout) / dt);
      vorige_afgeleide = afgeleide;

      // PID output
      output = constrain(abs(Kp * fout + Ki * integraal + Kd * afgeleide), 0, 5);

      // Zet om naar PWM (0-255)
      int pwmWaarde = (int)(output /5 * 255);
      analogWrite(PWM_PIN, pwmWaarde);
      if (millis() - vorigeSerialTijd > 95) {
          Serial.println(analogRead(analogPin));
          vorigeSerialTijd = millis();
      }
    }
  }
  vorigeTijd = huidigeTijd;
}
