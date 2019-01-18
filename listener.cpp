#include "ros/ros.h"
#include <ros/time.h>
#include "std_msgs/String.h"
#include "std_msgs/Time.h"

void chatterCallback(const std_msgs::Time::ConstPtr& msg)
{
  ROS_INFO("Touched at: [%s]", msg->data.c_str());
}

int main(int argc, char **argv)
{
  ros::init(argc, argv, "listener");

  ros::NodeHandle n;

  ros::Subscriber sub = n.subscribe("my_topic", 1000, chatterCallback);
  
  ros::spin();

  return 0;
}