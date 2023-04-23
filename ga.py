import random

# Konstanten
TARGET = "HELLO WORLD"
POP_SIZE = 100
MUTATION_RATE = 0.1

# Erstelle eine zufällige Population von Bakterien
def create_population():
    population = []
    for i in range(POP_SIZE):
        bacteria = []
        for j in range(len(TARGET)):
            bacteria.append(random.choice("ABCDEFGHIJKLMNOPQRSTUVWXYZ "))
        population.append(bacteria)
    return population

# Bewertung der Fitness
def fitness(bacteria):
    score = 0
    for i in range(len(TARGET)):
        if bacteria[i] == TARGET[i]:
            score += 1
    return score / len(TARGET)

# Selektion der besten Bakterien
def selection(population):
    fitness_scores = [(bacteria, fitness(bacteria)) for bacteria in population]
    fitness_scores.sort(key=lambda x: x[1], reverse=True)
    return [fitness_scores[i][0] for i in range(int(POP_SIZE/2))]

# Kreuzung (Crossover)
def crossover(parent1, parent2):
    child = []
    midpoint = random.randint(0, len(parent1)-1)
    for i in range(len(parent1)):
        if i < midpoint:
            child.append(parent1[i])
        else:
            child.append(parent2[i])
    return child

# Mutation
def mutate(bacteria):
    for i in range(len(bacteria)):
        if random.random() < MUTATION_RATE:
            bacteria[i] = random.choice("ABCDEFGHIJKLMNOPQRSTUVWXYZ ")
    return bacteria

# Genetischer Algorithmus
def genetic_algorithm():
    population = create_population()
    generations = 0
    while True:
        generations += 1
        best_bacteria = selection(population)[0]
        fitness_score = fitness(best_bacteria)
        if fitness_score == 1.0:
            print(f"Solution found in {generations} generations: {''.join(best_bacteria)}")
            break
        new_population = [best_bacteria]
        while len(new_population) < POP_SIZE:
            parent1 = random.choice(population)
            parent2 = random.choice(population)
            child = crossover(parent1, parent2)
            child = mutate(child)
            new_population.append(child)
        population = new_population

# Ausführen des genetischen Algorithmus
genetic_algorithm()