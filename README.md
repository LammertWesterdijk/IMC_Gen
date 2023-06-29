# IMC_Gen
Auto generates practice contests of varying difficulty. Problems are sourced from AIME, USAJMO, USAMO, IMO and Putnam and difficulty is ranked based on [AOPS difficulty estimation](https://artofproblemsolving.com/wiki/index.php/AoPS_Wiki:Competition_ratings). Likely difficulty of IMC is 6 - 10, but folders with practice tests of varying difficulty are included.

### Shortcomings
There are still several shortcomings of this generator. For one, problem types are not classified, and so the generator could come up with tests with only Number Theory problems, for instance. Secondly, the problem selection pool is relatively small, with several hard prominent contests missing, such as the Chinese TST. Also, the program can sometimes produce broken tests due to incorrect parsing, as problem formulations deviate a bit. In this case, simply rerun the program to try again.

### Blacklisting contests
There currently is no feature to blacklist certain contests for problem selection, for instance if you have already competed in an IMO in a specific year. Feel free to edit the contest selection code to exclude these contests.
