# Problem Set 6: Simulating robots
# Name:
# Collaborators:
# Time:

import math
import random

import ps2_visualize
import pylab

import numpy as np
# === Provided classes

class Position(object):
    """
    A Position represents a location in a two-dimensional room.
    """
    def __init__(self, x, y):
        """
        Initializes a position with coordinates (x, y).
        """
        self.x = x
        self.y = y
    def getX(self):
        return self.x
    def getY(self):
        return self.y
    def getNewPosition(self, angle, speed):
        """
        Computes and returns the new Position after a single clock-tick has
        passed, with this object as the current position, and with the
        specified angle and speed.

        Does NOT test whether the returned position fits inside the room.

        angle: float representing angle in degrees, 0 <= angle < 360
        speed: positive float representing speed

        Returns: a Position object representing the new position.
        """
        old_x, old_y = self.getX(), self.getY()
        # Compute the change in position
        delta_y = speed * math.cos(math.radians(angle))
        delta_x = speed * math.sin(math.radians(angle))
        # Add that to the existing position
        new_x = old_x + delta_x
        new_y = old_y + delta_y
        return Position(new_x, new_y)


class Tile(object):
    """A tile object represents a tile(the smallest area that the robot can move to inside the room).
    A tile object has a positional argument, which can be used to get the tile at that Position in 
    the room
    """
    def __init__(self, X,Y):
        self.X = X
        self.Y = Y
        self.IsCleaned = False


def TileFromPos(pos):
    """Returns a tile when giving a Positon as an argument"""
    return Tile(math.floor(pos.x), math.floor(pos.y))

def generateTiles(upperWidth, upperHeight, lowerWidth =0, lowerHeight =0 ):
    """Generates a list of Tiles that should be used in the rectangular room object,
    and store information about whether thy have been cleaned or not"""
    Tiles = []
    for w in range(lowerWidth, upperWidth):
        for h in range(lowerHeight, upperHeight):
            Tiles.append( Tile(w,h) )
    return Tiles


# === Problems 1

class RectangularRoom(object):
    """
    A RectangularRoom represents a rectangular region containing clean or dirty
    tiles.

    A room has a width and a height and contains (width * height) tiles. At any
    particular time, each of these tiles is either clean or dirty.
    """
    def __init__(self, width, height):
        """
        Initializes a rectangular room with the specified width and height.

        Initially, no tiles in the room have been cleaned.

        width: an integer > 0
        height: an integer > 0
        """
        self.width = width
        self.height = height
        self.Tiles = generateTiles(upperWidth=self.width, upperHeight=self.height)
    
    def cleanTileAtPosition(self, pos):
        """
        Mark the tile under the position POS as cleaned.

        Assumes that POS represents a valid position inside this room.

        pos: a Position
        """
        tile = TileFromPos(pos)
        for t in self.Tiles:
            if t.X == tile.X and t.Y == tile.Y:
                t.IsCleaned = True

    def isTileCleaned(self, m, n):
        """
        Return True if the tile (m, n) has been cleaned.

        Assumes that (m, n) represents a valid tile inside the room.

        m: an integer
        n: an integer
        returns: True if (m, n) is cleaned, False otherwise
        """
        for t in self.Tiles:
            if t.X == m and t.Y == n:
                if t.IsCleaned == True:
                    return True
                else:
                    return False

    def getNumTiles(self):
        """
        Return the total number of tiles in the room.

        returns: an integer
        """
        len(self.Tiles)

    def getNumCleanedTiles(self):
        """
        Return the total number of clean tiles in the room.

        returns: an integer
        """
        count = 0
        for t in self.Tiles:
            if t.IsCleaned == True:
                count += 1
        return count

    def getRandomPosition(self):
        """
        Return a random position inside the room.

        returns: a Position object.
        """
        return Position(random.randint(0,self.width) + 0.5, random.randint(0,self.height) + 0.5)

    def isPositionInRoom(self, pos):
        """
        Return True if pos is inside the room.

        pos: a Position object.
        returns: True if pos is in the room, False otherwise.
        """
        t = TileFromPos(pos)
        count = 0
        for tile in self.Tiles:
            if t.X == tile.X and t.Y == tile.Y:
                count += 1
        if count == 1:
            return True
        elif count > 1:
            self.Tiles = list(set(self.Tiles))
            return True
        else:
            return False
    
    def getUncleanTiles(self):
        """Returns a list of unclean Tiles when called"""
        uncleanTiles = []
        for tile in self.Tiles:
            if tile.IsCleaned == False:
                uncleanTiles.append(tile)
        return uncleanTiles


