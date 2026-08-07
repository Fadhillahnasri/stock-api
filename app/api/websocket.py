from fastapi import APIRouter, WebSocket, WebSocketDisconnect

from app.services.stock_service import get_stock_price
from app.utils.logger import logger


router = APIRouter()


@router.websocket("/ws/stock/{symbol}")
async def stock_websocket(
    websocket: WebSocket,
    symbol: str
):

    await websocket.accept()

    symbol = symbol.upper()

    logger.info(
        f"WebSocket Connected - Stock: {symbol}"
    )

    try:

        while True:

            # Ambil data melalui service
            data = get_stock_price(symbol)

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

            # Menunggu pesan dari client
            message = await websocket.receive_text()

            logger.info(
                f"WebSocket Message - {symbol}: {message}"
            )

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