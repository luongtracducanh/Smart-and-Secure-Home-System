const int tilt_sensor_pin=7;
int output_pin = 8;
bool enable = true;
void setup() {
    pinMode(tilt_sensor_pin, INPUT);
    pinMode(output_pin, OUTPUT);
    Serial.begin(9600);
}

void alert(){
  digitalWrite(output_pin, HIGH);
  delay(500);
  digitalWrite(output_pin, LOW);
  Serial.println("O");
}

void loop() {
    int sensorValue = digitalRead(tilt_sensor_pin);
    if (enable) {
      if(sensorValue==HIGH){
      // debug message
      alert();
      //Serial.println("O");
      }else{
      // debub message
      digitalWrite(output_pin, LOW);
      Serial.println("C");
      }
    }
    if (Serial.available() > 0) {
      char readByte = Serial.read();
      if (readByte == '1') {
        enable = true;
        Serial.println("Enable");
      }
      else if (readByte == '0' ) {
        enable = false;
        digitalWrite(output_pin, LOW);
        Serial.println("Disable");
      } 
    }
    delay(1000);
}