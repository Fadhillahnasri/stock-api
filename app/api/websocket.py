import asyncio

from fastapi import APIRouter, WebSocket, WebSocketDisconnect

from app.services.stock_service import get_stock_price
from app.utils.logger import logger


router = APIRouter()


@router.websocket("/ws/{symbol}")
async def stock_websocket(
    websocket: WebSocket,
    symbol: str
):

    symbol = symbol.upper()

    logger.info(
        f"WebSocket Connection Attempt - Stock: {symbol}"
    )

    await websocket.accept()

    logger.info(
        f"WebSocket Connected - Stock: {symbol}"
    )

    try:

        while True:

            # Ambil data saham
            data = await asyncio.to_thread(
                get_stock_price,
                symbol
            )

            # Jika data tidak ditemukan
            if data is None:

                logger.warning(
                    f"WebSocket - Stock not found: {symbol}"
                )

                await websocket.send_json({
                    "success": False,
                    "message": f"Stock '{symbol}' not found."
                })

                break

            # Kirim data ke client
            await websocket.send_json({
                "success": True,
                "provider": "Yahoo Finance",
                "data": data
            })

            logger.info(
                f"WebSocket Update Sent - Stock: {symbol}"
            )

            # Tunggu 5 detik sebelum mengambil data lagi
            await asyncio.sleep(5)


    except WebSocketDisconnect:

        logger.info(
            f"WebSocket Disconnected - Stock: {symbol}"
        )


    except Exception as e:

        logger.exception(
            f"WebSocket Error - {symbol}: {e}"
        )

        try:

            await websocket.send_json({
                "success": False,
                "message": "Internal server error"
            })

        except Exception:
            pass