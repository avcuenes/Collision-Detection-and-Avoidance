"""
Mehmet Enes AVCU    
"""
import asyncio
from turtle import pos
from mavsdk import System
import rclpy
from rclpy.node import Node

from std_msgs.msg import String,Float32MultiArray
from geometry_msgs.msg import Point,Twist
from nav_msgs.msg import Odometry


async def positon(drone):
    async for position in drone.telemetry.position():
        rclpy.init(args=None)
        node = rclpy.create_node('Position_publisher')
        publisher = node.create_publisher(Point, 'Position_Vehicle', 10)

        msg = Point()
        def timer_callback():
            msg.x = position.latitude_deg
            msg.y = position.longitude_deg
            msg.z = position.relative_altitude_m
            node.get_logger().info('Publishing: "%s"' % msg)
            publisher.publish(msg)

        timer_period = 0.5  # seconds
        timer = node.create_timer(timer_period, timer_callback)

        rclpy.spin_once(node)

        # Destroy the timer attached to the node explicitly
        # (optional - otherwise it will be done automatically
        # when the garbage collector destroys the node object)
        node.destroy_timer(timer)
        node.destroy_node()
        rclpy.shutdown()


async def velocity(drone):
    async for velocity in drone.telemetry.velocity_ned():
        rclpy.init(args=None)
        node = rclpy.create_node('Velocity_publisher')
        publisher = node.create_publisher(Twist, 'Velocity_vehicle', 10)

        msg = Twist()
        def timer_callback():
            msg.linear.x = velocity.north_m_s
            msg.linear.y = velocity.east_m_s
            msg.linear.z = velocity.down_m_s
            node.get_logger().info('Publishing: "%s"' % msg)
            publisher.publish(msg)

        timer_period = 0.5  # seconds
        timer = node.create_timer(timer_period, timer_callback)

        rclpy.spin_once(node)

        # Destroy the timer attached to the node explicitly
        # (optional - otherwise it will be done automatically
        # when the garbage collector destroys the node object)
        node.destroy_timer(timer)
        node.destroy_node()
        rclpy.shutdown()
