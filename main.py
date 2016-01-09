import pygame
import xml.sax
import time

transparency_color = pygame.Color('#ffffff')

class Tileset: 
	rows = 0
	columns = 0
	def __init__(self, tile_width, tile_height, filepath):
		image = pygame.image.load(filepath).convert()
		image.set_colorkey((transparency_color))
		self.height = image.get_height()
		self.width = image.get_width()
		rows = int(self.height / tile_height)
		columns = int(self.width / tile_width)
		self.tiles = []

		for row in range(0, rows):
			for column in range (0, columns):
				tile = pygame.Rect(column*tile_width, row*tile_height,
									tile_width, tile_height)
				tile_subsurface = image.subsurface(tile)
				self.tiles.append(tile_subsurface)

		print("Produced " + str(len(self.tiles)) + "tiles as subsurfaces.")



class TMXHandler(xml.sax.ContentHandler):
	def __init__(self):
		self.content = ""
		self.image_source = ""
		self.width = ""
		self.height = ""
		self.tile_width = ""
		self.tile_height = ""
		self.column = 0
		self.row = 0
		self.map_size = ()
		self.tileset = None
		self.surface = None

	def startElement(self, name, attr):
		self.content = name
		if name == "map":
			self.width = int(attr["width"])
			self.height = int(attr["height"])
			self.tile_width = int(attr["tilewidth"])
			self.tile_height = int(attr["tileheight"])
			self.map_size = (self.width * self.tile_width,
							 self.height * self.tile_height)
			self.surface = pygame.Surface(self.map_size)

		elif name == "image":
			self.tileset = Tileset(self.tile_width, self.tile_height, "./assets/tiles/demo_tiles.png") # VERY IMPORTANT, HARDCODED FOR DEMO
		elif name == "layer":
			print(attr["name"])
			self.column = 0
			self.row = 0
		elif name == "tile":
			gid = int(attr["gid"])
			tile = self.tileset.tiles[gid-1]
			position = (self.column*self.tile_width, self.row*self.tile_height)
			self.surface.blit(tile, position)
			self.column += 1
			if self.column >= (self.width):
				self.column = 0
				self.row += 1
			




			
def createHandler(file_name): 
	"""This function creates an XML parser object."""
	parser = xml.sax.make_parser()
	handler = TMXHandler()
	parser.setContentHandler(handler)
	parser.parse(file_name) #parses the XML data
	return handler

if __name__ == "__main__":
	pygame.init()
	gameDisplay = pygame.display.set_mode((640, 640)) 
	demo_data = createHandler("./assets/maps/demo.tmx")
	gameDisplay.fill((0,0,0))
	gameDisplay.blit(demo_data.surface, (0,0))
	pygame.display.update()
	time.sleep(5)

	





