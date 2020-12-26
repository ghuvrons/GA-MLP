import random

class GeneticAlgorithm:
    def __init__(self):
        self.number_of_population = 10
        self.number_of_generation = 2
        self.generation = []
        self.population = []

    def fitness_func(self, individu):
        pass

    def randomArray(self, arr, length = 1):
        rand_arr = []
        
        tmp_population = arr.copy()
        while len(tmp_population) > 0 and len(rand_arr) < length:
            i = random.randint(0, len(tmp_population)-1)
            val = tmp_population[i]
            del tmp_population[i]
            rand_arr.append(val)
        return rand_arr

    def setFirstGeneration(self):
        self.generation = []
        self.population = []
        for i in range(self.number_of_population):
            individu = self.createIndividu([
                random.randint(1, 100),
                random.randint(1, 100),
                random.randint(1, 100),
                random.randint(1, 100),
                random.randint(1, 100)
            ])
            self.population.append(individu)
        self.generation.append(self.population)

    def fitness(self, f):
        print(">", f)
        self.fitness_func = f
        def decorator():
            return self.fitness_func
        return decorator

    def addPopulation(self, individu):
        # individu = [hl1, hl2, hl3, hl4, hl5]
        # hl1 = jumlah hl1
        self.population.append({
            "kromosom": individu,
            "fitness": self.fitness_func(individu),
            "isMarried": False
        })

    def createIndividu(self, individu, parents = None):
        return {
            "kromosom": individu,
            "model": None,
            "fitness": 0,
            "isMarried": False,
            "parents": parents
        }

    def crossOverSinglePoint(self, parent1, parent2):
        # parent1 = [hl1, hl2, hl3, hl4, hl5]
        # parent2 = [hl1, hl2, hl3, hl4, hl5]
        p1 = parent1["kromosom"]
        p2 = parent2["kromosom"]
        point = random.randint(1, 4)
        child1 = self.createIndividu([])
        child2 = self.createIndividu([])
        for i in range(len(p1)):
            hl = None
            if i < point:
                child1["kromosom"].append(p1[i])
                child2["kromosom"].append(p2[i])
            else:
                child1["kromosom"].append(p2[i])
                child2["kromosom"].append(p1[i])
        return child1, child2

    def crossOverAvg(self, parent1, parent2, rate = 0.2):
        # parent1 = [hl1, hl2, hl3, hl4, hl5]
        # parent2 = [hl1, hl2, hl3, hl4, hl5]
        p1 = parent1["kromosom"]
        p2 = parent2["kromosom"]

        length_kromosom = len(p1)
        number_of_co_gen = round(length_kromosom * rate)

        random_index = self.randomArray(range(length_kromosom), length=number_of_co_gen)
        
        child1 = self.createIndividu([])
        child2 = self.createIndividu([])
        for i in range(length_kromosom):
            hl = None
            if i in random_index:
                avg = round((p1[i] + p2[i])/2)
                child1["kromosom"].append(avg)
                child2["kromosom"].append(avg)
            else:
                child1["kromosom"].append(p2[i])
                child2["kromosom"].append(p1[i])
        return child1, child2

    def setFitness(self, individu):
        self.fitness_func(individu)

    def mutation(self, individu):
        # mutasi
        point = random.randint(0, 4)
        return individu

    def etilsmReplacement(self):
        pass

    def selection(self):
        mates = []
        tmp_population = self.population.copy()
        while len(tmp_population) > 0:
            i = random.randint(0, len(tmp_population)-1)
            ind_1 = tmp_population[i]
            del tmp_population[i]
            
            i = random.randint(0, len(tmp_population)-1)
            ind_2 = tmp_population[i]
            del tmp_population[i]
            
            mates.append((ind_1, ind_2, ))
        return mates

    def newGeneration(self):
        self.newGen = []
        # cari jodoh : select from population
        mates = self.selection()
        for parent1, parent2 in mates:
            print("crossing over >", parent1["kromosom"], parent2["kromosom"])
            child1, child2 = self.crossOverAvg(parent1, parent2)
            print("children >", child1["kromosom"], child2["kromosom"])

            # mutasi

            # hitung fitness
            print("getting fitness > ...")
            self.setFitness(child1)
            self.setFitness(child2)
            print("get fitness > done")
            # dipilih
            self.newGen.append(child1)
            self.newGen.append(child2)
        self.population = self.newGen
        self.generation.append(self.population)