class Robot(object):
    """
    Represents a robot cleaning a particular room.

    At all times the robot has a particular position and direction in the room.
    The robot also has a fixed speed.

    Subclasses of Robot should provide movement strategies by implementing
    updatePositionAndClean(), which simulates a single time-step.
    """
    def __init__(self, room, speed):
        """
        Initializes a Robot with the given speed in the specified room. The
        robot initially has a random direction and a random position in the
        room. The robot cleans the tile it is on.

        room:  a RectangularRoom object.
        speed: a float (speed > 0)
        """
        self.room :RectangularRoom = room

        self.speed = speed
        self.Position = self.room.getRandomPosition()
        self.Direction = random.randrange(0,361,45)
        self.room.cleanTileAtPosition(self.Position)

    def getRobotPosition(self):
        """
        Return the position of the robot.

        returns: a Position object giving the robot's position.
        """
        return self.Position
    
    def getRobotDirection(self):
        """
        Return the direction of the robot.

        returns: an integer d giving the direction of the robot as an angle in
        degrees, 0 <= d < 360.
        """
        return self.Direction

    def setRobotPosition(self, position):
        """
        Set the position of the robot to POSITION.

        position: a Position object.
        """
        self.Position = position

    def setRobotDirection(self, direction):
        """
        Set the direction of the robot to DIRECTION.

        direction: integer representing an angle in degrees
        """
        self.Direction = direction

    def updatePositionAndClean(self):
        """
        Simulate the raise passage of a single time-step.

        Move the robot to a new position and mark the tile it is on as having
        been cleaned.
        """
        self.setRobotPosition(self.Position.getNewPosition)
        self.room.cleanTileAtPosition(self.Position)

# === Helper Methods
    def getDirectionToTile(self, pos, tile):
        """Get's the direction to a tile given a Position.
        pos : Position object
        tile : The Tile you want to move to
        
        Returns: the direction as an int
        """
        refTile = TileFromPos(pos)
        if(refTile.X > tile.X and refTile.Y < tile.Y):
            return 315
        elif refTile.X == tile.X and refTile.Y < tile.Y:
            return 0
        elif refTile.X < tile.X and refTile.Y < tile.Y:
            return 45
        elif refTile.X > tile.X and refTile.Y == tile.Y:
            return 270
        elif refTile.X < tile.X and refTile.Y== tile.Y:
            return 90
        elif refTile.X > tile.X and refTile.Y > tile.Y:
            return 225
        elif refTile.X== tile.X  and refTile.Y > tile.Y:
            return 180
        elif refTile.X < tile.X and refTile.Y > tile.Y:
            return 135
        
    def canMoveToFutureTile(self, direction):
        """
        Checks if the robot continuing on his present trajectory,
        would lead it to be out of  the room boundary.

        Parameters: Takes a Position as an argument

        Returns: bool
        """
        pos = self.getRobotPosition()

        futurePos = pos.getNewPosition(direction, self.speed)
            
        isInRoom = self.room.isPositionInRoom(futurePos)
        tile = TileFromPos(futurePos)
        if tile.IsCleaned == True and isInRoom:
            return True
        else:
            return False

# === Problem 2
class StandardRobot(Robot):
    """
    A StandardRobot is a Robot with the standard movement strategy.

    At each time-step, a StandardRobot attempts to move in its current direction; when
    it hits a wall, it chooses a new direction randomly.
    """
    # ==== Helper Methods

    def surroundingTiles(self, refTile):
        """Get's a list of the tiles that are surround a reference tile that have not been cleaned

        Args:
            refTile (Tile): reference tile in question

        Returns:
            list[Tile]: list of viable tiles around the reference tile
        """
        xRange = range(refTile.X - 1, refTile.X + 2)
        yRange = range(refTile.Y -1, refTile.Y +2)
        uncleanTiles = self.room.getUncleanTiles()
        surroundingTiles = []
        for t in uncleanTiles:
            if t.X in xRange and t.Y in yRange:
                surroundingTiles.append(t)
        return surroundingTiles

    def obviousPath(self):
        """This method lifts the heavy load in the Standard Robot class, it determines when to 
        change the robots direction and by what amount. It takes into account it's surroundings and
        places the robot adequately
        """
        i = 0
        reftile =  TileFromPos(self.Position)
        surroundings = self.surroundingTiles(reftile)
        directions = []
        while i < len(surroundings):
            if self.room.isPositionInRoom(Position(surroundings[i].X, surroundings[i].Y)):
                directionToTile = self.getDirectionToTile(self.Position,surroundings[i])
                if directionToTile == None:
                    directions.append(721)
                else:
                    directions.append(directionToTile)
            else:
                directions.append(721)
            i += 1
        
        relativeDir = []
        for x in directions:
            relativeDir.append(abs(self.Direction - x))
        mini  =  relativeDir.index(min(relativeDir))
        self.setRobotDirection(self.getDirectionToTile(self.Position, surroundings[mini]))
        
    def updatePositionAndClean(self):
        """
        Simulate the passage of a single time-step.

        Move the robot to a new position and mark the tile it is on as having
        been cleaned.
        """
        tile = TileFromPos(self.Position)
        surroundingTiles =  self.surroundingTiles(tile)
        uncleanTiles = self.room.getUncleanTiles()
        
        if surroundingTiles == []:
            self.setRobotPosition(Position(uncleanTiles[0].X, uncleanTiles[0].Y))
            self.room.cleanTileAtPosition(self.Position)
        elif surroundingTiles != []:
            self.obviousPath()
            self.setRobotPosition(self.Position.getNewPosition(self.Direction, self.speed))
            self.room.cleanTileAtPosition(self.Position)

