import asyncio
from fastapi import APIRouter, WebSocket, WebSocketDisconnect

from app.services import get_stock_price

router = APIRouter()


@router.websocket("/ws/{symbol}")
async def websocket_stock(websocket: WebSocket, symbol: str):

    await websocket.accept()

    try:
        while True:

            data = get_stock_price(symbol)

            if data:
                await websocket.send_json(data)
            else:
                await websocket.send_json({
                    "error": "Stock not found"
                })

            await asyncio.sleep(5)

    except WebSocketDisconnect:
        print(f"Client disconnected from {symbol}")