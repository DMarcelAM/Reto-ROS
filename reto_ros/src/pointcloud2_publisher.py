#!/usr/bin/env python

import rospy
import os
import time

from sensor_msgs import point_cloud2
from sensor_msgs.msg import PointCloud2, PointField
from std_msgs.msg import Header

topic_frequency=rospy.get_param("topic_frequency")
filename=rospy.get_param("path")

if topic_frequency < 2:
    raise Exception("La frecuencia tiene que ser mayor o igual a 2Hz.")

rospy.loginfo("Parameter %s was found on the parameter server. Using %fs Hz for topic_frequency."%("topic_frequency", topic_frequency))

def pcd_to_pointcloud2(filename):

    if not os.path.isfile(filename):
            raise Exception("El archivo .pcd no existe.")
    n = 4

    with open(filename, "r") as pcdfile:
        line = pcdfile.readline()
        while line[0:6] != 'FIELDS':
            line = pcdfile.readline()
        try:
            f, x, y, z, c = line.split(" ", n)
        except:
            n = 3
    if n==3:
        with open(filename, "r") as pcdfile:
            line = pcdfile.readline()
            while line[0:6]!='FIELDS':
                line = pcdfile.readline()
            f, x, y, z= line.split(" ", 3)
            z=z[0]

            while line[0:4]!='SIZE':
                line = pcdfile.readline()
            f, s_x, s_y, s_z= line.split(" ", 3)
            s_x=int(s_x)
            s_y=int(s_y)
            s_z=int(s_z)

            while line[0:4]!='TYPE':
                line = pcdfile.readline()
            f, t_x, t_y, t_z= line.split(" ", 3)
            if t_x == 'F':
                t_x = PointField.FLOAT32
            if t_y == 'F':
                t_y = PointField.FLOAT32
            if t_z[0] == 'F':
                t_z = PointField.FLOAT32

            while line[0:5]!='COUNT':
                line = pcdfile.readline()
            f, c_x, c_y, c_z= line.split(" ", 3)
            c_x = int(c_x)
            c_y = int(c_y)
            c_z = int(c_z)

            fields = [PointField(x, 0, t_x, c_x),
                      PointField(y, 4, t_y, c_y),
                      PointField(z, 8, t_z, c_z),]

            while line[0:4]!='DATA':
                line = pcdfile.readline()

            data = pcdfile.read()

        separador1 = '\n'
        separador2 = ' '
        lista = data.split(separador1)
        points=[]
        for i in lista:
            m = i.split(separador2)
            m=m[0:4]
            if len(m)==3:
                m = list(map(float, m))
                points.append(m)

    elif n==4:

        with open(filename, "r") as pcdfile:
            line = pcdfile.readline()
            while line[0:6]!='FIELDS':
                line = pcdfile.readline()
            f, x, y, z, c= line.split(" ", 4)
            c=c[0:4]

            while line[0:4]!='SIZE':
                line = pcdfile.readline()
            f, s_x, s_y, s_z, s_c= line.split(" ", 4)
            s_x=int(s_x)
            s_y=int(s_y)
            s_z=int(s_z)
            s_c=int(s_c)

            while line[0:4]!='TYPE':
                line = pcdfile.readline()
            f, t_x, t_y, t_z, t_c= line.split(" ", 4)
            if t_x == 'F':
                t_x = PointField.FLOAT32
            if t_y == 'F':
                t_y = PointField.FLOAT32
            if t_z == 'F':
                t_z = PointField.FLOAT32
            if t_c[0] == 'U' or t_c[0] == 'F':
                t_c = PointField.UINT32

            while line[0:5]!='COUNT':
                line = pcdfile.readline()
            f, c_x, c_y, c_z,c_c= line.split(" ", 4)
            c_x = int(c_x)
            c_y = int(c_y)
            c_z = int(c_z)
            c_c = int(c_c)

            fields = [PointField(x, 0, t_x, c_x),
                      PointField(y, 4, t_y, c_y),
                      PointField(z, 8, t_z, c_z),
                      PointField(c, 12, t_c, c_c),]

            while line[0:4]!='DATA':
                line = pcdfile.readline()

            data = pcdfile.read()

        separador1 = '\n'
        separador2 = ' '
        lista = data.split(separador1)
        points=[]
        for i in lista:
            m = i.split(separador2)
            m=m[0:4]
            if len(m)==4:
                m = list(map(float, m))
                points.append(m)

    header = Header()
    header.frame_id = "map"
    pc2 = point_cloud2.create_cloud(header, fields, points)

    return pc2

class Publisher:
    def __init__(self, msg_type, topic_name, node_name, topic_frequency, topic_content):
        self.node_name = node_name
        self.topic_frequency = topic_frequency
        self.topic_content = topic_content
        self.simple_publisher = rospy.Publisher(topic_name, msg_type, queue_size = 2)
        self.node_initialization()

    def node_initialization(self):
        rospy.init_node(self.node_name, anonymous = False)
        rate = rospy.Rate(self.topic_frequency)

        while not rospy.is_shutdown():
            self.simple_publisher.publish(self.topic_content)
            rate.sleep()

if __name__ == '__main__':

    msg_type = PointCloud2
    topic_name = 'playtec_pointcloud2'
    node_name = 'pc2_publisher'
    topic_content = pcd_to_pointcloud2(filename)

    try:
        Publisher(msg_type, topic_name, node_name, topic_frequency, topic_content)
    except rospy.ROSInterruptException:
        pass
