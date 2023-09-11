from fastapi import FastAPI

from uav import UAV

app = FastAPI()

drone = UAV()

@app.get("/status")
def get_status():
    return drone.get_status()

@app.post("/init")
async def init_drone(body):
    drone.init_position((body['outx'], body['outy'], body['inx'],
                         body['iny']), body['id'])
    return

@app.post("/move")
async def move_drone(body):
    drone.move((body['outx'], body['outy'], body['inx'],
                         body['iny']))
    drone.transmit_payload()
    return