# === Problem 3

def runSimulation(num_robots, speed, width, height, min_coverage, num_trials,
                  robot_type):
    """
    Runs NUM_TRIALS trials of the simulation and returns the mean number of
    time-steps needed to clean the fraction MIN_COVERAGE of the room.

    The simulation is run with NUM_ROBOTS robots of type ROBOT_TYPE, each with
    speed SPEED, in a room of dimensions WIDTH x HEIGHT.

    num_robots: an int (num_robots > 0)
    speed: a float (speed > 0)
    width: an int (width > 0)
    height: an int (height > 0)
    min_coverage: a float (0 <= min_coverage <= 1.0)
    num_trials: an int (num_trials > 0)
    robot_type: class of robot to be instantiated (e.g. Robot or
                RandomWalkRobot)
    """
    # anim = ps2_visualize.RobotVisualization(num_robots, width, height)
    room = RectangularRoom(width,height)
    robots = []


    for i in range(num_robots):
        robots.append(robot_type(room, speed))
    times =  []

    i = 0
    while i < num_trials:
        timesteps = 0

        while(room.getNumCleanedTiles() <= (width * height *  min_coverage)):
            for r in robots : #we're going to loop thru each robot and update pos
                r.updatePositionAndClean()

            # anim.update(room, robots)
            timesteps += 1

        times.append(timesteps)
        # anim.done()
        i += 1

    return sum(times)/len(times)


# === Problem 4
#
# 1) How long does it take to clean 80% of a 20�20 room with each of 1-10 robots?
#
# 2) How long does it take two robots to clean 80% of rooms with dimensions 
#	 20�20, 25�16, 40�10, 50�8, 80�5, and 100�4?

def showPlot1():
    """
    Produces a plot showing dependence of cleaning time on number of robots.
    """ 
    oneR = [1,runSimulation(1,1,20,20,0.8,1,StandardRobot)]
    twoR = [2,runSimulation(2,1,20,20,0.8,1,StandardRobot)]
    threeR = [3,runSimulation(3,1,20,20,0.8,1,StandardRobot)]
    fourR = [4, runSimulation(4,1,20,20,0.8,1,StandardRobot)]
    fiveR = [5, runSimulation(5,1,20,20,0.8,1,StandardRobot)]
    sixR = [6,runSimulation(6,1,20,20,0.8,1,StandardRobot)]
    sevR = [7,runSimulation(7,1,20,20,0.8,1,StandardRobot)]
    eigR = [8,runSimulation(8,1,20,20,0.8,1,StandardRobot)]
    nineR = [9,runSimulation(9,1,20,20,0.8,1,StandardRobot)]
    tenR =[10, runSimulation(10,1,20,20,0.8,1,StandardRobot)]

    xdata = [oneR[0], twoR[0],threeR[0], fourR[0], fiveR[0], sixR[0],sevR[0], eigR[0], nineR[0], tenR[0]]
    ydata = [oneR[1], twoR[1],threeR[1], fourR[1], fiveR[1], sixR[1],sevR[1], eigR[1], nineR[1], tenR[1]]
    
    pylab.plot(xdata,ydata)
    pylab.title("Cleaning Times on Number of Robots")
    pylab.ylabel("Average Time")
    pylab.xlabel("Number of robots")
    pylab.show()

#showPlot1()

