from fastapi import BackgroundTasks, FastAPI
from pydantic import BaseModel

from uav import UAV

app = FastAPI()

drone = UAV()

class InitItem(BaseModel):
    outx: int
    outy: int
    inx: int
    iny: int
    dc_id: str

class Move(BaseModel):
    outx: int
    outy: int
    inx: int
    iny: int
 
@app.get("/status")
def get_status():
    return drone.get_status()

@app.post("/init")
async def init_drone(body: InitItem, background_tasks: BackgroundTasks):
    drone.init_position((body.outx, body.outy, 
                         body.inx, body.iny), 
                            body.dc_id)
    background_tasks.add_task(drone.transmit_payload)
    print(drone.get_status())
    return

@app.post("/move")
async def move_drone(move: Move, background_tasks: BackgroundTasks):
    drone.move((move.outx, move.outy, 
                    move.inx, move.iny))
    background_tasks.add_task(drone.transmit_payload)
    print(get_status())
    return
