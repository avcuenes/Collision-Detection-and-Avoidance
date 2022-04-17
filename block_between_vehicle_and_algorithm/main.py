"""
Mehmet Enes AVCU
"""

import asyncio
from mavsdk import System
from vehicle_state.vehicle_state import positon,velocity,acceleration
from action.action import Action
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
    A = Action(Drone=drone,Vehicle_ID=vehicle_ID)
    asyncio.ensure_future(A.goto())
    
    #asyncio.ensure_future(velocity(drone))
    




if __name__ == "__main__":
    # Start the main function
    asyncio.ensure_future(run())

    # Runs the event loop until the program is canceled with e.g. CTRL-C
    asyncio.get_event_loop().run_forever()
