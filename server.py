import http.server
import socketserver
import os
import sys
import json
import threading
import time
import live_sync

PORT = 3000
DIRECTORY = os.path.dirname(os.path.abspath(__file__))

class DynamicDashboardHandler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=DIRECTORY, **kwargs)
        
    def end_headers(self):
        self.send_header('Cache-Control', 'no-store, no-cache, must-revalidate, max-age=0')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        super().end_headers()

    def do_OPTIONS(self):
        self.send_response(200)
        self.end_headers()

    def do_GET(self):
        # API: /api/sync -> Force live re-fetch from Google Sheets
        if self.path.startswith('/api/sync'):
            try:
                res = live_sync.sync_now()
                self.send_response(200)
                self.send_header('Content-Type', 'application/json')
                self.end_headers()
                self.wfile.write(json.dumps(res).encode('utf-8'))
            except Exception as e:
                self.send_response(500)
                self.send_header('Content-Type', 'application/json')
                self.end_headers()
                self.wfile.write(json.dumps({'status': 'error', 'message': str(e)}).encode('utf-8'))
            return

        # API: /api/status -> Return sync health
        if self.path.startswith('/api/status'):
            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
            status_data = {
                'status': 'online',
                'isLiveLinked': True,
                'spreadsheetId': live_sync.SHEET_ID,
                'lastSynced': live_sync._cache.get('last_synced'),
                'isSyncing': live_sync._cache.get('is_syncing', False)
            }
            self.wfile.write(json.dumps(status_data).encode('utf-8'))
            return

        # Fallback to static files
        super().do_GET()

def background_periodic_sync():
    """Background thread that automatically syncs from Google Sheets every 90 seconds"""
    while True:
        try:
            time.sleep(90)
            print("[Auto-Sync] Polling latest changes from Google Sheet...")
            live_sync.sync_now()
            print("[Auto-Sync] Live Google Sheet data refreshed successfully!")
        except Exception as e:
            print(f"[Auto-Sync Error] {e}")

if __name__ == '__main__':
    # Start background auto-sync thread
    sync_thread = threading.Thread(target=background_periodic_sync, daemon=True)
    sync_thread.start()

    with socketserver.TCPServer(("", PORT), DynamicDashboardHandler) as httpd:
        print(f"Dynamic Glassmorphic Dashboard serving at http://localhost:{PORT}")
        print("Connected directly to Google Spreadsheet:", live_sync.SHEET_ID)
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            pass
