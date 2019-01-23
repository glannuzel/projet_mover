#include "ros/ros.h"
#include <ros/time.h>
#include "std_msgs/String.h"
#include "std_msgs/Time.h"

void chatterCallback(const std_msgs::Time::ConstPtr& msg)
{
  ROS_INFO("Wire has been touched!");
}

void chatterCallbackBeginning(const std_msgs::Time::ConstPtr& msg)
{
  ROS_INFO("BEGINNING OF THE GAME");
}

void chatterCallbackEnd(const std_msgs::Time::ConstPtr& msg)
{
  ROS_INFO("END OF THE GAME");
}

int main(int argc, char **argv)
{
  ros::init(argc, argv, "listener_mover");

  ros::NodeHandle n;

  ros::Subscriber sub = n.subscribe("touched", 280, chatterCallback);
  ros::Subscriber sub_beginning = n.subscribe("beginning", 280, chatterCallbackBeginning);
  ros::Subscriber sub_end = n.subscribe("end", 280, chatterCallbackEnd);
  
  ros::spin();

  return 0;
}