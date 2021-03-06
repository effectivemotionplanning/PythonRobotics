"""
Obstacle navigation using A* on a toroidal grid
Author: Daniel Ingram (daniel-s-ingram)
        Tullio Facchinetti (tullio.facchinetti@unipv.it)
"""
from math import pi
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import from_levels_and_colors
import sys
import random

plt.ion()

# Simulation parameters
#M = 100
#obstacles = []
#randomTotal = int(random.random()*5)
#for x in range(randomTotal):
    #random1 = random.uniform(-2, 2)
    #random2 = random.uniform(-2, 2)
    #random3 = random.uniform(.4,.7)
    #obstacles.append([random1, random2, random3])


def press(event):
    """Exit from the simulation."""
    if event.key == 'q' or event.key == 'Q':
        print('Quitting upon request.')
        sys.exit(0)


filenamenumber = -1
#global routestatus
#routestatus = 0

def main(number,obs):
    # Arm geometry in the working space
    print("-------------------------------------------CSPACE NUMBER {:05d}".format(number)) #number is the cspace number
    link_length = [0.5, 1.5]
    initial_link_angle = [50, 0]
    arm = NLinkArm(link_length, initial_link_angle, plt)
    numlinks = len(link_length)
    #arm.plot_arm(plt, obs, number, [20, 150]) #need to change this so that its the angle variable

        ##what r the comments below saying??
        ##Whoever works next this is the code to plot the start one idrk
        #for i in range(self.n_links + 1):
            #if i is not self.n_links:
            #myplt.plot(self.points[i][0], self.points[i][1], 'k.')

    for x in range(10):
        plt.clf()
        grid = get_occupancy_grid(arm, obstacles)
        plt.imshow(grid)
        np.savetxt('Training/x/cspace/cspace{:04d}.dat'.format(number), grid, fmt='%1d')
        grid = np.loadtxt('Training/x/cspace/cspace{:04d}.dat'.format(number))
        np.savetxt('Training/x/cspace/cspace{:04d}.dat'.format(number), grid, fmt='%1d')
        plt.savefig('Training/images/cspace/cspace{:04d}.dat05d}.png'.format(number))
        plt.clf()
        global filenamenumber
        filenamenumber += 1
        print("FILE NAME NUMBER:{:05d}".format(filenamenumber))
        # (x, y) co-ordinates in the joint space [cell]
        startx = int(random.random()*99)
        starty = int(random.random()*99)
        goalx = int(random.random()*99)
        goaly = int(random.random()*99)
        start = (startx,starty)
        goal = (goalx, goaly)
        s = (100,100)
        #startgrid
        ##grid2 = []
        ##grid2.append([grid])
        ##np.savetxt('cspace.dat', grid2)
        route = astar_torus(grid, start, goal, filenamenumber)

        global routegrid
        routegrid = np.zeros(s)
        for i in range(1, len(route)):
            routegrid[route[i]] = 6
            plt.clf()
            plt.imshow(routegrid)
            np.savetxt('Training/y/route{:04d}.dat'.format(number), routegrid, fmt='%1d')
            plt.savefig('Training/images/route/route{:04d}.dat05d}.png'.format(filenamenumber))
            plt.clf()
        for obstacle in obs:
            circle = plt.Circle(
            (obstacle[0], obstacle[1]), radius=0.5 * obstacle[2], fc='k')
            print("plotted")
            plt.gca().add_patch(circle)
        limit = sum(link_length)
        plt.xlim([-limit, limit])
        plt.ylim([-limit, limit])
        plt.draw()
        data = np.fromstring(plt.canvas.tostring_rgb(), dtype=np.uint8, sep='')
        data = data.reshape(plt.canvas.get_width_height()[::-1] + (3,))
        np.savetxt('Training/x/workspace/workspace{:04d}.dat'.format(number), data, fmt='%1d')
        plt.savefig('Training/images/workspace/workspace{:05d}.png'.format(filenamenumber))
        plt.show()
        plt.clf()
        plt.pause(1e-5)
        #first/start arm conifg
        for i, node in enumerate(route):
            if i == 0:
                plt.cla()
                grid[node] = 6
                theta1 = 2 * pi * node[0] / M - pi
                theta2 = 2 * pi * node[1] / M - pi
                arm.plot_arm2(plt, obstacles, number, [theta1, theta2])
            if i == len(route) - 1:
                plt.cla()
                grid[node] = 6
                theta1 = 2 * pi * node[0] / M - pi
                theta2 = 2 * pi * node[1] / M - pi
                arm.plot_arm(plt, obstacles, number, [theta1, theta2])
            #if len(route) >= 0:
            #animate(grid, arm, route, number)
            #previous 2 lines commented out to fix goalgrid and startgrid


