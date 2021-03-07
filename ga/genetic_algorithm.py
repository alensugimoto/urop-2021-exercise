import math
from typing import List, Tuple

from numpy.random import randint
from numpy.random import rand

from ga.chromosome_elem import ChromosomeElem
from track_generator.command import Command
from track_generator.track_point import TrackPoint
from track_generator.generator import generate_track

Pair = Tuple[float, float]
Bitstring = List[int]


def genetic_algorithm(
    num_bits_per_inst: int,
    chromosome_length: int,
    population_size: int,
    num_generations: int,
    penalty_coefs: Pair,
    value_bounds: Tuple[Pair, Pair, Pair, Pair],
    crossover_rate: float,
    mutation_rate: float,
) -> List[ChromosomeElem]:
    # keep track of best solution
    best_chromosome: List[ChromosomeElem]
    best_score: float
    # initial population of random bitstrings
    pop: List[Bitstring] = [randint(0, 2, num_bits_per_inst * chromosome_length).tolist()
                            for _ in range(population_size)]
    # enumerate generations
    for gen in range(num_generations):
        # decode population
        decoded_pop: List[List[ChromosomeElem]] = [decode(
            bitstring=bitstring,
            num_bits_per_inst=num_bits_per_inst,
            chromosome_length=chromosome_length,
            value_bounds=value_bounds,
        ) for bitstring in pop]
        # evaluate all chromosomes in the population
        scores: List[float] = [fitness(
            chromosome_elements=chromosome_elements,
            penalty_coefs=penalty_coefs,
        ) for chromosome_elements in decoded_pop]
        # check for new best solution
        for i in range(population_size):
            if gen == i == 0 or scores[i] < best_score:
                best_chromosome, best_score = decoded_pop[i], scores[i]
                print(">%(gen)d, new best f([%(chromosome)s]) = %(score)f" % {
                    "gen": gen,
                    "chromosome": ', '.join([str(elem) for elem in best_chromosome]),
                    "score": best_score})
        # select parents
        selected: List[Bitstring] = [selection(
            population=pop,
            scores=scores,
        ) for _ in range(population_size)]
        # create the next generation
        children: List[Bitstring] = []
        for i in range(0, population_size, 2):
            # get selected parents in pairs
            parent1, parent2 = selected[i], selected[i + 1]
            # crossover and mutation
            for child in crossover(
                parent1=parent1,
                parent2=parent2,
                num_bits_per_inst=num_bits_per_inst,
                chromosome_length=chromosome_length,
                crossover_rate=crossover_rate,
            ):
                # mutation
                child = mutation(bitstring=child, mutation_rate=mutation_rate)
                # store for next generation
                children.append(child)
        # replace population
        pop = children
    print('Done!')
    print("f([%(chromosome)s]) = %(score)f" % {
        "chromosome": ', '.join([str(elem) for elem in best_chromosome]),
        "score": best_score})
    return best_chromosome


def decode(
    bitstring: Bitstring,
    num_bits_per_inst: int,
    chromosome_length: int,
    value_bounds: Tuple[Pair, Pair, Pair, Pair],
) -> List[ChromosomeElem]:
    decoded: List[ChromosomeElem] = []
    prev_command: Command
    # decode each instruction
    for i in range(chromosome_length):
        start = i * num_bits_per_inst
        end = start + num_bits_per_inst
        # decode command of instruction
        command: Command
        num_command_bits = 2
        if i == 0 or i == chromosome_length - 1:
            command = Command.S
        else:
            command_substring = bitstring[start:start + num_command_bits]
            command_chars = ''.join([str(s) for s in command_substring])
            if i == chromosome_length - 2:
                # possible commands: S, R, L
                command = Command(int(command_chars, 2) % 3)
            elif prev_command == Command.S:
                # possible commands: S, R, L, DY
                command = Command(int(command_chars, 2))
            elif prev_command == Command.DY:
                # possible commands: R, L
                command = Command(int(command_chars, 2) % 2 + 1)
            else:
                # possible commands: S, DY
                command = Command(int(command_chars, 2) % 2 * 3)
        # decode value of instruction
        value: float
        num_value_bits = num_bits_per_inst - num_command_bits
        value_substring = bitstring[start + num_command_bits:end]
        value_chars = ''.join([str(s) for s in value_substring])
        integer = int(value_chars, 2)
        # scale integer to desired range
        largest_value = 2**num_value_bits - 1
        value = value_bounds[command.value][0] + (integer / largest_value) * (
            value_bounds[command.value][1] - value_bounds[command.value][0])
        # prepare for next iteration
        prev_command = command
        decoded.append(ChromosomeElem(command=command, value=value))
    return decoded


