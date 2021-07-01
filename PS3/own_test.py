import unittest
import random
import ps3

def xyrange(x_upper_bound, y_upper_bound):
    """ Returns the cartesian product of range(x_upper_bound) and range(y_upper_bound).
        Useful for iterating over the tuple coordinates of a room
    """
    for x in range(x_upper_bound):
        for y in range(y_upper_bound):
            yield (x, y) # these are the room tile xy tuples 

class ps3_P1A(unittest.TestCase):
    def test_unimplemented_methods(self):
        """Test if student implemented methods in RectangularRoom abstract class that should not be implemented"""
        room = ps3.RectangularRoom(2,2,1)
        self.assertRaises(NotImplementedError, room.get_num_tiles)
        pos = ps3.Position(1,1)
        self.assertRaises(NotImplementedError, room.is_position_valid, pos)
        self.assertRaises(NotImplementedError, room.get_random_position)

    def test_room_dirt_dirty(self):
        """ 
        Can fail either because get_dirt_amount is working incorrectly 
        OR the student is initializing the dirt amount incorrectly
        """
        width, height, dirt_amount = (3, 4, 1)   
        room = ps3.RectangularRoom(width, height, dirt_amount)
        for x, y in xyrange(width, height):            
            self.assertEquals(room.get_dirt_amount(x, y),dirt_amount,
                            "Tile {} was not initialized with correct dirt amount".format((x, y))
                            )  

    def test_room_dirt_clean(self):
        """ 
        Can fail either because get_dirt_amount is working incorrectly 
        OR the student is initializing the dirt amount incorrectly
        """
        width, height, dirt_amount = (3, 4, 0)      
        room = ps3.RectangularRoom(width, height, dirt_amount)
        for x, y in xyrange(width, height):            
            self.assertEquals(room.get_dirt_amount(x, y),dirt_amount,
                             "Tile {} was not initialized with correct dirt amount".format((x, y))
                             )
    
    def test_is_tile_cleaned_dirty(self):
        """ Test is_tile_cleaned"""
        width, height, dirt_amount = (3, 4, 1)
        room = ps3.RectangularRoom(width, height, dirt_amount)
        # Check all squares are unclean at start, given initial dirt > 1
        for x, y in xyrange(width, height):
            self.assertFalse(room.is_tile_cleaned(x, y),
                             "Unclean tile {} was returned as clean".format((x, y))
                             )

    def test_is_tile_cleaned_clean(self):
        """ Test is_tile_cleaned"""
        width, height, dirt_amount = (3, 4, 0)
        room = ps3.RectangularRoom(width, height, dirt_amount)
        # Check all squares are unclean at start, given initial dirt > 1
        for x, y in xyrange(width, height):
            self.assertTrue(room.is_tile_cleaned(x, y),
                             "Unclean tile {} was returned as clean".format((x, y))
                             )

    def test_clean_tile_at_position_PosToZero(self):
        """ Test if clean_tile_at_position removes all dirt"""
        width, height, dirt_amount = (3, 4, 1)
        room = ps3.RectangularRoom(width, height, dirt_amount)
        # Clean the tiles and confirm they are marked as clean
        for x, y in xyrange(width, height):
            room.clean_tile_at_position(ps3.Position(x + random.random(), y + random.random()), dirt_amount) 
                # using random.random in case there is any issue with specific parts of a tile
        for x, y in xyrange(width, height):
            self.assertTrue(room.is_tile_cleaned(x, y),
                            "Clean tile {} was not marked clean".format((x, y))
                            )

    def test_clean_tile_at_position_PosToPos(self):
        """ Test if clean_tile_at_position removes all dirt"""
        width, height, dirt_amount = (3, 4, 2)
        room = ps3.RectangularRoom(width, height, dirt_amount)
        # Clean the tiles and confirm they are marked as clean
        for x, y in xyrange(width, height):
            room.clean_tile_at_position(ps3.Position(x + random.random(), y + random.random()), dirt_amount - 1) 
                # using random.random in case there is any issue with specific parts of a tile
        for x, y in xyrange(width, height):
            self.assertFalse(room.is_tile_cleaned(x, y),
                            "Unclean tile {} was marked clean".format((x, y))
                            )

    def test_clean_tile_at_position_ZeroToZero(self):
        """ Test if clean_tile_at_position removes all dirt"""
        width, height, dirt_amount = (3, 4, 0)
        room = ps3.RectangularRoom(width, height, dirt_amount)
        # Clean the tiles and confirm they are marked as clean
        for x, y in xyrange(width, height):
            room.clean_tile_at_position(ps3.Position(x + random.random(), y + random.random()), 1) 
                # using random.random in case there is any issue with specific parts of a tile
        for x, y in xyrange(width, height):
            self.assertTrue(room.is_tile_cleaned(x, y),
                            "Clean tile {} was marked clean, no negative dirt allowed".format((x, y))
                            )
    
    def test_get_num_cleaned_tiles_FullIn1(self):
        "Test get_num_cleaned_tiles for cleaning subset of room completely with 1 call"
        width, height, dirt_amount = (3, 4, 1)
        room = ps3.RectangularRoom(width, height, dirt_amount)
        cleaned_tiles = 0
        # Clean some tiles
        for x, y in xyrange(width-1, height-1):
            room.clean_tile_at_position(ps3.Position(x + random.random(), y + random.random()), 1)
            cleaned_tiles += 1
            num_cleaned = room.get_num_cleaned_tiles()
            self.assertEqual(num_cleaned, cleaned_tiles,
                            "Number of clean tiles is incorrect: expected {}, got {}".format(cleaned_tiles, num_cleaned)
                            )

    def test_get_num_cleaned_tiles_Partial(self):
        "Test get_num_cleaned_tiles for cleaning subset of room incompletely"
        width, height, dirt_amount = (3, 4, 2)
        room = ps3.RectangularRoom(width, height, dirt_amount)
        cleaned_tiles = 0
        # Clean some tiles
        for x, y in xyrange(width-1, height-1):
            room.clean_tile_at_position(ps3.Position(x + random.random(), y + random.random()), 1)
            num_cleaned = room.get_num_cleaned_tiles()
            self.assertEqual(num_cleaned, cleaned_tiles,
                            "Number of clean tiles is incorrect: expected {}, got {}".format(cleaned_tiles, num_cleaned)
                            )

    def test_get_num_cleaned_tiles_FullIn2(self):
        """Test get_num_cleaned_tiles for cleaning subset of room in two calls"""
        width, height, dirt_amount = (3, 4, 2)
        room = ps3.RectangularRoom(width, height, dirt_amount)
        cleaned_tiles = 0
        # Clean some tiles
        for x, y in xyrange(width-1, height-1):
            room.clean_tile_at_position(ps3.Position(x + random.random(), y + random.random()), 1)
            room.clean_tile_at_position(ps3.Position(x + random.random(), y + random.random()), 1)
            cleaned_tiles += 1
            num_cleaned = room.get_num_cleaned_tiles()
            self.assertEqual(num_cleaned, cleaned_tiles,
                             "Number of clean tiles is incorrect: expected {}, got {}".format(cleaned_tiles, num_cleaned)
                             )

    def test_get_num_cleaned_tiles_OverClean(self):
        "Test cleaning already clean tiles does not increment counter"
        width, height, dirt_amount = (3, 4, 2)
        room = ps3.RectangularRoom(width, height, dirt_amount)
        # clean all of the tiles in the room        
        for x, y in xyrange(width, height):
            room.clean_tile_at_position(ps3.Position(x + random.random(), y + random.random()), dirt_amount)
        for x, y in xyrange(width, height):
            room.clean_tile_at_position(ps3.Position(x + random.random(), y + random.random()), 1)
            num_cleaned = room.get_num_cleaned_tiles()
            self.assertEqual(num_cleaned, width * height,
                             "Number of clean tiles is incorrect: re-cleaning cleaned tiles must not increase number of cleaned tiles"
                             )

    def test_is_position_in_room(self):
        "Test is_position_in_room"
        width, height, dirt_amount = (3, 4, 2)
        room = ps3.RectangularRoom(width, height, dirt_amount)
        solution_room = ps3.RectangularRoom(width, height, dirt_amount)

        for x in [0.0, -0.1, width - 0.1, width, width + 0.1]:
            for y in [0.0, -0.1, height - 0.1, height, height + 0.1]:
                pos = ps3.Position(x, y)
                self.assertEquals(solution_room.is_position_in_room(pos),room.is_position_in_room(pos),
                                  "position {},{} is incorrect: expected {}, got {}".format(x, y, solution_room.is_position_in_room(pos), room.is_position_in_room(pos))
                                  )

