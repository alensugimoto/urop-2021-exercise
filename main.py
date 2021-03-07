from ga.chromosome_elem import ChromosomeElem
from ga.genetic_algorithm import genetic_algorithm
from track_generator.command import Command
from track_generator.generator import generate_track
from config import CHROMOSOME_LENGTH

import matplotlib.pyplot as plt

if __name__ == '__main__':

    # number of bits representing one instruction
    num_bits_per_inst = 34  # > 2
    # number of instructions per track
    chromosome_length = CHROMOSOME_LENGTH
    # population of every generation
    population_size = 100  # even
    # number of new generations to be generated
    num_generations = 100  # > 0
    # penalty coefficients for fitness function
    penalty_coefs = (50.0, 0.0)
    # lower and uppers bounds of instruction values
    value_bounds = ((5.0, 10.0), (5.0, 10.0), (5.0, 10.0), (5.0, 45.0))
    # probability of crossover between two parents
    crossover_rate = 0.9
    # probability of mutaton (bit flip) per every bit
    mutation_rate = 1.0 / float(num_bits_per_inst * chromosome_length)

    chromosome_elements = genetic_algorithm(
        num_bits_per_inst=num_bits_per_inst,
        chromosome_length=chromosome_length,
        population_size=population_size,
        num_generations=num_generations,
        penalty_coefs=penalty_coefs,
        value_bounds=value_bounds,
        crossover_rate=crossover_rate,
        mutation_rate=mutation_rate)

    track_points = generate_track(chromosome_elements=chromosome_elements)

    plot_x = [track_point.x for track_point in track_points]
    plot_y = [track_point.y for track_point in track_points]
    plt.scatter(plot_x, plot_y)
    plt.show()
