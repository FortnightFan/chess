#include <SPI.h>
#include <MFRC522.h>

#define SS_PIN_1 10 
#define SS_PIN_2 9  

#define RST_PIN 2 

MFRC522 mfrc522_1(SS_PIN_1, RST_PIN);

bool cardPresent_1 = false;

unsigned long getID(MFRC522& mfrc522) {
  unsigned long hex_num = 0;
  byte uidSize = mfrc522.uid.size;

  for (byte i = 0; i < uidSize; i++) {
    hex_num <<= 8; 
    hex_num |= mfrc522.uid.uidByte[i]; 
  }

  mfrc522.PICC_HaltA(); // Stop reading
  return hex_num;
}

void setup() {
  Serial.begin(9600);
  SPI.begin();

  mfrc522_1.PCD_Init();
}

void loop() {
  checkCardPresence(mfrc522_1, cardPresent_1, "Reader 1");
//  checkCardPresence(mfrc522_2, cardPresent_2, "Reader 2");
}

void checkCardPresence(MFRC522& mfrc522, bool& cardPresent, const char* readerName) {
  // Look for new cards
  if (mfrc522.PICC_IsNewCardPresent()) {
    if (!cardPresent) {
      Serial.println(readerName);
      Serial.println("Card placed!");
      cardPresent = true;
//      mfrc522.PICC_ReadCardSerial();
      Serial.print(getID(mfrc522));
      Serial.println();
    }
  } else {
    if (cardPresent) {
      Serial.println("Card lifted!");
      cardPresent = false;
    }
  }

  mfrc522.PICC_HaltA();
  mfrc522.PCD_StopCrypto1();
}