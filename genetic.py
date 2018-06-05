# -*- coding: utf-8 -*-

from statistics import mean
from datetime import datetime
import random


class Problem:
    """ Define um problema para a execução do algoritmo genético.

        Args:

            agent_class         :   classe Agent que define o agente
            population_size     :   quantidade de indivíduos a
                                    serem criados inicialmente
            episodes            :   quantidade de episódios a
                                    serem executados por cada
                                    indivíduo.
            .
    """

    def __init__(self, agent_class, population_size, episodes):
        self.episodes = episodes
        self.population_size = population_size
        self.done = False
        self.solutions = []
        self.agent = agent_class


class GeneticSolve:
    """ Define um problema para a execução do algoritmo genético.

        Args:

            problem             :   problema a ser resolvido
            p_mutation          :   parâmetro que define a frequência
                                    de mutação da população a cada
                                    geração.
            generations         :   quantidade de gerações a serem
                                    promovidas.
            fitness_fn          :   função fitness.

    """

    def __init__(self, problem, p_mutation, generations, fitness_fn):
        self.problem = problem
        self.population = self.init_population()
        self.p_mutation = p_mutation
        self.generations = generations
        self.fitness_fn = fitness_fn
        self.date_solving = None

    def init_population(self):
        """ Inicializa uma população para a execução do algoritmo
            genético.

            Args:

                population_size     :   quantidade de indivíduos a
                                        serem criados inicialmente
                state_length        :   quantidade de estados a
                                        serem executados por cada
                                        indivíduo.
                agent_class         :   classe agente para a criação
                                        dos agentes
        """
        agents = []
        for i in range(0, self.problem.population_size):
            agents.append(self.problem.agent(self.problem.episodes))
        return agents

    def solve(self):
        """ Executa o algoritmo genético."""

        self.date_solving = "{}-{}-{}_{}:{}:{}".format(datetime.now().month,
                                                       datetime.now().day,
                                                       datetime.now().year,
                                                       datetime.now().hour,
                                                       datetime.now().minute,
                                                       datetime.now().second)

        for i in range(self.generations):
            for individual in self.population:
                while individual.has_valid_actions():
                    individual.next_action()
                    if individual.done:
                        self.problem.done = True
                        self.problem.solutions.append(list(individual.actions))
            selection = self._selection_choices()

            new_population = []

            for individual in selection:
                new_population.append(self._reproduce(individual, random.
                                                      choice(selection)))
            self.population = new_population

            for individual in self.population:
                if random.random() <= self.p_mutation:
                    individual.mutate()

    def _selection_choices(self):
        """
            Retorna uma lista com indivíduos melhores. A lista é formada
            randomicamente pelos indivíduos da população.
            A frequência dos indivíduos na lista depende do desempenho
            (fitness) de cada um.

            Use essa lista de indivíduos para gerar uma nova população.

            Args:

                fitness_function    :   Função fitness
                population          :   População a ser selecionada

        """

        fitnesses = []
        for individual in self.population:
            fitness = self.fitness_fn(individual) 
            # print(fitness)
            fitnesses.append(fitness)

        with open("output/fitnesses/{}_{}_{}_{}_{}_{}.txt".format(
                self.fitness_fn.__name__,
                self.problem.episodes,
                self.generations,
                len(self.population),
                str(int(self.p_mutation * 100)),
                self.date_solving), "a") as outputFile:
            outputFile.write(str(mean(fitnesses)) + "\n")
        selection = random.choices(self.population, fitnesses,
                                   k=len(self.population))
        return selection

    def _reproduce(self, x, y):
        """ Retorna um novo indivíduo a partir de um par de indivíduos.

            Args:
                x    :   indivíduo pai
                y    :   indivíduo pai

        """
        n = len(x.actions)
        c = random.randrange(1, n)
        return self.problem.agent(x.episodes, actions=x.actions[:c] +
                                                      y.actions[c:])
    
    def reset(self):
        self.population = self.init_population()
