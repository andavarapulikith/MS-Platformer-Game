class MAP_ONE:
    def __init__(self, block_size, width, height,fire_width,fire_height):
        self.block_size = block_size
        self.width = width
        self.height = height
        self.fire_width = fire_width
        self.fire_height = fire_height

    def get_blocks(self):
      # Create a list of blocks
      blocks = [] 

      bricks = [
          (0,0,"brick"),(0,48,"brick"),(0,96,"brick"),(0,144,"brick"),
          (0,192,"brick"),(0,240,"brick"),(0,288,"brick"),(0,336,"brick"),
          (0,384,"brick"),(0,432,"brick"),(0,480,"brick"),(0,528,"brick"),
          (0,576,"brick"),(0,624,"brick"),(336,528,"brick"),(384,480,"brick"),
          (432,432,"brick"),(576,384,"brick"),(576,432,"brick"),(576,480,"brick"),
          (576,528,"brick"),(576,576,"brick"),(576,624,"brick"),(864,576,"brick"),
          (1008,480,"brick"),(1200,576,"brick"),(1200,624,"brick"),(1392,528,"brick"),
          (1392,576,"brick"),(1392,624,"brick"),(1584,432,"brick"),(1961,528,"brick"),
          (2304,576,"brick"),(2304,624,"brick"),(2688,624,"brick"),(2832,496,"brick"),
          (2976,392,"brick")
      ]

      grounds = [
         (0,672,"ground"),(48,672,"ground"),(96,672,"ground"),(144,672,"ground"),
         (192,672,"ground"),(240,672,"ground"),(288,672,"ground"),(336,672,"ground"),
         (384,672,"ground"),(432,672,"ground"),(480,672,"ground"),(528,672,"ground"),
         (576,672,"ground"),(624,672,"ground"),(672,672,"ground"),(720,672,"ground"),
         (1152,672,"ground"),(1200,672,"ground"),(1248,672,"ground"),(1296,672,"ground"),
         (1344,672,"ground"),(1392,672,"ground"),(1776,672,"ground"),(1824,672,"ground"),
         (2160,672,"ground"),(2208,672,"ground"),(2256,672,"ground"),(2304,672,"ground"),
         (2352,672,"ground"),(2400,672,"ground"),(2448,672,"ground"),(2496,672,"ground"),
         (2544,672,"ground"),(2592,672,"ground"),(2640,672,"ground"),(2688,672,"ground"),
         (3120,672,"ground"),(3168,672,"ground"),(3216,672,"ground"),(3264,672,"ground"),
         (3312,672,"ground"),(3360,672,"ground"),(3408,672,"ground"),(3456,672,"ground"),
         (3504,672,"ground"),(3552,672,"ground"),(3600,672,"ground"),(3648,672,"ground"),
         (3696,672,"ground")
      ]
      
      # append bricks to blocks
      blocks.extend(bricks)

      # append grounds to blocks
      blocks.extend(grounds)

      return blocks

    def get_fires(self):
      # Create a list of fire
      fire_coords = [
         (392,432),(1304,624),(2456,624),
         (3320,624)
      ]

      return fire_coords

    def get_fruits(self):
        # Create a list of fruits
        fruits = [
           (152,624,"Cherries"),(240,392,"Cherries"),(392,536,"Cherries"),(440,488,"Cherries"),
           (584,344,"Cherries"),(872,536,"Cherries"),(1016,440,"Cherries"),(1208,536,"Cherries"),
           (1400,488,"Cherries"),(1784,640,"Cherries"),(1969,488,"Cherries"),(2216,640,"Cherries"),
           (2456,544,"Cherries"),(2840,448,"Cherries"),(2984,344,"Cherries"),(3128,616,"Cherries"),

        ]
    
        return fruits