class ps3_P1B(unittest.TestCase):
    """test the Robot abstract base class"""
    def test_unimplemented_methods(self):
        """Test if student implemented methods in Robot abstract class that should not be implemented"""
        room = ps3.EmptyRoom(2,2,1)
        robot = ps3.Robot(room,1,1)
        self.assertRaises(NotImplementedError, robot.update_position_and_clean)
    
    def test_getset_robot_direction(self):
        """Test get_robot_direction and set_robot_direction"""
        # instantiate EmptyRoom from solutions for testing
        width, height, dirt_amount = (3, 4, 2)
        solution_room = ps3.EmptyRoom(width, height, dirt_amount)

        robots = [ps3.Robot(solution_room, 1.0, 1) for i in range(4)]
        directions = [1, 333, 105, 75, 74.3]
        for dir_index, robot in enumerate(robots):
            robot.set_robot_direction(directions[dir_index])
        for dir_index, robot in enumerate(robots):
            robot_dir = robot.get_robot_direction()
            self.assertEquals(robot_dir, directions[dir_index],
                              "Robot direction set or retrieved incorrectly: expected {}, got {}".format(directions[dir_index], robot_dir)
                              )
        
class ps3_P2_ER(unittest.TestCase):
    """test the EmptyRoom subclass"""
    def test_get_random_position(self):
        """Test get_random_position
            checks for distribution of positions and validity of positions
        """
        width, height, dirt_amount = (5, 10, 1)
        room = ps3.EmptyRoom(width, height, dirt_amount)
        sol_room = ps3.EmptyRoom(width, height, dirt_amount)
        freq_buckets = {}
        for i in range(50000):
            pos = room.get_random_position()
            # confirm from test that this is a valid position
            self.assertTrue(sol_room.is_position_valid(pos)) 
            try:
                x, y = pos.get_x(), pos.get_y()
            except AttributeError:
                self.fail("get_random_position returned {} which is not a Position".format(pos))
            self.assertTrue(0 <= x < width and 0 <= y < height,
                            "get_random_position returned {} which is not in [0, {}), [0, {})".format(pos,width,height))
            x0, y0 = int(x), int(y)
            freq_buckets[(x0, y0)] = freq_buckets.get((x0, y0), 0) + 1
        for t in xyrange(width, height):
            num_in_bucket = freq_buckets.get(t, 0)
            self.assertTrue(
                # This is a 99.7% confidence interval for a uniform
                # distribution. Fail if the total of any bucket falls outside
                # this range.
                865 < num_in_bucket < 1135,
                "The distribution of positions from get_random_position "
                "looks incorrect (it should be uniform)")

    def test_get_num_tiles(self):
        """ test get_num_tiles method"""
        for i in range(10):        
            width, height, dirt_amount = (random.randint(1,10), random.randint(1,10), 1)
            room_num_tiles = ps3.EmptyRoom(width, height, dirt_amount).get_num_tiles()
            sol_room_tiles = ps3.EmptyRoom(width, height, dirt_amount).get_num_tiles()
            self.assertEquals(room_num_tiles, sol_room_tiles,
                             "student code number of room tiles = {}, not equal to solution code num tiles {}".format(room_num_tiles, sol_room_tiles)
                             )
    
    def test_is_position_valid(self):
        """ Test is_position_valid
            this should be refactored as it's mostly a copy of is_position_in_room code        
        """
        width, height, dirt_amount = (3, 4, 2)
        room = ps3.EmptyRoom(width, height, dirt_amount)
        solution_room = ps3.EmptyRoom(width, height, dirt_amount)

        for x in [0.0, -0.1, width - 0.1, width, width + 0.1]:
            for y in [0.0, -0.1, height - 0.1, height, height + 0.1]:
                pos = ps3.Position(x, y)
                self.assertEquals(solution_room.is_position_valid(pos), room.is_position_valid(pos),
                             "student code and solution code disagree on whether position is valid"
                                  )

