#include <Keypad.h>

#include <Servo.h>

#include <LiquidCrystal_I2C.h>

// #include <LiquidCrystal_I2C_Hangul.h>

LiquidCrystal_I2C lcd(0x27, 16, 2);
// LiquidCrystal_I2C_Hangul lcd(0x3F, 16, 2);
Servo myservo;
int pos = 0;
const byte rows = 4;
const byte columns = 4;

// Define the key map
char keys[rows][columns] = {
  { '1', '2', '3', 'A' },
  { '4', '5', '6', 'B' },
  { '7', '8', '9', 'C' },
  { '*', '0', '#', 'D' }
};

// Arduino corresponding pins
byte rowPins[rows] = { 11, 10, 9, 8 };
byte columnPins[columns] = { 7, 6, 5, 4 };

// Initialize a Keypad object
Keypad keypad = Keypad(makeKeymap(keys), rowPins, columnPins, rows, columns);

char * password = "235689#";
int passwordLength = strlen(password);
int currentposition = 0;
const int redled = 13;
const int greenled = 12;
const int buzz = 3;

void setup() {
  Serial.begin(9600);
  pinMode(redled, OUTPUT); // red led for wrong password
  pinMode(greenled, OUTPUT); // green led for correct password
  pinMode(buzz, OUTPUT); // buzzer to indicate differenct states of the program
  myservo.attach(2); // servo at pin 2
  lcd.init(); // initialize LCD
  lcd.begin(16, 2);
  lcd.backlight();
  lcd.clear();
  mainScreen();
}

void loop() {
  while (Serial.available() > 0) {
    Serial.read(); // discard any previous characters
  }

  int value = -1;
  while (value == -1) {
    if (Serial.available() > 0) {
      value = Serial.read();
    } else {
      if (currentposition == 0) {
        mainScreen();
      }
      int l;
      char code = keypad.getKey();
      if (code != NO_KEY) {
        lcd.clear();
        lcd.setCursor(0, 0);
        lcd.print("PASSWORD:       ");
        lcd.setCursor(0, 1);
        
        for (l = 0; l <= currentposition; ++l) {
          lcd.print("*");
          keyPress();
        }

        if (code == password[currentposition]) {
          ++currentposition;
          if (currentposition == passwordLength) {
            unlockDoor();
            currentposition = 0;
          }

        } else {
          alert();
          currentposition = 0;
        }
      }
    }
  }

  if (value == '1') unlockDoor();
  else if (value == '0') alert();
}

// function to unlock door
void unlockDoor() {
  Serial.println(1, 2);
  lcd.clear();
  digitalWrite(greenled, HIGH);
  lcd.print("CORRECT PASSWORD");
  lcd.setCursor(0, 1);
  lcd.println("WELCOME!        ");
  unlockSound();

  for (pos = 180; pos >= 0; pos -= 5) // goes from 180 degrees to 0 degrees
  {
    myservo.write(pos); // tell servo to go to position in variable 'pos'
    delay(15); // waits 15ms for the servo to reach the position
  }
  delay(5000);

  counterLock();

  for (int i = 0; i < 4; i++) {
    digitalWrite(buzz, HIGH);
    delay(40);
    digitalWrite(buzz, LOW);
    delay(40);
  }

  lcd.clear();
  lcd.print("LOCKING");
  delay(500);

  for (int i = 7; i < 10; i++) {
    lcd.setCursor(i, 0);
    lcd.print(".");
    delay(500);
  }

  digitalWrite(greenled, LOW);
  delay(1000);

  for (pos = 0; pos <= 180; pos += 5) // goes from 0 degrees to 180 degrees
  { // in steps of 1 degree
    myservo.write(pos); // tell servo to go to position in variable 'pos'
    delay(15);
    currentposition = 0;  
  }

  lcd.clear();
  lcd.print("LOCKED!");
  delay(1000);
  lcd.clear();
  mainScreen();
}

// initiate alert when password is incorrect
void alert() {
  Serial.println(0, 2);
  lcd.clear();
  lcd.print("WRONG PASSWORD! ");
  digitalWrite(redled, HIGH);
  digitalWrite(buzz, HIGH);
  delay(3000);
  lcd.clear();
  digitalWrite(redled, LOW);
  digitalWrite(buzz, LOW);
  mainScreen();
}

// create key press sound using buzzer
void keyPress() {
  digitalWrite(buzz, HIGH);
  delay(50);
  digitalWrite(buzz, LOW);
}

// display the main screen
void mainScreen() {
  lcd.setCursor(0, 0);
  lcd.println("ENTER PASSWORD  ");
  lcd.setCursor(0, 1);
  lcd.println("OR USE FACEID   ");
}

// unlock buzz sound
void unlockSound() {
  for (int i = 0; i < 4; i++) {
    digitalWrite(buzz, HIGH);
    delay(80);
    digitalWrite(buzz, LOW);
    delay(80);
  }
}

// counter to close door
void counterLock() {
  lcd.clear();
  delay(1000);

  lcd.println("GET IN WITHIN:   ");
  delay(1000);
  for (int i = 3; i >= 0; i--) {
    lcd.println("GET IN WITHIN: ");
    lcd.setCursor(15, 0);
    lcd.print(i);
    delay(500);
    lcd.clear();
    lcd.println("GET IN WITHIN:  ");
    digitalWrite(buzz, HIGH);
    delay(1000);
    digitalWrite(buzz, LOW);
  }

  delay(1000);
}