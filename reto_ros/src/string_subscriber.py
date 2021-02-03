#!/usr/bin/env python

import rospy
from std_msgs.msg import String

msg_type = String
topic_name = 'topic_string'
node_name = 'string_subscriber'

class Subscriber():
    def __init__(self, msg_type, topic_name, node_name):
        self.msg_type = msg_type
        self.topic_name = topic_name
        self.node_name = node_name
        self.node_initialization()
        rospy.Subscriber(self.topic_name, self.msg_type, self.stringListenerCallback)
        rospy.spin()

    def node_initialization(self):
        rospy.init_node(self.node_name, anonymous=False)

    def stringListenerCallback(self, data):
        rospy.loginfo(data.data)


if __name__ == '__main__':
    Subscriber(msg_type, topic_name, node_name)
