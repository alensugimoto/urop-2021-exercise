from ga.genetic_algorithm import genetic_algorithm, decode
from ga.chromosome_elem import ChromosomeElem
from track_generator.command import Command
from track_generator.generator import generate_track

import matplotlib.pyplot as plt
from config import *

if __name__ == '__main__':

    # perform the genetic algorithm search
    best, score = genetic_algorithm(INST_VALUE_BOUNDS, CHROMOSOME_LENGTH, NUM_ELEMENT_BITS, NUM_GENERATIONS, POPULATION_SIZE, PENALTY_COEF, CROSSOVER_RATE, MUTATION_RATE)
    print('Done!')
    chromosome_elements = decode(INST_VALUE_BOUNDS, CHROMOSOME_LENGTH, NUM_ELEMENT_BITS, best)
    print('f(%s) = %f' % ([str(d) for d in chromosome_elements], score))

    track_points = generate_track(chromosome_elements=chromosome_elements)

    plot_x = [track_point.x for track_point in track_points]
    plot_y = [track_point.y for track_point in track_points]
    plt.scatter(plot_x, plot_y)
    plt.show()
