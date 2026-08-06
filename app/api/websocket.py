import asyncio

from fastapi import APIRouter, WebSocket, WebSocketDisconnect

from app.services.yahoo_service import get_stock_price
from app.utils.logger import logger

router = APIRouter()


@router.websocket("/ws/{symbol}")
async def websocket_endpoint(websocket: WebSocket, symbol: str):

    await websocket.accept()

    logger.info(f"WebSocket connected - {symbol}")

    try:

        while True:

            data = get_stock_price(symbol)

            if data is not None:
                await websocket.send_json(data)
            else:
                logger.warning(f"No data available for {symbol}")

            await asyncio.sleep(3)

    except WebSocketDisconnect:

        logger.info(f"WebSocket disconnected - {symbol}")

    except Exception as e:

        logger.error(f"WebSocket error ({symbol}): {e}")

    finally:

        logger.info(f"WebSocket closed - {symbol}")