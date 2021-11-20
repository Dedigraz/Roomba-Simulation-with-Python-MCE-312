# _*_ coding: utf-8 _*_
# Problem Set 6: Simulating robots
# Name:
# Collaborators:
# Time:
import math
import random
from typing import List
from matplotlib.pyplot import show

import numpy as np

import ps2_visualize
import pylab

# === Provided classes

class Position(object):
    """
    A Position represents a location in a two-dimensional room.
    """
    def __init__(self, x:float, y:float):
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
        self.Tiles =  np.asarray(list(zip(range(0,width+1), range(0, height+1))))
        self.cleanedTiles = np.array([])

    def getTileFromPos(self, pos):
        """
        Get the current tile that the robot is under from its position

        returns a tuple of int
        """
        return (pos.x//1,pos.y//1)
    
    def cleanTileAtPosition(self, pos):
        """
        Mark the tile under the position POS as cleaned.

        Assumes that POS represents a valid position inside this room.

        pos: a Position
        """
        np.append(self.cleanedTiles, self.getTileFromPos(pos))

    def isTileCleaned(self, m, n):
        """
        Return True if the tile (m, n) has been cleaned.

        Assumes that (m, n) represents a valid tile inside the room.

        m: an integer
        n: an integer
        returns: True if (m, n) is cleaned, False otherwise
        """
        if (m,n) in self.cleanedTiles:
            return True
        else:
            return False
 
    def getNumTiles(self):
        """
        Return the total number of tiles in the room.

        returns: an integer
        """
        return np.prod(self.Tiles.shape)

    def getNumCleanedTiles(self):
        """
        Return the total number of clean tiles in the room.

        returns: an integer
        """
        return np.prod(self.cleanedTiles.shape)

    def getRandomPosition(self):
        """
        Return a random position inside the room.

        returns: a Position object.
        """
        tempX = random.randint(0, self.width)
        tempY = random.randint(0, self.height)
        return Position(tempX,tempY)

    def isPositionInRoom(self, pos):
        """
        Return True if pos is inside the room.

        pos: a Position object.
        returns: True if pos is in the room, False otherwise.
        """
        #if (pos.x//1, pos.y//1) in self.Tiles:
        #    return False
        #else:
        #    return True
        if pos.x>= 0 and pos.y >= 0 and pos.x <= self.width and pos.y<=self.height:
            return True
        else:
            return False
    def getUncleanTile(self):
        unclean =  set(self.Tiles).difference(self.cleanedTiles)
        if unclean != {}:
            return unclean.pop()
        else:
            raise Exception



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
        self.room = RectangularRoom(room.width, room.height)
        self.speed = speed
        self.Position = self.room.getRandomPosition()
        self.direction = random.randrange(0, 361);

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
        return self.direction % 360

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
        self.direction = direction

    def updatePositionAndClean(self):
        """
        Simulate the raise passage of a single time-step.

        Move the robot to a new position and mark the tile it is on as having
        been cleaned.
        """
        self.setRobotPosition(self.Position.getNewPosition(self.direction, self.speed))
        self.room.cleanTileAtPosition(self.Position)


# === Problem 2
class StandardRobot(Robot):
    """
    A StandardRobot is a Robot with the standard movement strategy.

    At each time-step, a StandardRobot attempts to move in its current direction; when
    it hits a wall, it chooses a new direction randomly.
    """
    def __init__(self, room, speed):
        super().__init__(room, speed)
    #def updatePositionAndClean(self):
    #    """
    #    Simulate the passage of a single time-step.

    #    Move the robot to a new position and mark the tile it is on as having
    #    been cleaned.
    #    """
    #    Robot.updatePositionAndClean(self)

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
    anim = ps2_visualize.RobotVisualization(num_robots, width, height)
    room = RectangularRoom(width,height)
    robots = []


    for i in range(num_robots):
        robots.append(robot_type(room, speed))
    times =  []

    for i in range(num_trials):
        timesteps = 0
        while(len(room.cleanedTiles) != (len(room.Tiles) * min_coverage)):
            for r in robots : #we're going to loop thru each robot and update pos
                r.updatePositionAndClean()

            anim.update(room, robots)
            timesteps += 1

        times.append(timesteps)
        anim.done()

    return numpy.mean(times)

# === Problem 4
#
# 1) How long does it take to clean 80% of a 20×20 room with each of 1-10 robots?
#
# 2) How long does it take two robots to clean 80% of rooms with dimensions 
#	 20×20, 25×16, 40×10, 50×8, 80×5, and 100×4?

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

    data = [oneR, twoR,threeR, fourR, fiveR, sixR,sevR, eigR, nineR, tenR]
    
    pylab.plot(data)
    pylab.title("Cleaning times on Number of Robots")
    pylab.xlabel("average time")
    pylab.ylabel("Number of robots")
    pylab.show()

showPlot1()

def showPlot2():
    """
    Produces a plot showing dependence of cleaning time on room shape.
    """
    oneR = ["20X20",runSimulation(2,1,20,20,0.8,1,StandardRobot)]
    twoR = ["25X16",runSimulation(2,1,25,16,0.8,1,StandardRobot)]
    threeR = ["40X10",runSimulation(2,1,40,10,0.8,1,StandardRobot)]
    fourR = ["50X8", runSimulation(2,1,50,8,0.8,1,StandardRobot)]
    fiveR = ['80X5', runSimulation(2,1,80,5,0.8,1,StandardRobot)]
    sixR = ['100X4',runSimulation(2,1,100,4,0.8,1,StandardRobot)]

    data = [oneR, twoR,threeR, fourR, fiveR, sixR]
    
    pylab.plot(data)
    pylab.title("Cleaning times on Number of Robots")
    pylab.xlabel("average time")
    pylab.ylabel("Room Shape")
    pylab.show()

# === Problem 5

class RandomWalkRobot(Robot):
    """
    A RandomWalkRobot is a robot with the "random walk" movement strategy: it
    chooses a new direction at random after each time-step.
    """
    raise NotImplementedError


# === Problem 6

# For the parameters tested below (cleaning 80% of a 20x20 square room),
# RandomWalkRobots take approximately twice as long to clean the same room as
# StandardRobots do.
def showPlot3():
    """
    Produces a plot comparing the two robot strategies.
    """
    raise NotImplementedError