def showPlot2():
    """
    Produces a plot showing dependence of cleaning time on room shape.
    """
    oneR = [20 * 20,runSimulation(2,1,20,20,0.8,1,StandardRobot)]
    twoR =   [25 * 16,runSimulation(2,1,25,16,0.8,1,StandardRobot)]
    threeR = [40 * 10,runSimulation(2,1,40,10,0.8,1,StandardRobot)]
    fourR =  [50 * 8, runSimulation(2,1,50,8,0.8,1,StandardRobot)]
    fiveR =  [80 * 5, runSimulation(2,1,80,5,0.8,1,StandardRobot)]
    sixR =   [100 * 4,runSimulation(2,1,100,4,0.8,1,StandardRobot)]

    ydata = [oneR[0], twoR[0],threeR[0], fourR[0], fiveR[0], sixR[0]]
    xdata = [oneR[1], twoR[1],threeR[1], fourR[1], fiveR[1], sixR[1]]
    
    pylab.plot(xdata, ydata)
    pylab.title("Time to Clean 80% of square rooms with different sizes, with 2 Robots ")
    pylab.xlabel("Average time")
    pylab.ylabel("Number of Tiles")
    pylab.show()

#showPlot2()
# === Problem 5

class RandomWalkRobot(Robot):
    """
    A RandomWalkRobot is a robot with the "random walk" movement strategy: it
    chooses a new direction at random after each time-step.
    """
    def surroundingTiles(self, refTile):
        """Get's a list of the tiles that are surround a reference tile

        Args:
            refTile (Tile): reference tile in question

        Returns:
            list[Tile]: list of tiles around the reference tile
        """
        xRange = range(refTile.X - 1, refTile.X + 2)
        yRange = range(refTile.Y -1, refTile.Y +2)
        surroundingTiles = []
        for t in self.room.Tiles:
            if t.X in xRange and t.Y in yRange:
                surroundingTiles.append(t)
        return surroundingTiles
    
    def obscurePath(self):
        """This method lifts the heavy load in the Random Robot class, it determines when to 
        change the robots direction and by what amount. It randomly selects a position from 
        the surrounding tiles and set's it as the robot's direction.
        """
        i = 0
        reftile =  TileFromPos(self.Position)
        surroundings = self.surroundingTiles(reftile)
        directions = []
        while i < len(surroundings):
            if self.room.isPositionInRoom(Position(surroundings[i].X, surroundings[i].Y)):
                directionToTile = self.getDirectionToTile(self.Position,surroundings[i])
                if directionToTile != None:
                    directions.append(directionToTile)
            i += 1

        self.setRobotDirection(random.choice(directions))

    def updatePositionAndClean(self):
        tile = TileFromPos(self.Position)
        surroundingTiles =  self.surroundingTiles(tile)
        uncleanTiles = self.room.getUncleanTiles()
        
        if surroundingTiles == []:
            self.setRobotPosition(Position(uncleanTiles[0].X, uncleanTiles[0].Y))
            self.room.cleanTileAtPosition(self.Position)
        elif surroundingTiles != []:
            self.obscurePath()
            self.setRobotPosition(self.Position.getNewPosition(self.Direction, self.speed))
            self.room.cleanTileAtPosition(self.Position)


# === Problem 6

# For the parameters tested below (cleaning 80% of a 20x20 square room),
# RandomWalkRobots take approximately twice as long to clean the same room as
# StandardRobots do.
def showPlot3():
    """
    Produces a plot comparing the two robot strategies.
    """
    standardR = [[20 *20,runSimulation(1,1,20,20,0.8,3,StandardRobot)],
                 [25 * 16,runSimulation(2,1,25,16,0.8,1,StandardRobot)],
                 [40 * 10,runSimulation(2,1,40,10,0.8,1,StandardRobot)],
                 [50 * 8, runSimulation(2,1,50,8,0.8,1,StandardRobot)],
                 [80 * 5, runSimulation(2,1,80,5,0.8,1,StandardRobot)],
                 [100 * 4,runSimulation(2,1,100,4,0.8,1,StandardRobot)]]
    
    RandomR = [[20 * 20,runSimulation(1,1,20,20,0.8,3,RandomWalkRobot),
               [25 * 16,runSimulation(2,1,25,16,0.8,1,StandardRobot)],
                [40 * 10,runSimulation(2,1,40,10,0.8,1,StandardRobot)],
                [50 * 8, runSimulation(2,1,50,8,0.8,1,StandardRobot)],
                [80 * 5, runSimulation(2,1,80,5,0.8,1,StandardRobot)],
                [100 * 4,runSimulation(2,1,100,4,0.8,1,StandardRobot)]]]
    
    foreach r in 
    
    pylab.plot(SRdata,'r', label='Standard robot')
    pylab.plot(RRdata,'b', label='Random robot')
    pylab.title("Time to Clean 80% of a room with different Robot mechanics")
    pylab.ylabel("Average time")
    pylab.legend()
    pylab.show()
showPlot3()