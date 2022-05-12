"""
Mehmet Enes AVCU
"""

import asyncio
from turtle import position
from mavsdk import System
from vehicle_state.vehicle_state import positon,velocity,acceleration
from action.action import Action
import sys

async def run():
    # Init the drone
    vehicle_ID = sys.argv[1]
    system_add = "5004" + str(vehicle_ID)
    drone = System(mavsdk_server_address="localhost", port=system_add)
    connection_string = "udp://:1454"
    
    
    system_address = connection_string + str(int(vehicle_ID))
    await drone.connect(system_address=system_address)
    print("connect")
    # Start the tasks
    #asyncio.ensure_future(positon(drone,vehicle_ID=vehicle_ID))
    A = Action(Drone=drone,Vehicle_ID=vehicle_ID)
    f1 = asyncio.ensure_future(positon(drone,vehicle_ID=vehicle_ID))

    while True:
            
        #asyncio.ensure_future(acceleration(drone,vehicle_ID=vehicle_ID))
        f2 = asyncio.ensure_future(A.goto())
        await asyncio.wait([f2])
        
    #asyncio.ensure_future(velocity(drone))
    




if __name__ == "__main__":
    # Start the main function
    asyncio.ensure_future(run())

    # Runs the event loop until the program is canceled with e.g. CTRL-C
    asyncio.get_event_loop().run_forever()
