# -*- coding: utf-8 -*-

from genetic import *
from agent import *
import matplotlib.pyplot as plt
import argparse
import os

PATH_SOLUTIONS = "output/solutions"
PATH_FITNESSES = "output/fitnesses"
PATH_IMAGES = "output/images"


def main():
    args = parser.parse_args()

    if args.acc:
        fitness_fn = Car.acceleration_fitness_function
    elif args.vel:
        fitness_fn = Car.velocity_fitness_function
    else:
        fitness_fn = Car.position_fitness_function

    problem = Problem(Car, args.population, args.episodes)
    problem_solving = GeneticSolve(problem, args.mut, args.generations,
                                   fitness_fn)

    if not os.path.exists(PATH_SOLUTIONS):
        os.makedirs(PATH_SOLUTIONS)
    if not os.path.exists(PATH_FITNESSES):
        os.makedirs(PATH_FITNESSES)
    if not os.path.exists(PATH_IMAGES):
        os.makedirs(PATH_IMAGES)

    print("\nSolving for {} episodes, {} generations, {} individuals and {} "
          "mutation frequency. Using the {}".format(args.episodes,
                                                    args.generations,
                                                    args.population,
                                                    args.mut,
                                                    fitness_fn.__name__))
    problem_solving.solve()

    if problem.done:
        solutions = []
        for solution in problem.solutions:
            if solutions not in solutions:
                solutions.append(solution)
            with open("output/solutions/solution_{}_{}_{}_{}_{}.txt".format(
                args.episodes,
                args.generations,
                args.population,
                args.mut,
                    problem_solving.date_solving), "a") as output_file:
                output_file.write(str(solution) + "\n")
        print("\nExecution finished. There were found {} possible solutions.".
              format(len(solutions)))
        if args.show:
            for solution in solutions:
                show(Car(args.episodes, actions=solution))
    else:
        print("\nNo solution.")

    if args.plot:
        print("\nGenerating graph")
        fitnesses_file = open("output/fitnesses/{}_{}_{}_{}_{}_{}.txt".format(
            problem_solving.fitness_fn.__name__,
            problem_solving.problem.episodes,
            problem_solving.generations,
            len(problem_solving.population),
            str(int(problem_solving.p_mutation * 100)), 
            problem_solving.date_solving), "r")

        points = []
        for line in fitnesses_file:
            points.append(float(line))

        fig, ax = plt.subplots()
        ax.tick_params(labelsize=7)
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        ax.set_xlim((0, args.generations))
        ax.set_xticks([0, args.generations/5, 2*args.generations/5,
                       3*args.generations/5, 4*args.generations/5],
                      args.generations)

        ax.set_xticklabels(['0',
                            str(args.generations/5), str(2*args.generations/5),
                            str(3*args.generations/5), str(4*args.generations/5),
                            args.generations])
        ax.set_ylim((0, max(points)))
        ax.set_yticks([0, max(points)/5, 2*max(points)/5, 3*max(points)/5,
                       4*max(points)/5, max(points)])

        plt.plot(points, '.', markersize=0.8, color="gray")
        plt.savefig("output/images/{}_{}_{}_{}_{}_{}.pdf".format(
            problem_solving.problem.episodes,
            problem_solving.fitness_fn.__name__,
            problem_solving.generations,
            len(problem_solving.population),
            str(int(problem_solving.p_mutation * 100)),
            problem_solving.date_solving))


def show(individual):
    """
    Nota: Serão reproduzidas as ações das soluções, mas o agente
    inicia em posição aletória. Podem ocorrer variações da
    solução original.
    """
    while individual.has_valid_actions():
        individual.next_action(True)
    individual.environment.close()


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Execute the genetic algorithm'
                                                 ' to solve the MountainCar'
                                                 ' OpenAI environment problem.')
    parser.add_argument("--show", help='show the final solutions',
                        action="store_true")
    parser.add_argument("--plot", help='plots and save a graph with the '
                                       'average fitnesses of each generation',
                        action="store_true")
    parser.add_argument("episodes", help="sets the number of episodes",
                        type=int)
    parser.add_argument("generations", help="sets the number of generations",
                        type=int)
    parser.add_argument("population", help="sets the number of agents",
                        type=int)
    parser.add_argument("mut", help="sets the mutation frequency [0.0 - 1.0]",
                        type=float)
    parser.add_argument("--acc", help='use the acceleration fitness function',
                        action="store_true")
    parser.add_argument("--pos", help='use the position fitness function, this'
                                      ' is the default option',
                        action="store_false")
    parser.add_argument("--vel", help='use the velocity fitness function',
                        action="store_true")
    main()
