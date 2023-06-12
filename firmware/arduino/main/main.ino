#include <Arduino.h>
#include <Adafruit_TinyUSB.h> // for Serial

// Pin values for led/pd
#define red_led 9
#define ir_led 12
#define violet_led 10
#define red_adc A4
#define ir_adc A0
#define violet_adc A2
// Set flags for red, ir, violet
#define red 0
#define ir 1
#define violet 2
// constants for adjusting ADC input
float MV_PER_LSB (0.73242188F); // 3.0V ADC range and 12-bit ADC resolution = 3000mV/4096
#define VBAT_DIVIDER (0.5F)
#define VBAT_DIVIDER_COMP (2.0F)
#define REAL_VBAT_MV_PER_LSB (VBAT_DIVIDER_COMP * MV_PER_LSB)
float raw;
// constants for burst & moving average filter
#define sampleSize 5    // number of samples for burst filter
#define sampleRate 100 //in Hz
#define window_size 10  // Number of samples for moving average filter
int red_idx = 0;       
int ir_idx = 0;
int violet_idx = 0;     // index of moving average filter to replace
int burst_sum = 0;
int burst_avg = 0;
// variables for managing adc processing
int red_sum = 0;
int ir_sum = 0;
int violet_sum = 0;
int red_avg;
int ir_avg;
int violet_avg;
int red_adc_arr[window_size];
int ir_adc_arr[window_size];
int violet_adc_arr[window_size];
// keys for associating flag with adc channel and led channel
int adc_key[3] = {red_adc, ir_adc, violet_adc};
int led_key[3] = {red_led, ir_led, violet_led};
int channel_flag = 0;
int avg;
int channel_data[3];


float readADC(int channel_flag){
    raw = analogRead(adc_key[channel_flag]);
    return raw*REAL_VBAT_MV_PER_LSB;
}

void setup() {
  // Set up LEDs
  pinMode(red_led, OUTPUT);
  pinMode(ir_led, OUTPUT);
  pinMode(violet_led, OUTPUT);
  // define baudrate
  Serial.begin(115200);
  while ( !Serial ) delay(10);
  // Setup ADC channels
  analogReference(AR_INTERNAL_3_0);
  analogReadResolution(12);
  delay(1);
  // Read all three adc channels
  readADC(red_adc);
  readADC(ir_adc);
  readADC(violet_adc);
}

float burst_sample(int channel_flag) {
  for (int i=0; i<sampleSize; i++){
      burst_sum += readADC(channel_flag);
      delay(1000/(6*sampleRate*sampleSize));
    }
  burst_avg = burst_sum/sampleSize;
  burst_sum = 0;
  return burst_avg;
}

float moving_average_filter(int channel_flag, int burst_val) {
  if (channel_flag == red) {
    red_sum = red_sum - red_adc_arr[red_idx];
    red_adc_arr[red_idx] = burst_val;
    red_sum += burst_val;
    red_avg = red_sum/window_size;
    red_idx = (red_idx+1) % window_size;
    return red_avg;
  }
  else if (channel_flag == ir) {
    ir_sum = ir_sum - ir_adc_arr[ir_idx];
    ir_adc_arr[ir_idx] = burst_val;
    ir_sum += burst_val;
    ir_avg = ir_sum/window_size;
    ir_idx = (ir_idx+1) % window_size;
    return ir_avg;
  }
  else {
    violet_sum = violet_sum - violet_adc_arr[violet_idx];
    violet_adc_arr[violet_idx] = burst_val;
    violet_sum += burst_val;
    violet_avg = violet_sum/window_size;
    violet_idx = (violet_idx+1) % window_size;
    return violet_avg;
  }
}

float channel_acquisition(int channel_flag) {
  digitalWrite(led_key[channel_flag], HIGH);
  avg = moving_average_filter(channel_flag, burst_sample(channel_flag));
  digitalWrite(led_key[channel_flag], LOW);
  return avg;
}

void loop() {

    channel_flag = red;
    channel_data[red] = channel_acquisition(channel_flag);
    delay(1000/(6*sampleRate));
    channel_flag = ir;
    channel_data[ir] = channel_acquisition(channel_flag);
    delay(1000/(6*sampleRate));
    channel_flag = violet;
    channel_data[violet] = channel_acquisition(channel_flag);
    delay(1000/(6*sampleRate));
  
    Serial.println(channel_data[red]);
    Serial.println(channel_data[ir]);
    Serial.println(channel_data[violet]);
    Serial.println('/');
    Serial.flush();


}


