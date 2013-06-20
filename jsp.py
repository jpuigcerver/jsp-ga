#!/usr/bin/env python
# -*- coding: utf-8 -*-

from random import randint, random, seed, shuffle
from sys import argv

# DEFAULT PARAMETERS
SEED = 0
PS = 50
IT = 1000
CP = 1.0
MP = 0.1

def LoadInstance(fname):
    f = open(fname, 'r')
    head = f.readline().split()
    n, m = int(head[0]), int(head[1])
    I = []
    for l in f:
        l = l.split()
        if len(l) < 3: continue
        ntasks = int(l[0])
        I.append([])
        for j in range(ntasks):
            mid = int(l[j*2+1])
            dur = int(l[j*2+2])
            I[-1].append((j, mid, dur))
    return I

def FormatGene(gene, I):
    ct = [0 for j in range(len(I))]
    sol = []
    for i in gene:
        tid = ct[i]
        mid = I[i][tid][1]
        dur = I[i][tid][2]
        sol.append((i, tid, mid, dur))
        ct[i] = ct[i] + 1
    return sol

def ComputeTimespan(s, I):
    # Build a DAG from the solution
    G = []
    for t in s: G.append([])
    G.append([])
    for i in range(1, len(s)):
        for j in range(i):
            if s[i][0] == s[j][0] and s[i][1] - 1 == s[j][1]:
                G[i].append(j)
            elif s[i][2] == s[j][2]:
                G[i].append(j)
        if s[i][1] + 1 == len(I[s[i][0]]):
            G[len(s)].append(i)
    # Compute the longest path in the DAG
    C = [0 for t in range(len(s)+1)]
    for i in range(len(s)+1):
        if len(G[i]) == 0:
            C[i] = 0
        else:
            C[i] = max(C[j] + s[j][3] for j in G[i])
    return C[len(s)]

def CrossOver(p1, p2, I):
    def Index(p1, I):
        ct = [0 for j in range(len(I))]
        s = []
        for i in p1:
            s.append((i, ct[i]))
            ct[i] = ct[i] + 1
        return s
    idx_p1 = Index(p1, I)
    idx_p2 = Index(p2, I)
    nj = len(I) # number of jobs
    nt = len(idx_p1) # total number of tasks
    i = randint(1, nt)
    j = randint(0, nt-1)
    k = randint(0, nt)
    implant = idx_p1[j:min(j+i,nt)] + idx_p1[:i - min(j+i,nt) + j]

    lft_child = idx_p2[:k]
    rgt_child = idx_p2[k:]
    for jt in implant:
        if jt in lft_child: lft_child.remove(jt)
        if jt in rgt_child: rgt_child.remove(jt)

    child = [ job for (job, task) in lft_child + implant + rgt_child ]
    return child

def Mutation(p):
    nt = len(p)
    i = randint(0, nt - 1)
    j = randint(0, nt - 1)
    m = [job for job in p]
    m[i], m[j] = m[j], m[i]
    return m


def Genetic(I, ps = 100, pc = 0.5, pm = 0.1, mit = 100):
    def InitPopulation(I, ps):
        """Generate initial population from random shuffles of the tasks"""
        gene = [j for j in range(len(I)) for t in I[j]]
        population = []
        for i in range(ps):
            shuffle(gene)
            population.append([j for j in gene])
        return population
    pop = [(ComputeTimespan(FormatGene(g, I), I), g) for g in InitPopulation(I, ps)]
    for it in range(1, mit+1):
        shuffle(pop)
        hpop = len(pop) / 2
        for i in range(hpop):
            if random() < pc:
                ch1 = CrossOver(pop[i][1], pop[hpop + i][1], I)
                ch2 = CrossOver(pop[hpop + i][1], pop[i][1], I)
                if random() < pm:
                    ch1 = Mutation(ch1)
                if random() < pm:
                    ch2 = Mutation(ch2)
                pop.append((ComputeTimespan(FormatGene(ch1, I), I), ch1))
                pop.append((ComputeTimespan(FormatGene(ch1, I), I), ch2))
        pop.sort()
        pop = pop[:ps]
    return pop[0]

def usage():
    print 'Usage: %s [OPTIONS] <instance-file>' % argv[0]
    print 'Options:'
    print '  -s <seed>           Random seed. Default: %d' % SEED
    print '  -p <population>     Population size. Default: %d' % PS
    print '  -i <iterations>     Iterations. Default: %d' % IT
    print '  -c <crossover-prob> Crossover probability. Default: %f' % CP
    print '  -m <mutation-prob>  Mutation probability. Default: %f' % MP

if len(argv) < 2:
    usage()
    exit(1)

i = 1
while i < len(argv) - 1:
    if argv[i] == '-s':
        SEED = int(argv[i+1])
    elif argv[i] == '-p':
        PS = int(argv[i+1])
    elif argv[i] == '-i':
        IT = int(argv[i+1])
    elif argv[i] == '-c':
        CP = float(argv[i+1])
    elif argv[i] == '-m':
        MP = float(argv[i+1])
    elif argv[i] == '-h':
        usage()
        exit(0)
    else:
        print 'Unknown option: %s' % argv[i]
        usage()
        exit(1)
    i = i + 2

seed(SEED)
I = LoadInstance(argv[-1])
(ts, g) = Genetic(I, ps=PS, mit=IT, pc=CP, pm=MP)
print ts, g

