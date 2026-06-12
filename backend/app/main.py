import asyncio
import struct
from asyncio import Queue
from contextlib import asynccontextmanager
from dataclasses import dataclass
from typing import Dict

import serial
import uvicorn
from fastapi import FastAPI


@dataclass
class Angles:
    theta: float
    phi: float


command_queue: Queue = Queue()
ARDUINO_UNO = serial.Serial(port="COM7", baudrate=9600, timeout=5)


async def send_angle(theta: float, phi: float) -> bytes:
    print("Send data")
    binary_data = struct.pack("<ff", theta, phi)
    await asyncio.to_thread(ARDUINO_UNO.write, binary_data)
    data = await asyncio.to_thread(ARDUINO_UNO.readline)
    return data


async def queue_worker():
    print("Worker started, serial port open:", ARDUINO_UNO.is_open)
    while True:
        command: Angles = await command_queue.get()
        theta = command.theta
        phi = command.phi
        print(f"Sending theta={theta} phi={phi}")
        response = await send_angle(theta=theta, phi=phi)
        print(f"Arduino response: {response}")
        command_queue.task_done()


@asynccontextmanager
async def lifespan(app: FastAPI):
    task = asyncio.create_task(queue_worker())
    print("Done")
    yield
    print("Task cancel")
    task.cancel()
    ARDUINO_UNO.close()


app = FastAPI(lifespan=lifespan)


@app.get("/moveby")
async def test(theta: float, phi: float):
    command = Angles(theta=theta, phi=phi)
    await command_queue.put(command)
    return {"theta": theta, "phi": phi}


if __name__ == "__main__":
    uvicorn.run(app, port=8080, host="0.0.0.0")
