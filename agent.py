# -*- coding: utf-8 -*-

import random

import gym


class Agent:
    """
    Representa um indivíduo capaz de executar ações no ambiente
    e promover auto-mutações.
    """

    def __init__(self, episodes, actions=None):
        """
        Constroi um novo agente. Cada indivíduo contém uma lista de
        ações a serem executadas.

        Args:

            episodes    :   quantidade de episódios a serem executados
                            no ambiente (ações), caso as ações não
                            estejam definidas.
            actions     :   lista de ações. Caso None, uma lista
                            de ações aleatórias será gerada.
        """
        self.episodes = episodes
        self.current_state = 0
        self.done = False

    def has_valid_actions(self):
        """
            Verifica se existem ações válidas a serem executadas.
        """
        raise NotImplementedError("This class has not implemented "
                                  "has_valid_actions()")

    def next_action(self, render=False):
        """
        Avança o indivíduo para o próximo estado.

        Args:
            render  :   se True, deve renderizar o ambiente.

        Deve retornar a observação do ambiente.
        """
        raise NotImplementedError("This class has not implemented "
                                  "next_action()")

    def mutate(self):
        """
        Deve alterar alguns bits aleatoriamente das ações do agente.
        """
        raise NotImplementedError("This class has not implemented "
                                  "mutate()")

    @property
    def fitness(self):
        """
        Retorna um número não negativo que determina o desempenho
        desse agente. Desempenhos melhores devem ter um valor de
        retorno mais alto, e devem ter preferência na escolha de
        soluções para o algoritmo de seleção de futuras gerações.
        """
        raise NotImplementedError("This class has not property "
                                  "fitness defined")

    @fitness.setter
    def fitness(self, fitness_function):
        """
        Configura a função fitness do agente.

        Args:
            fitness_function  :   função fitness do agente.
        """
        raise NotImplementedError("This class has not implemented "
                                  "fitness setter")


class Car(Agent):
    """
    Definição de um agente Car do ambiente MountainCar-v0
    """
    valid_actions = [0, 1, 2]

    def __init__(self, episodes, actions=None):
        super(Car, self).__init__(episodes, actions)
        self.environment = gym.make('MountainCar-v0')
        self.environment.reset()

        if actions is None:
            self.actions = []
            for i in range(episodes):
                self.actions.append(random.choice(Car.valid_actions))
        else:
            self.actions = actions
        self.positions = []
        self.velocities = []
        self._fitness_function = None

    def has_valid_actions(self):
        return self.current_state < len(self.actions) and not self.done

    def next_action(self, render=False):
        if self.current_state == 0:
            self.environment.reset()
        if render:
            self.environment.render()
        observation, reward, done, info = \
            self.environment.step(self.actions[self.current_state])
        self.done = observation[0] == 0.6
        self.positions.append(observation[0])
        self.velocities.append(observation[1])
        self.current_state += 1
        return observation

    def mutate(self):
        start = random.randint(0, len(self.actions) - 5)
        action = random.choice(Car.valid_actions)
        for i in range(start, start + 5):
            self.actions[i] = action

    @property
    def fitness(self):
        return self._fitness_function(self)

    @fitness.setter
    def fitness(self, fitness_function):
        self._fitness_function = fitness_function

    @staticmethod
    def position_fitness_function(car):
        """
        Retorna um valor fitness obtido através da posição máxima 
        alcançada pelo agente como função.
        """

        return (max(car.positions) + 1) ** 10

    @staticmethod
    def velocity_fitness_function(car):
        """
        Retorna um valor fitness obtido através da velocidade máxima 
        alcançada pelo agente como função.
        """

        return (max(car.velocities) + 1) ** 100

    @staticmethod
    def acceleration_fitness_function(car):
        """
        Retorna um valor fitness obtido através da aceleração máxima 
        alcançada pelo agente como função, através da equação de 
        Torricelli.
        """

        s1 = car.positions[0]
        v1 = car.velocities[0]
        accelerations = []
        for i in range(1, len(car.velocities) - 1):
            s0 = s1
            v0 = v1
            s1 = car.positions[i]
            v1 = car.velocities[i]
            accelerations.append((v1 ** 2 + v0 ** 2) / 2 * (s1 - s0))
        return max(accelerations) 

    def __str__(self):
        return "Actions={} \nPositions={} \nVelocities={} \nDone={}". \
            format(self.actions, self.positions, self.velocities, self.done)



