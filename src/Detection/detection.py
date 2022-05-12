""" 
Mehmet Enes AVCU
"""
import sys

import rclpy
from geometry_msgs.msg import Accel, Point, Twist
from lib.geomath import *
from rclpy.node import Node
import numpy as np


class Detection:
    def __init__(self,Vehicle_Own_ID:int, Number_of_Agent:float, Min_distance_btw_agent:float):
        self.Vehicle_Own_ID = Vehicle_Own_ID 
        self.Number_of_Agent = Number_of_Agent
        self.Min_distance = Min_distance_btw_agent
        self.Update_Velocity_of_Vehicles()
        

    def Subscribe_Velocity_of_Agent(self,Vehicle_ID:int,args=None):
        """
        This function subscribe other agents velocity
        """
        rclpy.init(args=args)
        node_name = 'velocity_subscribe_' + str(Vehicle_ID)
        velocity_node = rclpy.create_node(node_name)
        topic_name = 'Velocity_vehicle' + str(Vehicle_ID)
        self.Vehicle_ID = Vehicle_ID
        print(topic_name)
        subscription = velocity_node.create_subscription(Twist, topic_name, self.Velocity_Callback, 10)
        subscription  # prevent unused variable warning

        if rclpy.ok():
            rclpy.spin_once(velocity_node)

        # Destroy the node explicitly
        # (optional - otherwise it will be done automatically
        # when the garbage collector destroys the node object)
        velocity_node.destroy_node()
        rclpy.shutdown()
    
    def Velocity_Callback(self,msg):
        """
        This function callback function of velocity message

        Args:
            msg (_type_): _description_
        """
        self.Velocity_of_Vehicles.append([self.Vehicle_ID,msg.linear.x, msg.linear.y, msg.linear.z])        
        
    def Update_Velocity_of_Vehicles(self):
        """
        This function subscribe velocity of agents and update velocity of vehicles
        """
        self.Velocity_of_Vehicles = []
        for i in range(0,self.Number_of_Agent):
            self.Subscribe_Velocity_of_Agent(Vehicle_ID=i)
    
    def Subscribe_Position_of_Agent(self,Vehicle_ID:int,args=None):
        """
        This function subscribe other agents velocity
        """
        rclpy.init(args=args)
        node_name = 'position_subscribe_' + str(Vehicle_ID)
        velocity_node = rclpy.create_node(node_name)
        topic_name = 'Position_Vehicle' + str(Vehicle_ID)
        self.Vehicle_ID = Vehicle_ID
        print(topic_name)
        subscription = velocity_node.create_subscription(Point, topic_name, self.Position_Callback, 10)
        subscription  # prevent unused variable warning

        if rclpy.ok():
            rclpy.spin_once(velocity_node)

        # Destroy the node explicitly
        # (optional - otherwise it will be done automatically
        # when the garbage collector destroys the node object)
        velocity_node.destroy_node()
        rclpy.shutdown()
    
    def Position_Callback(self,msg):
        """
        This function callback function of velocity message

        Args:
            msg (_type_): _description_
        """
        self.Position_of_Vehicles.append([self.Vehicle_ID,msg.x, msg.y, msg.z])        
        
    def Update_Position_of_Vehicles(self):
        """
        This function subscribe velocity of agents and update velocity of vehicles
        """
        self.Position_of_Vehicles = []
        for i in range(0,self.Number_of_Agent):
            self.Subscribe_Position_of_Agent(Vehicle_ID=i)
    
    
    
    def Update_relative_velocity(self):
        """
        This function calculate relative velocity of agents respect to ID
        """
        self.relativevelocity = []
        for i in range(0,self.Number_of_Agent):
            if i == self.Vehicle_Own_ID:
                break
            else:
                relative_velocity_x = self.Velocity_of_Vehicles[i][1] -self.Velocity_of_Vehicles[self.Vehicle_Own_ID][1]
                relative_velocity_y = self.Velocity_of_Vehicles[i][2] -self.Velocity_of_Vehicles[self.Vehicle_Own_ID][2]
                relative_velocity_z = self.Velocity_of_Vehicles[i][3] -self.Velocity_of_Vehicles[self.Vehicle_Own_ID][3]
                relativeID = str(i) + str(self.Vehicle_Own_ID)
                relative_velocityxyz = np.sqrt(relative_velocity_x**2 + relative_velocity_y**2 + relative_velocity_z**2)
                self.relativevelocity.append([relativeID,relative_velocityxyz, relative_velocity_x, relative_velocity_y, relative_velocity_z])
    
    def Update_relative_position(self):
        """
        This function calculate relative position of agents respect to ID
        """
        self.relativedistance = []
        for i in range(0,self.Number_of_Agent):
            if i == self.Vehicle_Own_ID:
                break
            else:
                #latitude and longitude distance between agents
                latlondistance = formulation_of_haversine(loc1=[self.Position_of_Vehicles[i][1],self.Position_of_Vehicles[i][2]],loc2=[self.Position_of_Vehicles[self.Vehicle_Own_ID][1],self.Position_of_Vehicles[self.Vehicle_Own_ID][2]])
                #altitdude distance between agents
                relativealtdistance = self.Position_of_Vehicles[i][3]-self.Position_of_Vehicles[self.Vehicle_Own_ID][3]
                
                relativedistance = np.sqrt(latlondistance**2 + relativealtdistance**2)
                relativeverticaldistance = vertical_horizontal_haversine(loc1=[self.Position_of_Vehicles[i][1],self.Position_of_Vehicles[i][2]],loc2=[self.Position_of_Vehicles[self.Vehicle_Own_ID][1],self.Position_of_Vehicles[self.Vehicle_Own_ID][2]],ver_hor='v')
                relativehorizontaldistance = vertical_horizontal_haversine(loc1=[self.Position_of_Vehicles[i][1],self.Position_of_Vehicles[i][2]],loc2=[self.Position_of_Vehicles[self.Vehicle_Own_ID][1],self.Position_of_Vehicles[self.Vehicle_Own_ID][2]],ver_hor='h')
                
                relativeID = str(i) + str(self.Vehicle_Own_ID)
                self.relativedistance.append([relativeID , relativedistance,relativehorizontaldistance,relativeverticaldistance,relativealtdistance])

        
    def Detection_Calculation(self):
        """
        This function calculate detection formula
        """
        self.rij = []
        for i in range(0,self.Number_of_Agent):
            if i == self.Vehicle_Own_ID:
                break
            else:    
                dij = [self.relativedistance[i][2],self.relativedistance[i][3],self.relativedistance[i][4]]
                Vij = [self.relativevelocity[i][2],self.relativevelocity[i][3],self.relativevelocity[i][4]]
                part1 = Vectoral_multiplication(vec1=dij,vec2=Vij)
                part2 = Vector_norm(Vij)
                part3 = part1/part2
                part4 = part3*Vij
                part5 = part4-dij
                self.rij.append(part5)
            
    def Detection(self):
        """
        This function detect collision
        """
        self.Detection_Calculation()
        self.norm_of_rij = []
        for i in self.rij:
            self.norm_of_rij.append(Vector_norm(i))
        
        min_distance = min(self.norm_of_rij)
        
        if min_distance <= self.Min_distance:
            Detection = True
        else:
            Detection = False
        
        return Detection

        
    def Update(self):
        """
        This function update all variable
        """ 
        self.Update_Position_of_Vehicles()
        self.Update_Velocity_of_Vehicles()
        self.Update_relative_velocity()
        self.Update_relative_position()
    def Run(self):
        """
        This function main function of detection algorithm
        """
        self.Update()
        self.Detection()
        
        
        
        
            
        
        



if __name__ == "__main__":
    number_of_agent = sys.argv[1]
    vehicle_ID = sys.argv[2]
    
    D = Detection(Vehicle_Own_ID=vehicle_ID,Number_of_Agent=number_of_agent)




























