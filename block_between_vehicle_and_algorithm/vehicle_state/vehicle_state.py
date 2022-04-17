"""
Mehmet Enes AVCU    
"""
import asyncio
from turtle import pos
from mavsdk import System
import rclpy
from rclpy.node import Node

from geometry_msgs.msg import Point,Twist,Accel


async def positon(drone,vehicle_ID:int):
    """_summary_
    This function read position data from vehicle and publish it
    Args:
        drone (_type_): _description_
        vehicle_ID (int): _description_ Vehicle ID number
    """
    async for position in drone.telemetry.position():
        rclpy.init(args=None)
        publisher_node_name = 'Position_publisher_' + vehicle_ID
        node = rclpy.create_node(publisher_node_name)
        topic_name ='Position_Vehicle' + vehicle_ID
        publisher = node.create_publisher(Point, topic_name, 10)

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


async def velocity(drone,vehicle_ID:int):
    """_summary_
    This function read velocity data from vehicle and publish it
    Args:
        drone (_type_): _description_
        vehicle_ID (int): _description_ Vehicle ID number
    """
    async for velocity in drone.telemetry.velocity_ned():
        rclpy.init(args=None)
        publisher_node_name = 'Velocity_publisher_' + vehicle_ID
        node = rclpy.create_node(publisher_node_name)
        topic_name = 'Velocity_vehicle' + vehicle_ID
        publisher = node.create_publisher(Twist, topic_name, 10)

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


async def acceleration(drone,vehicle_ID:int):
    """_summary_
    This function read acceleration data from vehicle and publish it
    Args:
        drone (_type_): _description_
        vehicle_ID (_type_): _description_ Vehicle ID number
    """
    async for acceleration in drone.telemetry.imu():
        rclpy.init(args=None)
        publisher_node_name = 'Acceleration_publisher_' + vehicle_ID
        node = rclpy.create_node(publisher_node_name)
        topic_name = 'Acceleration_vehicle' + vehicle_ID
        publisher = node.create_publisher(Accel, topic_name, 10)

        msg = Accel()
        def timer_callback():
            msg.linear.x = acceleration.acceleration_frd.forward_m_s2
            msg.linear.y = acceleration.acceleration_frd.right_m_s2
            msg.linear.z = acceleration.acceleration_frd.down_m_s2
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