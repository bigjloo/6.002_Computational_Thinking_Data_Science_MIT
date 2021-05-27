###########################
# 6.0002 Problem Set 1a: Space Cows 
# Name: Junzhong Loo
# Collaborators: --
# Time: --

from os import name
from ps1_partition import get_partitions
import time
import math

#================================
# Part A: Transporting Space Cows
#================================

# Problem 1
def load_cows(filename):
    """
    Read the contents of the given file.  Assumes the file contents contain
    data in the form of comma-separated cow name, weight pairs, and return a
    dictionary containing cow names as keys and corresponding weights as values.

    Parameters:
    filename - the name of the data file as a string

    Returns:
    a dictionary of cow name (string), weight (int) pairs
    """
    with open(filename) as file:
        content = file.read().splitlines()
    cows = {}
    for line in content:
        splited = line.split(',')
        cows[splited[0]] = int(splited[1])
    return cows

# Problem 2
def greedy_cow_transport(cows,limit=10):
    """
    Uses a greedy heuristic to determine an allocation of cows that attempts to
    minimize the number of spaceship trips needed to transport all the cows. The
    returned allocation of cows may or may not be optimal.
    The greedy heuristic should follow the following method:

    1. As long as the current trip can fit another cow, add the largest cow that will fit
        to the trip
    2. Once the trip is full, begin a new trip to transport the remaining cows

    Does not mutate the given dictionary of cows.

    Parameters:
    cows - a dictionary of name (string), weight (int) pairs
    limit - weight limit of the spaceship (an int)
    
    Returns:
    A list of lists, with each inner list containing the names of cows
    transported on a particular trip and the overall list containing all the
    trips
    """
    # condition - max per trip = 10
    # goal - find the minimum trips using the greedy algorithm
    # return - list of list of names

    # 1. create new list of tuples from cows dict
    lst = []
    for name, weight in cows.items():
        lst.append((name, weight))
    
    # 2. sort the list by weight
    lst = sorted(lst, key= lambda x: x[1], reverse= True)
    
    def maxV(toConsider, weightAvail, trip):
        # if no more cows or weight left == 0; continue
        if toConsider == [] or weightAvail == 0:
            return 
        # if weight too much, continue by calling maxV starting from next in list
        if toConsider[0][1] > weightAvail:
            maxV(toConsider[1:], weightAvail,trip)
        # weight < weightAvail
        else: 
            # add cow name to trip
            trip.append(toConsider[0][0])
            # reduce weight available by weight of cow
            weightAvail -= toConsider[0][1]
            # remove cow from cow list
            lst.remove(toConsider[0])
            # continue next 
            maxV(toConsider[1:], weightAvail, trip)

        return trip
    
    # 3. iterate through the list and insert into new list until old list == 0
    trip_list = []
    max_load = 10
    while len(lst) != 0:
        trip_list.append(maxV(lst, max_load, trip=[]))

    return trip_list

    

# Problem 3
def brute_force_cow_transport(cows,limit=10):
    """
    Finds the allocation of cows that minimizes the number of spaceship trips
    via brute force.  The brute force algorithm should follow the following method:

    1. Enumerate all possible ways that the cows can be divided into separate trips 
        Use the given get_partitions function in ps1_partition.py to help you!
    2. Select the allocation that minimizes the number of trips without making any trip
        that does not obey the weight limitation
            
    Does not mutate the given dictionary of cows.

    Parameters:
    cows - a dictionary of name (string), weight (int) pairs
    limit - weight limit of the spaceship (an int)
    
    Returns:
    A list of lists, with each inner list containing the names of cows
    transported on a particular trip and the overall list containing all the
    trips
    """
    maxV = []
    minTrip = math.inf
    for partition in get_partitions(cows):
        metWeightLimit = True
        for trip in partition:
            weight_avail = 10
            for cow in trip:
                if cows[cow] <= weight_avail:
                    weight_avail -= cows[cow]
                else:
                    metWeightLimit = False
        if metWeightLimit and len(partition) < minTrip:
            minTrip = len(partition)
            maxV = partition

    return maxV

        
# Problem 4
def compare_cow_transport_algorithms():
    """
    Using the data from ps1_cow_data.txt and the specified weight limit, run your
    greedy_cow_transport and brute_force_cow_transport functions here. Use the
    default weight limits of 10 for both greedy_cow_transport and
    brute_force_cow_transport.
    
    Print out the number of trips returned by each method, and how long each
    method takes to run in seconds.

    Returns:
    Does not return anything.
    """
    filename = "ps1_cow_data.txt"
    cows = load_cows(filename)
    print("greedy algo:")
    time_start_greedy = time.time()
    greedy_return = greedy_cow_transport(cows)
    time_end_greedy = time.time()
    time_taken_greedy = time_end_greedy - time_start_greedy
    print("Total time taken for greedy algo: ", time_taken_greedy)
    print("Return value: ", greedy_return)

    print("brute force algo")
    time_start_brute_force = time.time()
    brute_force_return = brute_force_cow_transport(cows)
    time_end_brute_force = time.time()
    time_taken_brute_force = time_end_brute_force - time_start_brute_force
    print("Total time taken for brute force algo: ", time_taken_brute_force)
    print("Return value: ", brute_force_return)


filename = "ps1_cow_data.txt"
cows = load_cows(filename)
greedy_cow_transport(cows)
# brute_force_cow_transport(cows)
# compare_cow_transport_algorithms()