def animate(grid, arm, route, number):
    fig, axs = plt.subplots(1, 2)
    fig.canvas.mpl_connect('key_press_event', press)
    colors = ['white', 'black', 'red', 'pink', 'yellow', 'green', 'orange']
    levels = [0, 1, 2, 3, 4, 5, 6, 7]
    cmap, norm = from_levels_and_colors(levels, colors)
    for i, node in enumerate(route):
        plt.subplot(1, 2, 1)
        grid[node] = 6
        plt.cla()
        plt.imshow(grid, cmap=cmap, norm=norm, interpolation=None)
        theta1 = 2 * pi * node[0] / M - pi
        theta2 = 2 * pi * node[1] / M - pi
        ##arm.update_joints([theta1, theta2])
        plt.subplot(1, 2, 2)
        arm.plot_arm(plt, obstacles, number, [theta1, theta2])
        plt.xlim(-2.0, 2.0)
        plt.ylim(-3.0, 3.0)
        plt.show()
        # Uncomment here to save the sequence of frames
        # plt.savefig('frame{:04d}.png'.format(i))
        plt.pause(0.1)


def animate2(obst):
    fig, axs = plt.subplots(1, 2)
    fig.canvas.mpl_connect('key_press_event', press)
    colors = ['white', 'black', 'red', 'pink', 'yellow', 'green', 'orange']
    levels = [0, 1, 2, 3, 4, 5, 6, 7]
    cmap, norm = from_levels_and_colors(levels, colors)
    plt.cla()
    plt.subplot(1, 2, 2)
    arm.plot_arm(plt, obstacles=obst)
    plt.xlim(-2.0, 2.0)
    plt.ylim(-3.0, 3.0)
    plt.show()
        # Uncomment here to save the sequence of frames
        # plt.savefig('frame{:04d}.png'.format(i))


def detect_collision(line_seg, circle):
    """
    Determines whether a line segment (arm link) is in contact
    with a circle (obstacle).
    Credit to: http://doswa.com/2009/07/13/circle-segment-intersectioncollision.html
    Args:
        line_seg: List of coordinates of line segment endpoints e.g. [[1, 1], [2, 2]]
        circle: List of circle coordinates and radius e.g. [0, 0, 0.5] is a circle centered
                at the origin with radius 0.5
    Returns:
        True if the line segment is in contact with the circle
        False otherwise
    """
    a_vec = np.array([line_seg[0][0], line_seg[0][1]])
    b_vec = np.array([line_seg[1][0], line_seg[1][1]])
    c_vec = np.array([circle[0], circle[1]])
    radius = circle[2]
    line_vec = b_vec - a_vec
    line_mag = np.linalg.norm(line_vec)
    circle_vec = c_vec - a_vec
    proj = circle_vec.dot(line_vec / line_mag)
    if proj <= 0:
        closest_point = a_vec
    elif proj >= line_mag:
        closest_point = b_vec
    else:
        closest_point = a_vec + line_vec * proj / line_mag
    if np.linalg.norm(closest_point - c_vec) > radius:
        return False
    return True


