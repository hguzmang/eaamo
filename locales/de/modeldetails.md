## Model Details
Mathematical details of our model are provided [here](assets/companion.pdf).  You
can also review [our website](https://www.testandcontain.com) for an introduction
and historical information about this project.

In this section we describe briefly the model parameters and we give
general explanation of the computation of results.

### Parameters
#### University Population
We assume there are 500 professors, 500 cafeteria staff and 9000
students. Moreover, we have 500 Covid-19 tests available, which can be
pooled into groups of sizes 1, 3, 5 or 10.

#### Connectivity
The following table captures the quantity of people interaction between
different categories of the population. For example, students are often
in contact with professors through teaching, but they also visit the
university's cafeterias regularly. This might result in one student
interacts with 50 professors and 100 members of the cafeteria staff. 
Similarly, one professor might interact with
fewer cafeteria staff member but many more students.


| Connectivity  | Professors    | Cafeteria staff | Students |
| ---------------:| -------------:|----------------:| --------:|
| Professors      |      10       |       20        |     180  |
| Cafeteria staff |      14       |       10        |     200  |
| Students        |      50       |       100       |      40  |



#### Infection rates
Having been in close contact with people is not enough for an
infection to occur automatically. Depending on the nature of their
interaction and each category's individual characteristics, we use
potentially different infection rates for each pair. For example, a
professor can be infected by 20 people of the cafeteria staff (as per
the previous table), each of which, if they are positive, could
transfer the disease with 2% probability.

| Infection rates  | Professors    | Cafeteria staff | Students |
| ---------------:| -------------:|----------------:| --------:|
| Professors      |      1%       |       2%        |     5%  |
| Cafeteria staff |      1%       |       2%        |     5%  |
| Students        |      1%       |       2%        |     5%  |



#### Vulnerability
Once infected, each category has different rates of getting a serious illness. We used the rates in the following table.

|  Categories     | Professors    | Cafeteria staff | Students |
| ---------------:| -------------:|----------------:| --------:|
|  Vulnerability  |      60%      |       40%       |      20% |


### Computation of results
The solutions you are exploring have been carefully selected using the
Test and Contain algorithm. In particular, our mechanism ensures that
no solution you see is better in all objectives than another.

The group sizes for each test are already limited to 1, 3, 5 or 10
people in each group (derived from typical group sizes in pool
testing). For the actual number of tests allocated to each category
we consider multiples of 10 until the maximum number of tests is
reached (i.e. 1, 10, 20, 30, ..., 500). 

To evaluate each testing plan, we generate all valid combinations of
group sizes and tests per category, ensuring that the testing budget
is exhausted and no person is tested more than once. After that, the
algorithm takes into account the parameters defined in the preceding tabels 
and computes the following objectives:

- The number of prevented infections.
- The number of unnecessary self-isolations in each category *separately*.

For this particular example, the quality of a testing plan is
expressed by 4 numbers: the expected number of prevented infections as
well as the number of people in unnecessary quarantine from each of
the 3 categories. These solutions are then sorted by the number of
prevented infections and filtered, so the only ones that remain are
pareto *optimal*, which just means that they cannot be improved upon
in every aspect.
