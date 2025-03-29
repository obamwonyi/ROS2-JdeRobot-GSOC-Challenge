#include "rclcpp/rclcpp.hpp"
#include "std_msgs/msg/string.hpp"

using namespace std::chrono_literals;

// Publisher Node
class PublisherNode : public rclcpp::Node
{
public:
  PublisherNode()
  : Node("publisher_node")
  {
    publisher_ = this->create_publisher<std_msgs::msg::String>("greeting_topic", 10);
    timer_ = this->create_wall_timer(
      500ms, std::bind(&PublisherNode::publish_message, this));
  }

private:
  void publish_message()
  {
    auto message = std_msgs::msg::String();
    message.data = "Hello! ROS2 is fun";
    publisher_->publish(message);
    RCLCPP_INFO(this->get_logger(), "Publishing: '%s'", message.data.c_str());
  }

  rclcpp::Publisher<std_msgs::msg::String>::SharedPtr publisher_;
  rclcpp::TimerBase::SharedPtr timer_;
};

// Subscriber Node
class SubscriberNode : public rclcpp::Node
{
public:
  SubscriberNode()
  : Node("subscriber_node")
  {
    subscriber_ = this->create_subscription<std_msgs::msg::String>(
      "greeting_topic", 10, std::bind(&SubscriberNode::callback, this, std::placeholders::_1));
  }

private:
  void callback(const std_msgs::msg::String::SharedPtr msg)
  {
    RCLCPP_INFO(this->get_logger(), "Received: '%s'", msg->data.c_str());
  }

  rclcpp::Subscription<std_msgs::msg::String>::SharedPtr subscriber_;
};

int main(int argc, char * argv[])
{
  rclcpp::init(argc, argv);

  // Creates and run the publisher node
  auto publisher_node = std::make_shared<PublisherNode>();

  // Creates and run the subscriber node
  auto subscriber_node = std::make_shared<SubscriberNode>();

  // Spin both nodes ( this is in one terminal ) so onlike turtlesim or talker/listner you don't have to use two terminals
  rclcpp::executors::SingleThreadedExecutor executor;
  executor.add_node(publisher_node);
  executor.add_node(subscriber_node);
  executor.spin();

  rclcpp::shutdown();
  return 0;
}