def get_occupancy_grid(arm, obstacles):
    """
    Discretizes joint space into M values from -pi to +pi
    and determines whether a given coordinate in joint space
    would result in a collision between a robot arm and obstacles
    in its environment.
    Args:
        arm: An instance of NLinkArm
        obstacles: A list of obstacles, with each obstacle defined as a list
                   of xy coordinates and a radius.
    Returns:
        Occupancy grid in joint space
    """
    grid = [[0 for _ in range(M)] for _ in range(M)]
    theta_list = [2 * i * pi / M for i in range(-M // 2, M // 2 + 1)]
    for i in range(M):
        for j in range(M):
            arm.update_joints([theta_list[i], theta_list[j]])
            points = arm.points
            collision_detected = False
            for k in range(len(points) - 1):
                for obstacle in obstacles:
                    line_seg = [points[k], points[k + 1]]
                    collision_detected = detect_collision(line_seg, obstacle)
                    if collision_detected:
                        break
                if collision_detected:
                    break
            grid[i][j] = int(collision_detected)
    return np.array(grid)

def astar_torus(grid, start_node, goal_node, number):
    """
    Finds a path between an initial and goal joint configuration using
    the A* Algorithm on a tororiadal grid.
    Args:
        grid: An occupancy grid (ndarray)
        start_node: Initial joint configuation (tuple)
        goal_node: Goal joint configuration (tuple)
    Returns:
        Obstacle-free route in joint space from start_node to goal_node
    """
    colors = ['white', 'black', 'red', 'pink', 'yellow', 'green', 'orange']
    levels = [0, 1, 2, 3, 4, 5, 6, 7]
    cmap, norm = from_levels_and_colors(levels, colors)

    grid[start_node] = 4
    grid[goal_node] = 5

    parent_map = [[() for _ in range(M)] for _ in range(M)]

    heuristic_map = calc_heuristic_map(M, goal_node)

    explored_heuristic_map = np.full((M, M), np.inf)
    distance_map = np.full((M, M), np.inf)
    explored_heuristic_map[start_node] = heuristic_map[start_node]
    distance_map[start_node] = 0
    while True:
        grid[start_node] = 4
        grid[goal_node] = 5

        current_node = np.unravel_index(
            np.argmin(explored_heuristic_map, axis=None), explored_heuristic_map.shape)
        min_distance = np.min(explored_heuristic_map)
        if (current_node == goal_node) or np.isinf(min_distance):
            break

        grid[current_node] = 2
        explored_heuristic_map[current_node] = np.inf

        i, j = current_node[0], current_node[1]

        neighbors = find_neighbors(i, j)

        for neighbor in neighbors:
            if grid[neighbor] == 0 or grid[neighbor] == 5:
                distance_map[neighbor] = distance_map[current_node] + 1
                explored_heuristic_map[neighbor] = heuristic_map[neighbor]
                parent_map[neighbor[0]][neighbor[1]] = current_node
                grid[neighbor] = 3

    if np.isinf(explored_heuristic_map[goal_node]):
        route = []
        #routestatus = 1
        print("No route found.")
        #s=(100,100)
        #blank = np.zeros(s)
        #plt.imshow(blank)
        plt.plot()
        plt.savefig('Training/images/route/route{:05d}'.format(number))
        plt.cla()
        grid[start_node] = 6
        theta1 = 2 * pi * start_node[0] / M - pi
        theta2 = 2 * pi * start_node[1] / M - pi
        arm.plot_arm2(plt, obstacles, number, [theta1, theta2])
        plt.cla()
        grid[goal_node] = 6
        theta1 = 2 * pi * goal_node[0] / M - pi
        theta2 = 2 * pi * goal_node[1] / M - pi
        arm.plot_arm(plt, obstacles, number, [theta1, theta2])

    else:
        route = [goal_node]
        while parent_map[route[0][0]][route[0][1]] != ():
            route.insert(0, parent_map[route[0][0]][route[0][1]])

        print("The route found covers %d grid cells." % len(route))


    return route


def find_neighbors(i, j):
    neighbors = []
    if i - 1 >= 0:
        neighbors.append((i - 1, j))
    else:
        neighbors.append((M - 1, j))

    if i + 1 < M:
        neighbors.append((i + 1, j))
    else:
        neighbors.append((0, j))

    if j - 1 >= 0:
        neighbors.append((i, j - 1))
    else:
        neighbors.append((i, M - 1))

    if j + 1 < M:
        neighbors.append((i, j + 1))
    else:
        neighbors.append((i, 0))

    return neighbors


def calc_heuristic_map(M, goal_node):
    X, Y = np.meshgrid([i for i in range(M)], [i for i in range(M)])
    heuristic_map = np.abs(X - goal_node[1]) + np.abs(Y - goal_node[0])
    for i in range(heuristic_map.shape[0]):
        for j in range(heuristic_map.shape[1]):
            heuristic_map[i, j] = min(heuristic_map[i, j],
                                      i + 1 + heuristic_map[M - 1, j],
                                      M - i + heuristic_map[0, j],
                                      j + 1 + heuristic_map[i, M - 1],
                                      M - j + heuristic_map[i, 0]
                                      )
    return heuristic_map


class NLinkArm(object):
    """
    Class for controlling and plotting a planar arm with an arbitrary number of links.
    """

    def __init__(self, link_lengths, joint_angles, plt):
        self.n_links = len(link_lengths)
        if self.n_links != len(joint_angles):
            raise ValueError()

        self.link_lengths = np.array(link_lengths)
        self.joint_angles = np.array(joint_angles)
        self.points = [[0, 0] for _ in range(self.n_links + 1)]

        self.lim = sum(link_lengths)
        self.update_points()

    def update_joints(self, joint_angles):
        self.joint_angles = joint_angles
        self.update_points()

    def update_points(self):
        for i in range(1, self.n_links + 1):
            self.points[i][0] = self.points[i - 1][0] + \
                self.link_lengths[i - 1] * \
                np.cos(np.sum(self.joint_angles[:i]))
            self.points[i][1] = self.points[i - 1][1] + \
                self.link_lengths[i - 1] * \
                np.sin(np.sum(self.joint_angles[:i]))
        self.end_effector = np.array(self.points[self.n_links]).T

    def plot_arm(self, myplt, obstacles, number, joint_angles):  # pragma: no cover
        self.update_joints(joint_angles)
        #for i in range(self.n_links + 1):
        i = self.n_links
            #if i is not self.n_links:
                #myplt.plot([self.points[i][0], self.points[i + 1][0]],
                        #  [self.points[i][1], self.points[i + 1][1]], 'r-')
        myplt.plot(self.points[i][0], self.points[i][1], 'k.')
        myplt.xlim([-self.lim, self.lim])
        myplt.ylim([-self.lim, self.lim])
        myplt.draw()
        myplt.savefig('images/goal/goal{:05d}'.format(filenamenumber))
        data = np.fromstring(myplt.canvas.tostring_rgb(), dtype=np.uint8, sep='')
        data = data.reshape(myplt.canvas.get_width_height()[::-1] + (3,))
        np.savetxt('Training/x/goal/goal{:04d}.dat'.format(number), data, fmt='%1d')
        myplt.show()
        myplt.clf()
        myplt.xlim([-self.lim, self.lim])
        myplt.ylim([-self.lim, self.lim])
        myplt.draw()

        # myplt.pause(1e-5)
    def plot_arm2(self, myplt, obstacles, number, joint_angles):  # pragma: no cover
        self.update_joints(joint_angles)
        #for i in range(self.n_links + 1):
        i = self.n_links
            #if i is not self.n_links:
                #myplt.plot([self.points[i][0], self.points[i + 1][0]],
                        #  [self.points[i][1], self.points[i + 1][1]], 'r-')
        myplt.plot(self.points[i][0], self.points[i][1], 'k.')
        myplt.xlim([-self.lim, self.lim])
        myplt.ylim([-self.lim, self.lim])
        myplt.draw()
        data = np.fromstring(myplt.canvas.tostring_rgb(), dtype=np.uint8, sep='')
        data = data.reshape(myplt.canvas.get_width_height()[::-1] + (3,))
        np.savetxt('Training/x/start/start{:04d}.dat'.format(number), data, fmt='%1d')
        myplt.savefig('images/start/start{:05d}'.format(filenamenumber))
        myplt.show()
        myplt.clf()
        myplt.xlim([-self.lim, self.lim])
        myplt.ylim([-self.lim, self.lim])
        myplt.draw()

        # myplt.pause(1e-5)



np.set_printoptions(threshold=sys.maxsize)
for z in range(2):
    # Simulation parameters
    M = 100
    obstacles = []
    randomTotal = int(random.random()*2 +1)
    #for x in range(randomTotal):, testing something must indent back pater
    random1 = random.uniform(-2, 2)
    random2 =random.uniform(-2, 2)
    random3 = random.uniform(.4,.7)
    obstacles.append([random1, random2,random3])
    random1 = random.uniform(-2, 2)
    random2 =random.uniform(-2, 2)
    random3 = random.uniform(.4,.7)
    obstacles.append([random1, random2,random3])
    link_length = [0.5, 1.5]
    initial_link_angle = [0, 0]
    arm = NLinkArm(link_length, initial_link_angle, plt)
    grid = get_occupancy_grid(arm, obstacles)
    #f=open("cspace.dat", "a+")
    s = np.array_str(grid)
    if __name__ == '__main__':
        main(z,obstacles)
    #f.write("test \n")
    #if routestatus == 0:
    #    plt.show()
##np.savetxt('cspace.dat', grid2)
