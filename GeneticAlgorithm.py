import random
import pickle
import os

class GeneticAlgorithm:
    def __init__(self):
        self.number_of_population = 10
        self.number_of_generation = 2
        self.min_gen = 1
        self.max_gen = 100
        self.generation = []
        self.population = []

    def fitness_func(self, individu):
        pass

    def randomArray(self, arr, length = 1):
        rand_arr = []
        
        tmp_population = [x for x in arr]
        while len(tmp_population) > 0 and len(rand_arr) < length:
            i = random.randint(0, len(tmp_population)-1)
            val = tmp_population[i]
            del tmp_population[i]
            rand_arr.append(val)
        return rand_arr

    def saveModel(self, model, name):
        path = "storage/models/"+name+".pkl"
        file = open(path, 'wb')
        pickle.dump(model, file)
        file.close()
        return path
    
    def saveGeneration(self, index = None):
        if(index):
            data = self.generation[index]
            path = "storage/generations/"+str(index)+".pkl"
        else:
            data = self.generation
            path = "storage/generation-all.pkl"
        file = open(path, 'wb')
        pickle.dump(data, file)
        file.close()
        return path
        
    def loadGeneration(self, index = None):
        if(index):
            path = "storage/generations/"+str(index)+".pkl"
        else:
            path = "storage/generation-all.pkl"
        if not os.path.isfile(path):
            return None
        file = open(path, 'rb')# open a file, where you stored the pickled data
        data = pickle.load(file)
        file.close()
        return data

    #Inisiasi generasi pertama
    def setFirstGeneration(self, backup = True, restore = False):
        self.generation = []
        self.population = []
        if restore:
            self.generation = [self.loadGeneration()[0]]
            self.population = self.generation[0]
            return
        for i in range(self.number_of_population):
            individu = self.createIndividu([
                random.randint(self.min_gen, self.max_gen),
                random.randint(self.min_gen, self.max_gen),
                random.randint(self.min_gen, self.max_gen),
                random.randint(self.min_gen, self.max_gen),
                random.randint(self.min_gen, self.max_gen)
            ])
            self.setFitness(individu)
            self.population.append(individu)
        self.generation.append(self.population)
        if backup:
            self.saveGeneration()

    #membuat fungsi fitness
    def fitness(self, f):
        self.fitness_func = f
        def decorator():
            return self.fitness_func
        return decorator

    #inisiasi random populasi
    def addPopulation(self, individu):
        # individu = [hl1, hl2, hl3, hl4, hl5]
        # hl1 = jumlah hl1
        self.population.append({
            "kromosom": individu,
            "fitness": self.fitness_func(individu),
            "isMarried": False
        })

    #inisiasi individu
    def createIndividu(self, individu, parents = None):
        return {
            "kromosom": individu,
            "model": None,
            "fitness": 0,
            "isMarried": False,
            "parents": parents
        }
        
    def selection(self):
        mates = []
        tmp_population = self.population.copy()
        
        # cari yang fitness paling tinggi. DIA GK BOLEH KAWIN
        i_great = 0
        for i in range(1, len(tmp_population)):
            if tmp_population[i]["fitness"] > tmp_population[i_great]["fitness"]:
                i_great = i
        del tmp_population[i_great]

        while len(tmp_population) > 1:
            i = random.randint(0, len(tmp_population)-1)
            ind_1 = tmp_population[i]
            ind_1["isMarried"] = True
            del tmp_population[i]
            
            i = random.randint(0, len(tmp_population)-1)
            ind_2 = tmp_population[i]
            ind_2["isMarried"] = True
            del tmp_population[i]
            
            mates.append((ind_1, ind_2, ))
        return mates

    # membuaat fungsi umtuk crossover/kawin silang
    def crossOverSinglePoint(self, parent1, parent2):
        # parent1 = [hl1, hl2, hl3, hl4, hl5]
        # parent2 = [hl1, hl2, hl3, hl4, hl5]
        p1 = parent1["kromosom"]
        p2 = parent2["kromosom"]
        point = random.randint(1, 4)
        child1 = self.createIndividu([], (p1, p2))
        child2 = self.createIndividu([], (p1, p2))
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
        
        child1 = self.createIndividu([], (p1, p2))
        child2 = self.createIndividu([], (p1, p2))
        for i in range(length_kromosom):
            if i in random_index:
                avg = round((p1[i] + p2[i])/2)
                child1["kromosom"].append(avg)
                child2["kromosom"].append(avg)
            else:
                child1["kromosom"].append(p1[i])
                child2["kromosom"].append(p2[i])
        return child1, child2

    def setFitness(self, individu):
        self.fitness_func(individu)

    def mutation(self, individu, rate = 0.2):
        kromosom = individu["kromosom"]
        length_kromosom = len(kromosom)
        number_of_mut_gen = round(length_kromosom * rate)
        random_index = self.randomArray(range(length_kromosom), length=number_of_mut_gen)

        for i in random_index:
            mut = random.randint(-10, 10)
            kromosom[i] += mut
            if kromosom[i] > self.max_gen:
                kromosom[i] = self.max_gen
            if kromosom[i] < self.min_gen:
                kromosom[i] = self.min_gen

    def etilsmReplacement(self):
        # get 
    
    #membuat generasi selanjutnya sampai ke-n
    def newGeneration(self):
        self.newGen = []
        # cari jodoh : select from population
        mates = self.selection()
        for parent1, parent2 in mates:
            print("crossing over >", parent1["kromosom"], parent2["kromosom"])
            child1, child2 = self.crossOverAvg(parent1, parent2)

            # mutasi
            self.mutation(child1, rate=0.2)
            self.mutation(child2, rate=0.2)
            print("children >", child1["kromosom"], child2["kromosom"])
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