from ga.chromosome_elem import ChromosomeElem
from track_generator.command import Command
from track_generator.generator import generate_track
from numpy.random import randint
from numpy.random import rand

import matplotlib.pyplot as plt
import config
import math

if __name__ == '__main__':

    # decode a bitstring to a chromosome
    def decode(bitstring, bounds, n_inst, n_bits):
        # for every n_bits in bitstring, decode an instruction
        # ensure values are of the right type
        return # decoded chromosome

    # evaluate the fitness of 'chromosome'
    def fitness(chromosome, c_penalty):
        # generate track points
        track_points = generate_track(chromosome_elements=chromosome)
        # calculate distance between start and end points
        start_point = track_points[0]
        end_point = track_points[len(chromosome_elements)-1]
        distance = math.sqrt((start_point.x - end_point.x)**2 + (start_point.y - end_point.y)**2)
        # calculate number of segment intersections
        n_int = 0
        for i in range(len(track_points) - 3):
            for j in range(i + 2, len(track_points) - 1):
                # set up points
                p1, p2 = track_points[i], track_points[i+1]
                p3, p4 = track_points[j], track_points[j+1]
                x1, x2, x3, x4 = p1.x, p2.x, p3.x, p4.x
                y1, y2, y3, y4 = p1.y, p2.y, p3.y, p4.y
                # check if segments intersect
                denom = (x1-x2) * (y3-y4) - (y1-y2) * (x3-x4);
                if denom != 0:
                    t = ((x1-x3) * (y3-y4) - (y1-y3) * (x3-x4)) / denom
                    if 0 < t <= 1:
                        u = (((x2-x1) * (y1-y3)) - ((y2-y1) * (x1-x3))) / denom
                        if 0 < u <= 1:
                            # increment 'n_int'
                            n_int += 1
        return distance + c_penalty * n_int

    # select a parent with tournament selection
    def selection(pop, scores, k=3):
    	# select a random index
    	selection_i = randint(len(pop))
    	for i in randint(0, len(pop), k-1):
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
    def genetic_algorithm(fitness, bounds, n_inst, n_bits, n_iter, n_pop, c_penalty, r_cross, r_mut):
        # generate random bitstring
        # for every generation:
        #   decode population
        #   get fitness values
        #   select parents
        #   create new population
        return # best solution

    chromosome_elements = [ChromosomeElem(command=Command.S, value=11),
                           ChromosomeElem(command=Command.DY, value=15.5),
                           ChromosomeElem(command=Command.R, value=9),
                           ChromosomeElem(command=Command.S, value=10)]

    track_points = generate_track(chromosome_elements=chromosome_elements)

    plot_x = [track_point.x for track_point in track_points]
    plot_y = [track_point.y for track_point in track_points]
    plt.scatter(plot_x, plot_y)
    plt.show()
