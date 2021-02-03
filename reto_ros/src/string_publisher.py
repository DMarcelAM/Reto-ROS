#!/usr/bin/env python

import rospy
from std_msgs.msg import String

topic_content = rospy.get_param('topic_content')
msg_type = String
topic_name = 'topic_string'
node_name = 'string_publisher'
topic_frequency = 5


class Publisher:
    def __init__(self, msg_type, topic_name, node_name, topic_frequency, topic_content):
        self.node_name = node_name
        self.topic_frequency = topic_frequency
        self.topic_content = topic_content
        self.simple_publisher = rospy.Publisher(topic_name, msg_type, queue_size = 10)
        self.node_initialization()

    def node_initialization(self):
        rospy.init_node(self.node_name, anonymous = False)
        rate = rospy.Rate(self.topic_frequency)

        while not rospy.is_shutdown():
            self.simple_publisher.publish(self.topic_content)
            rate.sleep()

if __name__ == '__main__':
    try:
        Publisher(msg_type, topic_name, node_name, topic_frequency, topic_content)
    except rospy.ROSInterruptException:
        pass
