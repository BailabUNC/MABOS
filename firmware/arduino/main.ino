#include <Arduino.h>
#include <Adafruit_TinyUSB.h> // for Serial

#define red_led 7
#define red_adc A0
int adcvalue = 0;
float MV_PER_LSB (0.73242188F); // 3.0V ADC range and 12-bit ADC resolution = 3000mV/4096
#define VBAT_DIVIDER (0.5F)
#define VBAT_DIVIDER_COMP (2.0F)
#define REAL_VBAT_MV_PER_LSB (VBAT_DIVIDER_COMP * MV_PER_LSB)
float raw;

#define sampleSize 5
#define sampleRate 10

float readADC(void) {
  raw = analogRead(red_adc);
  return raw*REAL_VBAT_MV_PER_LSB;
}

void setup() {
  pinMode(red_led, OUTPUT);
  Serial.begin(115200);
  while ( !Serial ) delay(10);
  analogReference(AR_INTERNAL_3_0);
  analogReadResolution(12);
  delay(1);
  readADC();
}
void loop() {
  float red_adc_arr[sampleSize];
  float average;
  float median=0;
  float sum;
    digitalWrite(red_led, HIGH);

    for (int i=0; i<sampleSize; i++){
      red_adc_arr[i] = readADC();
      delay(sampleRate/10);
    }

    for (int i; i<sampleSize; i++){
      sum = sum + red_adc_arr[i];
    }
    average = (sum/sampleSize);
    Serial.println(average);
    Serial.flush();
    digitalWrite(red_led, LOW);
    delay(5);
}


