import urllib2, os
from gi.repository import Gtk

LASTFM_API_KEY = 'e92e11a5f1a8f8f154b45face4398499' #My Personal LastFM key, get your own if using this code in another application
USERAGENT = 'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.1) Gecko/2008072820 Firefox/7.0.0'
CACHEFILE = '/home/mike/Desktop/tempimg.jpg'
PLACEHOLDER = '/home/mike/Desktop/Python/IconoClast/iconoclast/iconoclast.png'

class getCover:
	def getLastFMCover(self, artist, album):
		url = 'http://ws.audioscrobbler.com/2.0/?method=album.getinfo&api_key=%s&artist=%s&album=%s' % (LASTFM_API_KEY, artist, album)
		request = urllib2.Request(url, headers = {'User-Agent': USERAGENT})
		try:
			stream = urllib2.urlopen(request)
			data = stream.read()

			startIdx  = data.find('<image size="large">')
			endIdx    = data.find('</image>', startIdx)
			if startIdx != -1 and endIdx != -1:
			    coverURL    = data[startIdx+len('<image size="large">'):endIdx]

			request = urllib2.Request(coverURL, headers = {'User-Agent': USERAGENT})
			stream  = urllib2.urlopen(request)
			data    = stream.read()
			output = open(CACHEFILE, 'wb')
			output.write(data)
			output.close()
			return True
		except:
			return False

	def getLocalCover(self, filelocation=None):
		if filelocation:
			self.folderjpg = os.path.split(filelocation)[0] + '/' + 'Folder.jpg'
			if os.path.exists(self.folderjpg):
				stream = open(self.folderjpg, 'r')
				data = stream.read()			
				return True
			else:
				return False
		return False

	def returnCover(self, artist, album, filelocation=None):
		img = Gtk.Image()
		if self.getLocalCover(filelocation):
			img.set_from_file(self.folderjpg)
		elif self.getLastFMCover(artist, album):		
			img.set_from_file(CACHEFILE)
		else:
			img.set_from_file(PLACEHOLDER)
		return img

"""#Debugging stuff and example usage below this, comment out when in use
coverFetch = getCover()
img = coverFetch.returnCover('symphony%20X', 'Iconoclast', '/media/Media/Music/Babyshambles/Down In Albion/2 - Fuck Forever.mp3')

win = Gtk.Window()
win.connect("delete-event", Gtk.main_quit)
win.add(img)

win.show_all()
Gtk.main()"""