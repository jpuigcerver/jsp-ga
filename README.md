jsp-ga
======

Job-shop Scheduling Problem using Genetic Algorithms.

Author: Joan Puigcerver i Pérez (joapuipe@upv.es)

Usage
-----

The program usage is straightforward:

```
$ python jsp.py jsp-instance.txt
```

The program will output the timespan of the best solution and the chromosome representation of the solution (a topological sort of the tasks).

jsp-ga has some options that can be configured to tune the performance / speed of the genetic algorithm.

```
$ python jsp.py
Usage: jsp.py [OPTIONS] <instance-file>
Options:
  -s <seed>           Random seed. Default: 0
  -p <population>     Population size. Default: 50
  -i <iterations>     Iterations. Default: 1000
  -c <crossover-prob> Crossover probability. Default: 1.000000
  -m <mutation-prob>  Mutation probability. Default: 0.100000
```

If you want to know more details about the genetic algorithm used, check the report article and do not hesitate contact me.