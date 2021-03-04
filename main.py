from ga.chromosome_elem import ChromosomeElem
from track_generator.command import Command
from track_generator.generator import generate_track

import matplotlib.pyplot as plt
import config
import math

if __name__ == '__main__':

    # decode a bitstring to a chromosome
    def decode(bitstring, bounds, n_inst, n_bits):
        # for every n_bits in bitstring, decode an instruction
        # ensure values are of the right type
        return # decoded chromosome

    # fitness function
    def fitness(inst, c_penalty):
        # generate track points
        # calculate distance between start and end points
        # calculate number of segment intersections
        return # distance + c_penalty * intersections

    # tournament selection
    def selection(pop, scores, k=3):
        # pick and compare k chromosomes
        return # best chromosome

    # two-parent crossover
    def crossover(p1, p2, r_cross):
        # copy parents into children
        # perform crossover based on crossover rate
        return # children

    # mutation operator
    def mutation(bitstring, r_mut):
        # for each bit, perform a bit flip based on mutation rate
        return # nothing

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
