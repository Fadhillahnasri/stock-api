
const WS_BASE_URL = 'ws://127.0.0.1:8000'

export function connectStockWebSocket(
  symbol,
  { onMessage, onStatus, onError } = {},
) {
  const normalizedSymbol = symbol.trim().toUpperCase()

  const socket = new WebSocket(
    `${WS_BASE_URL}/ws/${encodeURIComponent(normalizedSymbol)}`,
  )

  let manuallyDisconnected = false

  socket.onopen = () => {
    if (!manuallyDisconnected) {
      onStatus?.('connected')
    }
  }

  socket.onmessage = (event) => {
    if (manuallyDisconnected) return

    try {
      const data = JSON.parse(event.data)
      onMessage?.(data)
    } catch (error) {
      console.error('Gagal membaca pesan WebSocket:', error)
      onError?.('Format data WebSocket tidak valid.')
    }
  }

  socket.onerror = () => {
    if (manuallyDisconnected) return

    onStatus?.('error')
    onError?.('Koneksi WebSocket mengalami masalah.')
  }

  socket.onclose = () => {
    if (!manuallyDisconnected) {
      onStatus?.('disconnected')
    }
  }

  return {
    socket,

    disconnect() {
      manuallyDisconnected = true

      if (
        socket.readyState === WebSocket.CONNECTING ||
        socket.readyState === WebSocket.OPEN
      ) {
        socket.close()
      }
    },
  }
}

export default connectStockWebSocket
