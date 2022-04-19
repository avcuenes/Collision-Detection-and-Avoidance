""" 
Mehmet Enes AVCU
"""
from tkinter import NO
from geometry_msgs.msg import Point,Twist,Accel
import rclpy
from rclpy.node import Node
import sys


class Detection:
    def __init__(self,Vehicle_Own_ID:int, Number_of_Agent:float):
        self.Vehicle_Own_ID = Vehicle_Own_ID 
        self.Number_of_Agent = Number_of_Agent
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
    
    def Update(self):
        """
        This function update all variable
        """
        self.Update_Velocity_of_Vehicles()
        self.Update_relative_velocity()
    
    def Update_relative_velocity(self):
        """
        This function calculate relative velocity of agents respect to ID
        """
        self.relativevelocity = []
        for i in range(0,self.Number_of_Agent-1):
            if i == self.Vehicle_Own_ID:
                break
            else:
                relative_velocity_x = self.Velocity_of_Vehicles[i][1] -self.Velocity_of_Vehicles[self.Vehicle_Own_ID][1]
                relative_velocity_y = self.Velocity_of_Vehicles[i][2] -self.Velocity_of_Vehicles[self.Vehicle_Own_ID][2]
                relative_velocity_z = self.Velocity_of_Vehicles[i][3] -self.Velocity_of_Vehicles[self.Vehicle_Own_ID][3]
                relativeID = str(i) + str(self.Vehicle_Own_ID)
                self.relativevelocity.append([relativeID, relative_velocity_x, relative_velocity_y, relative_velocity_z])
    
    def Update_relative_position(self):
        """
        This function calculate relative position of agents respect to ID
        """      
    
    def Detection(self):
        """
        This function detect collision
        """
        
    def Run(self):
        """
        This function main function of detection algorithm
        """
        self.Update()
        
        
        
            
        
        



if __name__ == "__main__":
    number_of_agent = sys.argv[1]
    vehicle_ID = sys.argv[2]
    
    D = Detection(Vehicle_Own_ID=vehicle_ID,Number_of_Agent=number_of_agent)




























