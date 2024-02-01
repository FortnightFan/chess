/**
 * --------------------------------------------------------------------------------------------------------------------
 * Example sketch/program showing how to read data from more than one PICC to serial.
 * --------------------------------------------------------------------------------------------------------------------
 * This is a MFRC522 library example; for further details and other examples see: https://github.com/miguelbalboa/rfid
 *
 * Example sketch/program showing how to read data from more than one PICC (that is: a RFID Tag or Card) using a
 * MFRC522 based RFID Reader on the Arduino SPI interface.
 *
 * Warning: This may not work! Multiple devices at one SPI are difficult and cause many trouble!! Engineering skill
 *          and knowledge are required!
 *
 * @license Released into the public domain.
 *
 * Typical pin layout used:
 * -----------------------------------------------------------------------------------------
 *             MFRC522      Arduino       Arduino   Arduino    Arduino          Arduino
 *             Reader/PCD   Uno/101       Mega      Nano v3    Leonardo/Micro   Pro Micro
 * Signal      Pin          Pin           Pin       Pin        Pin              Pin
 * -----------------------------------------------------------------------------------------
 * RST/Reset   RST          9             5         D9         RESET/ICSP-5     RST
 * SPI SS 1    SDA(SS)      ** custom, take a unused pin, only HIGH/LOW required **
 * SPI SS 2    SDA(SS)      ** custom, take a unused pin, only HIGH/LOW required **
 * SPI MOSI    MOSI         11 / ICSP-4   51        D11        ICSP-4           16
 * SPI MISO    MISO         12 / ICSP-1   50        D12        ICSP-1           14
 * SPI SCK     SCK          13 / ICSP-3   52        D13        ICSP-3           15
 *
 * More pin layouts for other boards can be found here: https://github.com/miguelbalboa/rfid#pin-layout
 *
 */

#include <SPI.h>
#include <MFRC522.h>

#define RST_PIN         2          // Configurable, see typical pin layout above
#define SS_1_PIN        10         // Configurable, take a unused pin, only HIGH/LOW required, must be different to SS 2
#define SS_2_PIN        9          // Configurable, take a unused pin, only HIGH/LOW required, must be different to SS 1

#define NR_OF_READERS   2

bool piece_on = false;
String serialized_data = "";

MFRC522 mfrc522_1;   // Create MFRC522 instance.
MFRC522 mfrc522_2;

/**
 * Initialize.
 */
void setup() {
  Serial.begin(9600); // Initialize serial communications with the PC
  SPI.begin();        // Init SPI bus

  mfrc522_1.PCD_Init(SS_1_PIN,RST_PIN);
  mfrc522_2.PCD_Init(SS_2_PIN,RST_PIN);
}

unsigned long getID(MFRC522 mfrc522){
  unsigned long hex_num;
  hex_num =  mfrc522.uid.uidByte[0] << 24;
  hex_num += mfrc522.uid.uidByte[1] << 16;
  hex_num += mfrc522.uid.uidByte[2] <<  8;
  hex_num += mfrc522.uid.uidByte[3];
  return hex_num;
}

void reader_1()
{
  if (mfrc522_1.PICC_IsNewCardPresent()) {
      if (mfrc522_1.PICC_ReadCardSerial()) {
        serialized_data += "1/" + String(getID(mfrc522_1)) + " ";
    }
  }
}

void reader_2()
{
  if (mfrc522_2.PICC_IsNewCardPresent()) {
      if (mfrc522_2.PICC_ReadCardSerial()) {
        serialized_data += "2/" + String(getID(mfrc522_2)) + " ";
    }
  }
}
void loop() 
{
  serialized_data = "_";
  reader_1();
  reader_2();

  Serial.println(serialized_data);
  delay(500);
}

/**
 * Helper routine to dump a byte array as hex values to Serial.
 */
