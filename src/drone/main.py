import asyncio

from uav import UAV

drone = UAV()

asyncio.run(drone.fly())
