import http.server
import socketserver
import webbrowser
import os
from urllib.parse import urlparse

# Konfigurera port
PORT = 8080

# Skapa en enkel HTTP-server
Handler = http.server.SimpleHTTPRequestHandler

print(f"Startar lokal server på port {PORT}...")
print(f"Öppnar webbläsare för förhandsgranskning...")

# Starta webbläsaren med adressen
webbrowser.open(f'http://localhost:{PORT}')

# Starta servern
with socketserver.TCPServer(("", PORT), Handler) as httpd:
    print(f"Server igång på http://localhost:{PORT}")
    print("Tryck Ctrl+C för att avsluta")
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\nAvslutar server...")
        httpd.shutdown()