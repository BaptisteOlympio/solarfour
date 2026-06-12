import asyncio
import json
import struct
from asyncio import Queue
from contextlib import asynccontextmanager
from dataclasses import dataclass
from typing import Dict

import serial
import uvicorn
from fastapi import FastAPI, WebSocket
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse


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

# Configure CORS to allow connections from the UI
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    try:
        while True:
            data = await websocket.receive_text()
            try:
                message = json.loads(data)
                theta = float(message.get("theta", 0))
                phi = float(message.get("phi", 0))
                command = Angles(theta=theta, phi=phi)
                await command_queue.put(command)
                await websocket.send_text(
                    json.dumps({"status": "ok", "theta": theta, "phi": phi})
                )
            except (json.JSONDecodeError, KeyError, ValueError) as e:
                await websocket.send_text(
                    json.dumps({"status": "error", "message": str(e)})
                )
    except Exception as e:
        print(f"WebSocket error: {e}")
    finally:
        print("WebSocket disconnected")


if __name__ == "__main__":
    uvicorn.run(app, port=8080, host="0.0.0.0")
