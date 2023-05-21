#include <dht11.h>

#include <Wire.h>

#include <LiquidCrystal.h>

// #include<LiquidCrystal_I2C_Hangul.h>

#define DHT11PIN 6
const int buzzerPin = 8; // Arduino pin connect to buzzer
float alertGasValue = 850; // threshold to alarm for gas detection
float alertTempValue = 30;
float alertHumidValue = 80;

bool enableTempAlert = true;
bool enableHumidAlert = true;
bool enableGasAlert = true;

const int gasSensorPin = A1;
dht11 DHT11;
// LiquidCrystal_I2C_Hangul lcd(0x3F, 16, 2);
const int rs = 12,
  en = 11,
  d4 = 5,
  d5 = 4,
  d6 = 3,
  d7 = 2;
LiquidCrystal lcd(rs, en, d4, d5, d6, d7);

int alertTempPin = 7;
int alertHumidPin = 13;

void showAlert(bool hot, bool humid) {
  if (hot) digitalWrite(alertTempPin, HIGH);
  else digitalWrite(alertTempPin, LOW);

  if (humid) digitalWrite(alertHumidPin, HIGH);
  else digitalWrite(alertHumidPin, LOW);
}

void setup() {
  Serial.begin(9600);
  lcd.begin(16, 2);
  // lcd.init();
  // lcd.backlight();

  // led to alert high temperature and high humidity
  pinMode(alertTempPin, OUTPUT);
  pinMode(alertHumidPin, OUTPUT);
  pinMode(buzzerPin, OUTPUT);
}

void loop() {
  int check = DHT11.read(DHT11PIN);
  // float readTemp = analogRead(tempSensor);
  // float volt = readTemp * 5 / 1023;
  float temperature = DHT11.temperature;
  // float temperature = DHT11.temperature;
  float humidity = DHT11.humidity;

  float gas = analogRead(gasSensorPin); // Read the sensor value
  if (enableGasAlert && gas > alertGasValue) {
    digitalWrite(buzzerPin, HIGH);

    // gas debug message
    // Serial.println("Gas: DANGEROUS!");
  } else {
    digitalWrite(buzzerPin, LOW);

    // gas debug message
    // Serial.println("Gas: Safe");
  }

  Serial.print(temperature, 2);
  Serial.print(",");
  Serial.print(humidity, 2);
  Serial.print(",");
  Serial.println(gas, 2);

  // lcd to display current temperature
  String a = "Temp (C): " + String(temperature) + String(" ");
  String b = "Humid (%): " + String(humidity);
  String c = "HIGH TEMPERATURE";
  String d = "HIGH HUMIDITY   ";

  // alert node on Arduino
  bool highTemp = false;
  bool highHumid = false;

  if (enableTempAlert && temperature >= alertTempValue) {
    highTemp = true;
  }
  if (enableHumidAlert && humidity >= alertHumidValue) {
    highHumid = true;
  }

  //if (data == "0") showAlert(false, false);
  //else
  showAlert(highTemp, highHumid);

  if (highTemp) {
    lcd.setCursor(0, 0);
    lcd.print(c);
  } else if (!highTemp) {
    lcd.setCursor(0, 0);
    lcd.print(a);
  }

  if (highHumid) {
    lcd.setCursor(0, 1);
    lcd.print(d);
  } else if (!highHumid) {
    lcd.setCursor(0, 1);
    lcd.print(b);
  }

  // if (Serial.available()) { // check if there's incoming data

  // }
  String data = Serial.readStringUntil('\n'); // read the incoming data until a newline character is received
  data = data.substring(0, data.length() - 1);
  int comma1 = data.indexOf(','); // find the position of the first comma
  int comma2 = data.indexOf(',', comma1 + 1); // find the position of the second comma
  // Serial.println("comma1: " + String(comma1) + " comma2: " + String(comma2));
  String value1 = data.substring(0, comma1); // extract the first value
  String value2 = data.substring(comma1 + 1, comma2); // extract the second value
  String value3 = data.substring(comma2 + 1); // extract the third value
  //Serial.println(value1 + "," + value2 + "," + value3);
  if (!value1.equals(" ") && !value1.equals("")) { // check if value1 is not empty
    alertTempValue = value1.toFloat(); // convert the first value to an integer
    if (alertTempValue == 0) enableTempAlert = false;
    else enableTempAlert = true;
  }

  if (!value2.equals(" ") && !value2.equals("")) { // check if value2 is not empty
    alertHumidValue = value2.toFloat(); // convert the second value to an integer
    if (alertHumidValue == 0) enableHumidAlert = false;
    else enableHumidAlert = true;
  }

  if (!value3.equals(" ") && !value3.equals("")) { // check if value3 is not empty
    alertGasValue = value3.toFloat(); // convert the third value to an integer
    if (alertGasValue == 0) enableGasAlert = false;
    else enableGasAlert = true;
  }

  //Serial.println("alerTempValue: " + String(alertTempValue) + ", alertHumidValue: " + String(alertHumidValue) + ",alertGasValue: " + String(alertGasValue) + ".");
  delay(2000);
}