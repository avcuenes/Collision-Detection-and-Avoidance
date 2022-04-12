"""
Mehmet Enes AVCU
"""

import asyncio
from mavsdk import System
from vehicle_state.vehicle_state import positon,velocity,acceleration
import sys

async def run():
    # Init the drone
    drone = System()
    connection_string = "udp://:145"
    vehicle_ID = sys.argv[1]
    system_address = connection_string + str(int(vehicle_ID)*10 + 30)
    await drone.connect(system_address=system_address)

    # Start the tasks
    asyncio.ensure_future(positon(drone,vehicle_ID=vehicle_ID))
    asyncio.ensure_future(velocity(drone,vehicle_ID=vehicle_ID))
    asyncio.ensure_future(acceleration(drone,vehicle_ID=vehicle_ID))
    
    #asyncio.ensure_future(velocity(drone))
    


async def print_battery(drone):
    async for battery in drone.telemetry.imu():
        print(f"Battery: {battery.acceleration_frd.forward_m_s2}")


async def print_gps_info(drone):
    async for gps_info in drone.telemetry.gps_info():
        print(f"GPS info: {gps_info}")


async def print_in_air(drone):
    async for in_air in drone.telemetry.in_air():
        print(f"In air: {in_air}")




if __name__ == "__main__":
    # Start the main function
    asyncio.ensure_future(run())

    # Runs the event loop until the program is canceled with e.g. CTRL-C
    asyncio.get_event_loop().run_forever()
