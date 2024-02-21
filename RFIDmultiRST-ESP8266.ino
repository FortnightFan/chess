/**
   WIRING:
   -----------------------------------------------------------------------------------------
               MFRC522      Arduino       Arduino   Arduino    Arduino          Arduino
               Reader/PCD   Uno/101       Mega      Nano v3    Leonardo/Micro   Pro Micro
   Signal      Pin          Pin           Pin       Pin        Pin              Pin
   -----------------------------------------------------------------------------------------
   RST/Reset   RST          Take an unused digital pin for each sensor
   SPI SS      SDA(SS)      Take an uned digital pin, same for all sensors
   SPI MOSI    MOSI         11 / ICSP-4   51        D11        ICSP-4           16
   SPI MISO    MISO         12 / ICSP-1   50        D12        ICSP-1           14
   SPI SCK     SCK          13 / ICSP-3   52        D13        ICSP-3           15

*/

#include <SPI.h>
#include <MFRC522.h>
#define SS_PIN          15        // Any unused digital pin
#define NR_OF_READERS   7         // How many readers do you have?

MFRC522 mfrc522[NR_OF_READERS];   // Create MFRC522 instances.

String currentIDs[] = {"00000000", "00000000", "00000000", "00000000"}; // Change if more are needed.
byte RSTpins[] = {3, 2, 0, 4, 5, 16, 10};                                 // Unique digital pin for each sensor

void setup() {
  Serial.begin(9600); // Initialize serial communications with the PC
  SPI.begin();        // Init SPI bus
  
  for (int i = 0; i < NR_OF_READERS; i++) pinMode(RSTpins[i], OUTPUT);
}

void loop() {
  for (uint8_t reader = 0; reader < NR_OF_READERS; reader++) {
    currentIDs[reader] = "00000000";
    digitalWrite(RSTpins[reader], HIGH);                      // Turn on the sensor by setting the RST pin to HIGH
    delay(40);                                                // Delay could be shortened/removed, test please
    mfrc522[reader].PCD_Init(SS_PIN, RSTpins[reader]);        // Init each MFRC522 card
    delay(40);                                                // Delay could be shortened/removed, test please
    if (mfrc522[reader].PICC_IsNewCardPresent() && mfrc522[reader].PICC_ReadCardSerial()) {
      currentIDs[reader] = getCode(mfrc522[reader].uid.uidByte, mfrc522[reader].uid.size);
      mfrc522[reader].PICC_HaltA();                           // Stop reading
      mfrc522[reader].PCD_StopCrypto1();
    }
    digitalWrite(RSTpins[reader], LOW);                       // Turn the sensor off by setting the RST pin to LOW
  }

  printIDs();
}

void printIDs() { // Print the ID's
  for (int i = 0; i < NR_OF_READERS; i++) {
    Serial.print(currentIDs[i]);
    Serial.print(", ");
  }
  Serial.println();
}

String getCode(byte *buffer, byte bufferSize) {
  String code = "";
  for (byte i = 0; i < bufferSize; i++) code = code + String(buffer[i], HEX);
  return (code);
}
