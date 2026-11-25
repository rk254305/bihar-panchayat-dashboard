import urllib.request

req = urllib.request.urlopen('http://localhost:3000')
html = req.read().decode('utf-8')
print('Server status:', req.status)
print('page-zoom-level in html:', 'id="page-zoom-level"' in html)
print('floating-zoom-level in html:', 'id="floating-zoom-level"' in html)
print('map-zoom-level in html:', 'id="map-zoom-level"' in html)
print('main-app-container in html:', 'id="main-app-container"' in html)
print('changePageZoom in html:', 'changePageZoom' in html)
print('togglePageFitWidth in html:', 'togglePageFitWidth' in html)
