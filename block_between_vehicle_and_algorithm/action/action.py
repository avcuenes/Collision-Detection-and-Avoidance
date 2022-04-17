"""
Mehmet Enes AVCU
"""
import asyncio
import rclpy
from geometry_msgs.msg import Point,Twist,Accel
from rclpy.node import Node



class Action:
    def __init__(self,Drone,Vehicle_ID:float):
        self.drone = Drone
        self.Vehicle_ID = Vehicle_ID
        self.alt = 0
        self.lat = 0
        self.lon = 0
        
    async def takeoff(self):
        await self.drone.action.takeoff()

    async def arm(self):
        await self.drone.action.arm()
    
    def position_sub(self,msg):
        self.lat = msg.x
        self.lon = msg.y
        self.alt = msg.z
        
    def goto_sub(self):
        rclpy.init(args=None)

        g_node = rclpy.create_node('Position_subs')
        topic_name ='Position_Vehicle' + str(self.Vehicle_ID)

        subscription = g_node.create_subscription(Point, topic_name, self.position_sub, 10)
        subscription  # prevent unused variable warning

        if rclpy.ok():
            rclpy.spin_once(g_node)
        # Destroy the node explicitly
        # (optional - otherwise it will be done automatically
        # when the garbage collector destroys the node object)
        g_node.destroy_node()
        rclpy.shutdown()
        
    async def goto(self):
        print(self.lat)
        await  self.drone.action.goto_location(self.lat, self.lon, self.alt, 0)
        

if __name__=="__main__":
    A = Action(1,1)
    A.goto_sub()