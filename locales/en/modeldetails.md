### Computation of results
The solutions you are exploring have been carefully selected using the
algorithm. In particular, our mechanism ensures that
no solution you see is better in all objectives than another.

The group sizes for each test are already limited to 1, 3, 5 or 10
people in each group (derived from typical group sizes in pool
testing). 

To evaluate each testing plan, we generate all valid combinations of
group sizes and tests per category, ensuring that the testing budget
is exhausted and no person is tested more than once. After that, the
algorithm takes into account the parameters defined in the tabels 
and computes the following objectives:

- The number of prevented infections.
- The number of unnecessary self-isolations in each category *separately*.

For this particular example, the quality of a testing plan is
expressed by the expected number of prevented infections as
well as the number of people in unnecessary quarantine from each category. These solutions are then sorted by the number of
prevented infections and filtered, so the only ones that remain are
pareto *optimal*, which just means that they cannot be improved upon
in every aspect.


## Model Details
Mathematical details of our model are provided [here](assets/companion2.pdf). In this section we describe briefly the model parameters and we give
general explanation of the computation of results.

### Parameters

#### Connectivity
The following table captures the quantity of people interaction between
different categories of the population. For example, students are often
in contact with professors through teaching, but they also visit the
university's cafeterias regularly. See the conectivity table.


#### Infection rates
Having been in close contact with people is not enough for an
infection to occur automatically. Depending on the nature of their
interaction and each category's individual characteristics, we use
potentially different infection rates for each pair. See the co-infection table.


#### Vulnerability
Once infected, each category has different rates of getting a serious illness. In this case study, we consider that the vulnerability is 100% for all categories. 