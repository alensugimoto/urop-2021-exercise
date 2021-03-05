from ga.chromosome_elem import ChromosomeElem
from track_generator.track_point import TrackPoint
from track_generator.command import Command
from track_generator.generator import generate_track
from numpy.random import randint
from numpy.random import rand

import math

# decode a bitstring to a chromosome
def decode(bounds, n_inst, n_bits, bitstring):
    decoded = list()
    prev_command = None
    largest_value = 2**(n_bits - 2)
    # decode each instruction
    for i in range(n_inst):
        command = None
        start = i * n_bits
        end = start + n_bits

        # decode command of instruction
        if i == 0 or i == n_inst - 1:
            command = Command.S
        elif prev_command == Command.S:
            # extract the substring
            command_substring = bitstring[start:start + 2]
            # convert bitstring to a string of chars
            command_chars = ''.join([str(s) for s in command_substring])
            # convert string to integer
            command = Command(int(command_chars, 2))
        else:
            # extract the substring
            command_substring = bitstring[start + 1:start + 2]
            # convert bitstring to a string of chars
            command_chars = ''.join([str(s) for s in command_substring])
            # convert string to a command
            if prev_command == Command.DY:
                command = Command(int(command_chars, 2) + 1)
            else:
                command = Command(int(command_chars, 2) * 3)

        # decode value of instruction
        # extract the substring
        value_substring = bitstring[start + 3:end]
        # convert bitstring to a string of chars
        value_chars = ''.join([str(s) for s in value_substring])
        # convert string to integer
        integer = int(value_chars, 2)
        # scale integer to desired range
        value = bounds[command.value][0] + (integer / largest_value) * \
            (bounds[command.value][1] - bounds[command.value][0])

        # store
        prev_command = command
        decoded.append(ChromosomeElem(command=command, value=value))
    return decoded

# evaluate the fitness of 'chromosome'
def fitness(chromosome, c_penalty):
    # generate track points
    track_points = generate_track(chromosome_elements=chromosome)
    # calculate distance between start and end points
    track_points = [TrackPoint(track_points[0].x, track_points[0].y - 2)] + track_points
    start_point = track_points[0]
    end_point = track_points[len(track_points) - 1]
    distance = math.sqrt((start_point.x - end_point.x)
                         ** 2 + (start_point.y - end_point.y)**2)
    # calculate number of segment intersections
    n_int = 0
    for i in range(len(track_points) - 3):
        for j in range(i + 2, len(track_points) - 1):
            # set up points
            p1, p2 = track_points[i], track_points[i + 1]
            p3, p4 = track_points[j], track_points[j + 1]
            x1, x2, x3, x4 = p1.x, p2.x, p3.x, p4.x
            y1, y2, y3, y4 = p1.y, p2.y, p3.y, p4.y
            # check if segments intersect
            '''
            left1, right1 = min(x1, x2), max(x1, x2)
            left2, right2 = min(x3, x4), max(x3, x4)
            bottom1, top1 = min(y1, y2), max(y1, y2)
            bottom2, top2 = min(y3, y4), max(y3, y4)
            if left1 <= right2 and right1 >= left2 and top1 >= bottom2 and bottom1 <= top2:
            '''
            denom = (x1 - x2) * (y3 - y4) - (y1 - y2) * (x3 - x4)
            if denom != 0:
                t = ((x1 - x3) * (y3 - y4) - (y1 - y3) * (x3 - x4)) / denom
                if 0 < t <= 1:
                    u = (((x2 - x1) * (y1 - y3)) -
                         ((y2 - y1) * (x1 - x3))) / denom
                    if 0 < u <= 1:
                        # increment 'n_int'
                        n_int += 1
    # calculate degree of kink at start and end points
    angle1 = math.atan2(
        track_points[1].y - track_points[0].y,
        track_points[1].x - track_points[0].x
    )
    angle2 = math.atan2(
        track_points[len(track_points) - 1].y - track_points[len(track_points) - 2].y,
        track_points[len(track_points) - 1].x - track_points[len(track_points) - 2].x
    )
    diff = abs(angle1 - angle2)

    return distance + c_penalty * (n_int + 0.2 * diff)

# select a parent with tournament selection
def selection(pop, scores, k=3):
    # select a random index
    selection_i = randint(len(pop))
    for i in randint(0, len(pop), k - 1):
        # check if this index is better than 'selection_i'
        if scores[i] < scores[selection_i]:
            # update best index
            selection_i = i
    return pop[selection_i]

# perform a singe-point crossover
def crossover(p1, p2, r_cross):
    # copy parents into children
    c1, c2 = p1.copy(), p2.copy()
    # try to perform a crossover
    if rand() < r_cross:
        # select crossover point
        pt = randint(1, len(p1))
        # perform crossover
        c1 = p1[:pt] + p2[pt:]
        c2 = p2[:pt] + p1[pt:]
    return [c1, c2]

# mutate 'bitstring' at a rate 'r_mut'
def mutation(bitstring, r_mut):
    for i in range(len(bitstring)):
        # try to mutate bit
        if rand() < r_mut:
            # flip bit
            bitstring[i] = 1 - bitstring[i]

# genetic algorithm
def genetic_algorithm(bounds, n_inst, n_bits, n_iter, n_pop, c_penalty, r_cross, r_mut):
    # initial population of random bitstrings
    pop = [randint(0, 2, n_bits * n_inst).tolist() for _ in range(n_pop)]
    # keep track of best solution
    best, best_eval = None, None
    # enumerate generations
    for gen in range(n_iter):
        # decode population
        decoded = [decode(bounds, n_inst, n_bits, p) for p in pop]
        # evaluate all chromosomes in the population
        scores = [fitness(d, c_penalty) for d in decoded]
        # check for new best solution
        for i in range(n_pop):
            if best_eval is None or scores[i] < best_eval:
                best, best_eval = pop[i], scores[i]
                print(">%d, new best f(%s) = %f" %
                      (gen, [str(d) for d in decoded[i]], scores[i]))
        # select parents
        selected = [selection(pop, scores) for _ in range(n_pop)]
        # create the next generation
        children = list()
        for i in range(0, n_pop, 2):
            # get selected parents in pairs
            p1, p2 = selected[i], selected[i + 1]
            # crossover and mutation
            for c in crossover(p1, p2, r_cross):
                # mutation
                mutation(c, r_mut)
                # store for next generation
                children.append(c)
        # replace population
        pop = children
    return [best, best_eval]
