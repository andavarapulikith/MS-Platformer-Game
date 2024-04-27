# return a dict with the map of the easy level
class MAP_TWO:
    def __init__(self, block_size, width, height,fire_width,fire_height):
        self.block_size = block_size
        self.width = width
        self.height = height
        self.fire_width = fire_width
        self.fire_height = fire_height

    def get_blocks(self):
      # Create a list of blocks

      blocks = []
      gold_blocks = [
         (0,0,"gold block"),(0,48,"gold block"),(0,96,"gold block"),(0,144,"gold block"),
         (0,192,"gold block"),(0,240,"gold block"),(0,288,"gold block"),(0,336,"gold block"),
         (0,384,"gold block"),(0,432,"gold block"),(0,480,"gold block"),(0,528,"gold block"),
         (0,576,"gold block"),(0,624,"gold block"),(312,576,"gold block"),(408,504,"gold block"),
         (504,432,"gold block"),(552,432,"gold block"),(600,432,"gold block"),(600,480,"gold block"),
         (600,528,"gold block"),(600,576,"gold block"),(600,624,"gold block"),(1080,624,"gold block"),
         (1080,576,"gold block"),(1080,528,"gold block"),(768,402,"gold block"),(888,472,"gold block"),
         (1254,528,"gold block"),(1446,488,"gold block"),(1606,418,"gold block"),(1774,338,"gold block"),
         (1918,426,"gold block"),(2037,598,"gold block"),(2478,571,"gold block"),(2573,460,"gold block"),
         (2705,381,"gold block"),(2982,624,"gold block"),(2982,576,"gold block"),(2982,528,"gold block"),
         (3154,459,"gold block"),(3462,576,"gold block"),(3602,483,"gold block"),(3815,624,"gold block")
      ]
      
      grounds = [
         (0,672,"ground"),(48,672,"ground"),(96,672,"ground"),(144,672,"ground"),(192,672,"ground"),
         (600,672,"ground"),(648,672,"ground"),(696,672,"ground"),(744,672,"ground"),
         (792,672,"ground"),(840,672,"ground"),(888,672,"ground"),(936,672,"ground"),(984,672,"ground"),
         (1032,672,"ground"),(1080,672,"ground"),(1328,672,"ground"),(1376,672,"ground"),(1510,672,"ground"),
         (1558,672,"ground"),(1606,672,"ground"),(1654,672,"ground"),(1702,672,"ground"),(1750,672,"ground"),
         (1918,672,"ground"),(2166,672,"ground"),(2214,672,"ground"),(2262,672,"ground"),(2310,672,"ground"),
         (2358,672,"ground"),(2838,672,"ground"),(2886,672,"ground"),(2934,672,"ground"),(2982,672,"ground"),
         (3303,672,"ground"),(3351,672,"ground"),(3719,672,"ground"),(3767,672,"ground"),(3815,672,"ground"),
         (3958,672,"ground"),(4006,672,"ground"),(4054,672,"ground"),(4102,672,"ground")
      ]
      start = [
         (48,572,"start")
      ]

      end = [
         (4070,575,"end")
      ]

      blocks.extend(gold_blocks)

      blocks.extend(grounds)  

      return blocks

    def get_fires(self):
      # Create a list of fire
      fire_coords = [
         (752,624),(800,624),(848,624),(896,624),(1336,624),
         (1384,624),(1614,624),(1662,624),(1926,378),
         (2222,624),(2270,624),(3359,624)
      ]
      
      return fire_coords

    def get_fruits(self):
        # Create a list of fruits
        fruits = [
         (320,544,"Strawberry"),(408,472,"Strawberry"),(512,400,"Strawberry"),(776,370,"Strawberry"),
         (1088,496,"Strawberry"),(1454,456,"Strawberry"),(2581,429,"Strawberry"),(2990,496,"Strawberry"),
         (3470,544,"Strawberry"),(3775,640,"Strawberry")
        ]
    
        return fruits

