int ledPins[] = {8, 9, 10, 11, 12}; 
int buzzerPin = 6;

bool handPresent = false;
bool previousHandPresent = false;

void setup() {
  Serial.begin(9600);

  for (int i = 0; i < 5; i++) {
    pinMode(ledPins[i], OUTPUT);
  }

  pinMode(buzzerPin, OUTPUT);
}

void loop() {
  if (Serial.available() >= 5) {
    handPresent = true;

    int fingers[5];
    int fingerCount = 0;

    for (int i = 0; i < 5; i++) {
      fingers[i] = Serial.read();
      if (fingers[i] == 1) fingerCount++;
    }

    // -----------------------------
    //   ONE LED ACTIVE ONLY LOGIC
    // -----------------------------
    for (int i = 0; i < 5; i++) {
      digitalWrite(ledPins[i], LOW);  // Turn all OFF first
    }

    if (fingerCount > 0 && fingerCount <= 5) {
      int index = 5 - fingerCount;   // mapping: 5->0, 4->1, 3->2, 2->3, 1->4
      digitalWrite(ledPins[index], HIGH);
    }

    // -----------------------------
    //       BUZZER LOGIC
    // -----------------------------
    if (handPresent && !previousHandPresent) {
      tone(buzzerPin, 1200, 80);
      delay(100);
      tone(buzzerPin, 1200, 80);
    }

    if (fingerCount == 0) {
      tone(buzzerPin, 500, 300);  
    }

    previousHandPresent = handPresent;
  }

  else {
    handPresent = false;
    previousHandPresent = false;

    for (int i = 0; i < 5; i++) {
      digitalWrite(ledPins[i], LOW);
    }
  }
}