def fitness(
    chromosome_elements: List[ChromosomeElem],
    penalty_coefs: Tuple[float, float],
) -> float:
    # generate track points
    track_points = generate_track(chromosome_elements=chromosome_elements)
    # calculate distance between start and end points
    start_point = TrackPoint(track_points[0].x, track_points[0].y - 2)
    end_point = track_points[-1]
    disp = math.sqrt((start_point.x - end_point.x)**2
                     + (start_point.y - end_point.y)**2)
    # find all vertices of the track
    vertices = track_vertices(
        track_points=[end_point] + track_points,
        chromosome_elements=chromosome_elements)
    # calculate number of line-segment intersections
    num_intersects = 0
    for i in range(len(vertices) - 2):
        for j in range(i + 1, len(vertices) - 1):
            p1, p2 = vertices[i], vertices[i + 1]
            p3, p4 = vertices[j], vertices[j + 1]
            x1, x2, x3, x4 = p1.x, p2.x, p3.x, p4.x
            y1, y2, y3, y4 = p1.y, p2.y, p3.y, p4.y
            # check if segments intersect
            denom = (x1 - x2) * (y3 - y4) - (y1 - y2) * (x3 - x4)
            if denom != 0:
                t = ((x1 - x3) * (y3 - y4) - (y1 - y3) * (x3 - x4)) / denom
                if 0 < t <= 1:
                    u = ((x2 - x1) * (y1 - y3) - (y2 - y1) * (x1 - x3)) / denom
                    if 0 < u <= 1:
                        num_intersects += 1
    # calculate difference in vehicle direction at start and end points
    angle = math.atan2(
        end_point.y - track_points[-2].y,
        end_point.x - track_points[-2].x)
    if angle <= -math.pi / 2:
        angle += 2 * math.pi
    diff_direction = abs(math.pi / 2 - angle)
    # combine results
    return disp + penalty_coefs[0] * num_intersects + penalty_coefs[1] * diff_direction


def track_vertices(
    track_points: List[TrackPoint],
    chromosome_elements: List[ChromosomeElem],
) -> List[TrackPoint]:
    vertices: List[TrackPoint] = track_points[0:2]
    steps: int = 0
    prev_command: Command = Command.R
    # find vertices for each intruction
    for ce in chromosome_elements:
        command = ce.command
        args = ce.value
        if command == Command.S:
            steps += int(args)
            if steps > 1:
                if prev_command == Command.S:
                    vertices[-1] = track_points[steps]
                else:
                    vertices.append(track_points[steps])
        elif command != Command.DY:
            vertices += track_points[steps + 1:steps + int(args) + 1]
            steps += int(args)
        prev_command = command
    return vertices


def selection(
    population: List[Bitstring],
    scores: List[float],
    k: int = 3,
) -> Bitstring:
    # select a random index
    selection_i = randint(len(population))
    for i in randint(0, len(population), k - 1):
        # check if this index is better than 'selection_i'
        if scores[i] < scores[selection_i]:
            # update best index
            selection_i = i
    return population[selection_i]


def crossover(
    parent1: Bitstring,
    parent2: Bitstring,
    num_bits_per_inst: int,
    chromosome_length: int,
    crossover_rate: float,
) -> Tuple[Bitstring, Bitstring]:
    # copy parents into children
    child1, child2 = parent1.copy(), parent2.copy()
    # try to perform a crossover
    if rand() < crossover_rate:
        # select crossover point
        pt = randint(1, chromosome_length) * num_bits_per_inst
        # perform crossover
        child1 = parent1[:pt] + parent2[pt:]
        child2 = parent2[:pt] + parent1[pt:]
    return (child1, child2)


def mutation(
    bitstring: Bitstring,
    mutation_rate: float,
) -> Bitstring:
    for i in range(len(bitstring)):
        # try to mutate bit
        if rand() < mutation_rate:
            # flip bit
            bitstring[i] = 1 - bitstring[i]
    return bitstring
