// include ROS, messages, time
#include <ros.h>
#include <ros/time.h>
#include <std_msgs/Time.h>

ros::NodeHandle  nh;

std_msgs::Time current_time;
ros::Publisher p("touched", &current_time);
ros::Publisher b("beginning", &current_time);
ros::Publisher e("end", &current_time);

// change pin that buzzer is connected to here
#define BUZZER_PIN  5

// define led colors pin
#include <FastLED.h>
#define STRIP_PIN     3
#define NUM_LEDS    60

// define led alone pin
#define LED_PIN 7

//Circuit detection
#define LOOP_PIN 9

// button stop
#define BUTTON_PIN 12

// define beginning of the game
bool hasbegun;

CRGB leds[NUM_LEDS];
CRGB myled[1];

/* 
 *  Set-up circuit and ROS
 */

void setup() {

  // setup ROS
  pinMode(13, OUTPUT);
  nh.initNode();
  nh.advertise(p);
  nh.advertise(b);
  nh.advertise(e);
  
  // setup buzzer as output
  pinMode(BUZZER_PIN, OUTPUT);

  //setup button as input
  pinMode(BUTTON_PIN, INPUT);

  // setup circuit as input
  pinMode(LOOP_PIN, INPUT_PULLUP);
  // connect internally 50k-ohm resistor between the pin and +5V

  // leds intialization
  FastLED.addLeds<WS2812, STRIP_PIN, GRB>(leds, NUM_LEDS);

  // led alone initialization
  FastLED.addLeds<WS2812, LED_PIN, GRB>(myled, 1);

  // set beginning to false
  hasbegun = false;

}

/*
 * While(1)
 */

void loop() {
  
  // read if loop is closed or not
  int sensorVal = digitalRead(LOOP_PIN);
  int buttonState = digitalRead(BUTTON_PIN);

  // beginning of the game
  if(!hasbegun){
    if(sensorVal == LOW)
    {
      myled[0] = CRGB(255, 255, 255);
      for (int i = 0; i<NUM_LEDS; i++){
        leds[i] = CRGB(0, 0, 0);
      }
      FastLED.show();
      nh.spinOnce();
    }
    else {
      hasbegun = true;
      digitalWrite(BUZZER_PIN, HIGH);
      delay(70);
      digitalWrite(BUZZER_PIN, LOW);
      delay(70);
      digitalWrite(BUZZER_PIN, HIGH);
      delay(70);
      digitalWrite(BUZZER_PIN, LOW);
      current_time.data = nh.now();
      b.publish( &current_time );
      nh.spinOnce();
    }
  }


  // GAME
  else {
    if (buttonState == HIGH) {
      
      hasbegun = false;
      current_time.data = nh.now();
      e.publish( &current_time );
      nh.spinOnce();
      
    }

    else {

      // if loop is closed
      if (sensorVal == HIGH) {
          myled[0] = CRGB(255, 0, 0);
          leds[0] = CRGB(0, 0, 0);
          FastLED.show();
          digitalWrite(BUZZER_PIN, HIGH);
          delay(100);
          digitalWrite(BUZZER_PIN, LOW);
          current_time.data = nh.now();
          p.publish( &current_time );
          nh.spinOnce();
      }
      
      // if loop is open
      else {
          nh.spinOnce();
          leds[0] = CRGB(0, 0, 0);
          myled[0] = CRGB(0, 255, 0);
          FastLED.show();
          delay(10);
      }

    }
    
    
  }
}
