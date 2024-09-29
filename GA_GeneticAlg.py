import random
from config import DATA_SIZE1, LATENCY_CS_FR, LATENCY_ED_FR, MAX_SIMULATION_TIME, NO_INSTRUCTIONS1, NORMAL_ALERTS, SLOT_TIME
from devices import Cloud, EdgeDevice, FogDevice, Job,logentry, cs,tt

N_CHROMOSOMES = 4
MAX_ITERATIONS = 20

class Chromosome  :
    def __init__(self,rs,jbs) :
        self.n_r = len(rs)
        self.n_j = len(jbs)
        self.rs = rs
        self.jbs = jbs
        self.tbl = [[0 for columns in range( self.n_r+1)] for rows in range(self.n_j)]
        self.LatencyFitnes = 0.                                                          
        self.randomInit()
#       self.printassignment()

    def printassignment(self):
        print(self.tbl)

    def copyfrom(self,p):
        self.LatencyFitnes = p.LatencyFitnes
        for i in range(self.n_j ):
            for  j in range(self.n_r+1):
                self.tbl[i][j] = p.tbl[i][j]         

    def Fitness(self):
        self.LatencyFitnes = 0.
        for i in range(self.n_j ):
            FR_ID = self.getRs(i)
            if FR_ID < len(self.rs):
                self.LatencyFitnes = self.LatencyFitnes + self.jbs[i].no_instructions / self.rs[FR_ID].cpu_speed + LATENCY_ED_FR
            else:
                self.LatencyFitnes = self.LatencyFitnes + self.jbs[i].no_instructions / cs.cpu_speed + LATENCY_CS_FR

    def getRs(self,j):
        for i in range (self.n_r + 1):
            if self.tbl[j][i] >0:
                return i
        return self.n_r
 
    def randomInit(self):
        no_tasks_assinged = 0
        fg_capacity = []
        for j in range(self.n_r):
            fg_capacity.append (self.rs[j].no_core)        
        for i in range(self.n_j ):
            for  j in range(self.n_r+1):
                #resource initialised with no job
                self.tbl[i][j] = 0
            dev = random.randrange(0, self.n_r, 1)
            if (0 < fg_capacity[dev]) :
                fg_capacity[dev]-=1
                self.tbl[i][dev] = 1
                no_tasks_assinged+=1       
            self.tbl[i][self.n_r] = 1 #assignment for cloud
        self.Fitness()

    #single point crossover
    def crossover(self,pt,p2):
        for i in range(pt,self.n_j ):
            for  j in range(self.n_r+1):
                #resource assigned according to parent-2
                self.tbl[i][j] = p2.tbl[i][j]
        self.Fitness()

    #The scramble mutation (SM) operator places the elements in a specified range of the individual solution
    #in a random order and checks whether the fitness value of the recently generated solution is improved or not
    #The place is randomly chosen from the given substring for displacement 
    #such that the resulting solution is valid as well as a random displacement mutation
    def mutation(self,p):        
        for r in range(self.n_r ):
            r_capacity = 0
            for j in range(self.n_j ):
                #resource assigned 
                r_capacity += self.tbl[j][r]
            if r_capacity > self.rs[r].no_core:
                over_r = r_capacity - self.rs[r].no_core
                self.adjust_to_lessloded(r,over_r)
        self.Fitness()
        if self.LatencyFitnes > p.LatencyFitnes:
            self.copyfrom(p)


    def adjust_to_lessloded(self,over_r, over_r_capacity):
        for r in range(self.n_r ):
            r_capacity = 0                           
            for j in range(self.n_j ):
                #resource assigned 
                r_capacity += self.tbl[j][r]
            if r_capacity < self.rs[r].no_core:
                les_r =  self.rs[r].no_core - r_capacity
                #adjust - resulting solution for valid
                adj = 0
                MaxAdj = over_r_capacity if over_r_capacity < les_r else les_r
                while adj < MaxAdj:
                    jb = random.randrange(0, self.n_j, 1)
                    if self.tbl[jb][over_r] > 0:
                        self.tbl[jb][over_r] = 0
                        self.tbl[jb][r] = 1
                        adj +=1
                over_r_capacity -= adj
        if over_r_capacity > 0:
        #unudjusted jobs should be moved to cloud        
            adj = 0
            while adj < over_r_capacity:
                jb = random.randrange(0, self.n_j, 1)
                if self.tbl[jb][over_r] > 0:
                    self.tbl[jb][over_r] = 0
                    adj +=1
                    print("Adjusted")


class GeneticAlgorithm:
    def __init__(self,rs,jbs) :
        self.rs = rs
        self.jbs = jbs

    # tournament selection
    def SeclectChromosomes(self, pop):
	# first random selection
        if len(pop) > 1:
            selection_ix = random.randint(0,len(pop)-1)
            for ix in range(0 , len(pop)-1, 3):
                # check if better (e.g. perform a tournament)
                if pop[ix].LatencyFitnes < pop[selection_ix].LatencyFitnes:
                    selection_ix = ix
            ret = pop[selection_ix]
            del pop[selection_ix]
        else:
            ret = pop[0]
        return ret

    #single point crossover - two parents to create two children
    def GA_crossover(self,p1, p2):
        # children are copies of parents by default
        c1 = Chromosome(self.rs, self.jbs)
        c2 = Chromosome(self.rs, self.jbs)
        c1.copyfrom(p1)
        c2.copyfrom(p2)
       
        # check for recombination
        # select crossover point that is not on the end of the string
        crossover_point = random.randrange(0, len(self.jbs)-1, 1)
#        print("crossover_point:"+ str(crossover_point))
        # perform crossover
#        c1.printassignment()
        c1.crossover(crossover_point,c2)
#        c1.printassignment()
#        c2.printassignment()
        c2.crossover(crossover_point,p1)
#        c2.printassignment()
        return [c1, c2]
    
    def GenarateOptomalChromosome(self):
        CRMs = []
        for i in range (N_CHROMOSOMES):
            ch =  Chromosome(self.rs, self.jbs)
            CRMs.append(ch)
        itr = 0
#        print ([CRMs[i].LatencyFitnes for i in range (N_CHROMOSOMES)])
        CRMs.sort(key=lambda Chromosome: Chromosome.LatencyFitnes)
        self.BESTCRM =  CRMs[0]
        while itr < MAX_ITERATIONS:
            itr += 1
            # select parents
            selected = [self.SeclectChromosomes(CRMs) for _ in range(N_CHROMOSOMES)]
#            print("selected:")
#            print ([selected[i].LatencyFitnes for i in range (N_CHROMOSOMES)])
            #print("selected-end:")
		    # create the next generation
            children = []
            for i in range(0, N_CHROMOSOMES-1, 2):
                # get selected parents in pairs
                p1, p2 = selected[i], selected[i+1]
                # crossover and mutation
                c= self.GA_crossover(p1, p2)
                # mutation
                c[0].mutation(p1)
                c[1].mutation(p2)
                # store for next generation
                children.append(c[0])
                children.append(c[1])          
            # replace population
            CRMs = children
            CRMs.sort(key=lambda Chromosome: Chromosome.LatencyFitnes)
#            print ([CRMs[i].LatencyFitnes for i in range (len(CRMs))])
#            print("BEST-IT"+str(itr))
#            CRMs[0].printassignment()
        self.BESTCRM =  CRMs[0]

    def returnBESTCRM(self):
        return self.BESTCRM
    