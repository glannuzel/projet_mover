// include ROS, messages, time
#include <ros.h>
#include <ros/time.h>
#include <std_msgs/Time.h>


ros::NodeHandle  nh;

std_msgs::Time test;
ros::Publisher p("my_topic", &test);

// change pin that buzzer is connected to here
#define BUZZER_PIN  5

// define led colors pin
#include <FastLED.h>
#define LED_PIN     3
#define NUM_LEDS    60

//Circuit detection
#define LOOP_PIN 9

CRGB leds[NUM_LEDS];

/* 
 *  Set-up circuit and ROS
 */

void setup() {

  // setup ROS
  pinMode(13, OUTPUT);
  nh.initNode();
  nh.advertise(p);
  
  // setup buzzer as output
  pinMode(BUZZER_PIN, OUTPUT);

  // setup circuit as input
  pinMode(LOOP_PIN, INPUT_PULLUP);
  // connect internally 50k-ohm resistor between the pin and +5V

  // leds intialization
  FastLED.addLeds<WS2812, LED_PIN, GRB>(leds, NUM_LEDS);

}

/*
 * While(1)
 */

void loop() {
  
  // read if loop is closed or not
  int sensorVal = digitalRead(LOOP_PIN);

  // if loop is closed
  if (sensorVal == HIGH) {
    leds[0] = CRGB(255, 0, 0);
    FastLED.show();
    digitalWrite(BUZZER_PIN, HIGH);
    delay(100);
    digitalWrite(BUZZER_PIN, LOW);
    test.data = nh.now();
    p.publish( &test );
    nh.spinOnce();
  }
  
  // if loop is open
  else {
    nh.spinOnce();
    leds[0] = CRGB(0, 255, 0);
    FastLED.show();
    delay(10);
  }
}