class ps3_P2_FR(unittest.TestCase):                  
    """tests the FurnishedRoom subclass """
    def test_is_tile_furnished(self):
        """ test is_tile_furnished """        
        for trial in range(5):
            width, height, dirt_amount = (random.randint(2, 8), random.randint(2, 8), 1)
            # create room using student's class, set furniture tiles for solution class
            room = ps3.FurnishedRoom(width, height, dirt_amount)
            room.add_furniture_to_room()
            sol_room = ps3.FurnishedRoom(width, height, dirt_amount)
            # this relies on knowing the underlying details of the class
            sol_room.furniture_tiles = room.furniture_tiles 
            for x,y in xyrange(width,height):
                self.assertEquals(room.is_tile_furnished(x,y),sol_room.is_tile_furnished(x,y),
                                  "student code and solution code disagree on whether tile is furnished"
                                  )
    
    def test_is_position_furnished(self):
        """ test_is_position_furnished """        
        for trial in range(5):
            width, height, dirt_amount = (random.randint(2, 8), random.randint(2, 8), 1)
            # create room using student's class, set furniture tiles for solution class
            room = ps3.FurnishedRoom(width, height, dirt_amount)
            room.add_furniture_to_room()
            sol_room = ps3.FurnishedRoom(width, height, dirt_amount)
            # this relies on knowing the underlying details of the class
            sol_room.furniture_tiles = room.furniture_tiles 
            for x,y in xyrange(width,height):
                pos = ps3.Position(x + random.random(), y + random.random())
                self.assertEquals(room.is_position_furnished(pos),sol_room.is_position_furnished(pos),
                                  "student code and solution code disagree on whether position is furnished"
                                  )
    
    def test_is_position_valid(self):
        """ Test is_position_valid
        """
        for trial in range(5):
            width, height, dirt_amount = (3, 4, 2)
            room = ps3.FurnishedRoom(width, height, dirt_amount)
            room.add_furniture_to_room()
            sol_room = ps3.FurnishedRoom(width, height, dirt_amount)
            sol_room.furniture_tiles = room.furniture_tiles 
    
            for x in [0.0, -0.1, width - 0.1, width, width + 0.1, room.furniture_tiles[0][0] + 0.3]:
                for y in [0.0, -0.1, height - 0.1, height, height + 0.1, room.furniture_tiles[0][1] + 0.3]:
                    pos = ps3.Position(x, y)
                    self.assertEquals(sol_room.is_position_valid(pos), room.is_position_valid(pos),
                                      "student code and solution code disagree on whether position is valid"
                                      )
    
    def test_get_num_tiles(self):
        """ test get_num_tiles method
            should refactor - is mostly copy of EmptyRoom test        
        """
        for i in range(10):        
            width, height, dirt_amount = (random.randint(2,10), random.randint(2,10), 1)
            # instanciate student's room
            room = ps3.FurnishedRoom(width, height, dirt_amount)
            room.add_furniture_to_room()
            # instanciate solution's room based on student's furniture
            sol_room = ps3.FurnishedRoom(width, height, dirt_amount)
            sol_room.furniture_tiles = room.furniture_tiles 
            # generate answers
            room_num_tiles = room.get_num_tiles()
            sol_room_num_tiles = sol_room.get_num_tiles()
            self.assertEquals(room_num_tiles, sol_room_num_tiles,
                             "student code number of room tiles = {}, not equal to solution code num tiles {}".format(room_num_tiles, sol_room_num_tiles)
                             )
    
    def test_get_random_position(self):
        """Test get_random_position for FurnishedRoom
           tests for validity of positions - could add distribution checking similar to empty room
        """
        width, height, dirt_amount = (5, 10, 1)
        # instanciate student's room
        room = ps3.FurnishedRoom(width, height, dirt_amount)
        room.add_furniture_to_room()
        # instanciate solution's room based on student's furniture
        sol_room = ps3.FurnishedRoom(width, height, dirt_amount)
        sol_room.furniture_tiles = room.furniture_tiles 
        for i in range(50000):
            pos = room.get_random_position()
            self.assertTrue(sol_room.is_position_valid(pos)) 

if __name__ == "__main__":
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(ps3_P1A))
    suite.addTest(unittest.makeSuite(ps3_P1B))
    suite.addTest(unittest.makeSuite(ps3_P2_ER))
    suite.addTest(unittest.makeSuite(ps3_P2_FR))
    unittest.TextTestRunner(verbosity=3).run(suite)