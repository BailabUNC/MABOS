#include <Arduino.h>
#include <Adafruit_TinyUSB.h> // for Serial

// Pin values for led/pd
#define red_led 7
#define red_adc A0
// constants for adjusting ADC input
float MV_PER_LSB (0.73242188F); // 3.0V ADC range and 12-bit ADC resolution = 3000mV/4096
#define VBAT_DIVIDER (0.5F)
#define VBAT_DIVIDER_COMP (2.0F)
#define REAL_VBAT_MV_PER_LSB (VBAT_DIVIDER_COMP * MV_PER_LSB)
float raw;
// constants for burst & moving average filter
#define sampleSize 5    // number of samples for burst fiilter
#define sampleRate 100 //in Hz
#define window_size 10  // Number of samples for moving average filter
int idx = 0;            // index of moving average filter to replace
int burst_sum = 0;
int burst_avg = 0;
int red_sum = 0;
int red_avg;
int red_adc_arr[window_size];

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

    digitalWrite(red_led, HIGH);

    for (int i=0; i<sampleSize; i++){
      burst_sum += readADC();
      delay(1000/(2*sampleRate*sampleSize));
    }
    burst_avg = (burst_sum/sampleSize);
    burst_sum = 0;
    red_sum = red_sum - red_adc_arr[idx];
    red_adc_arr[idx] = burst_avg;
    red_sum += burst_avg;
    idx = (idx + 1) % window_size;

    red_avg = red_sum/window_size;
    Serial.println(red_avg);
    Serial.flush();
    digitalWrite(red_led, LOW);
    delay(1000/(2*sampleRate));
}


