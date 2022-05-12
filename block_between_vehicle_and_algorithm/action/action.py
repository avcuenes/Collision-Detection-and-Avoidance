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
        print("ssssssssssss",msg)
        
    def goto_sub(self):
        print("got")
        rclpy.init(args=None)

        g_node = rclpy.create_node('Position_subs')
        topic_name ='Position_Vehicle' + str(1)

        subscription = g_node.create_subscription(Point, topic_name, self.position_sub, 1)

        if rclpy.ok():
            print("ok")
            rclpy.spin_once(g_node,timeout_sec=1)
        # Destroy the node explicitly
        # (optional - otherwise it will be done automatically
        # when the garbage collector destroys the node object)
        print("ros init")

        rclpy.shutdown()
        
    async def goto(self):
        self.goto_sub()
        #await asyncio.sleep(0.01)
        await self.drone.action.goto_location(1,1,1,1)
        print(self.lat)
        #while 1:
        #    self.goto_sub()
        #    print("gptp")
        #    #await  self.drone.action.goto_location(self.lat, self.lon, self.alt, 0)
        

if __name__=="__main__":
    A = Action(1,1)
    A.goto_sub()