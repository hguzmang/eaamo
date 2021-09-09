#=
MIT License

Optimal Testing and Containment Strategies for Universities in Mexico amid COVID-19

Copyright © 2021 Test and Contain. Luis Benavides-Vázquez, Héctor Alonso Guzmán-Gutiérrez, Jakob Jonnerby, Philip Lazos, Edwin Lock, Francisco J. Marmolejo-Cossío, Ninad Rajgopal,and José Roberto Tello-Ayala. https://www.testandcontain.com/

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
=#
using DataFrames
using CSV

include("frontier.jl")

function ranges(pop, config)
    k = length(pop.p)
    prealloc = preallocate(k)
    budget, step, guaranteed = config.budget, config.stepsize, config.guaranteed
    gsize = config.groupsizes
    mins = fill(Inf, k+1)
    maxes = fill(-Inf, k+1)
    do_nothing = critical(pop, prealloc, ones(Int, k), zeros(Int, k))
    @showprogress for groups in GroupIterator(gsize, k)
        for tests in TestIterator(budget, step, guaranteed, pop.n .÷ groups, k)
            objectives!(pop, prealloc, groups, tests, do_nothing)
            for i in 1:k+1
                mins[i] = min(mins[i], prealloc.obj[i])
                maxes[i] = max(maxes[i], prealloc.obj[i])
            end
        end
    end
    return mins, maxes
end

"""Compute the frontier, loading parameters from `filename` file."""
function compute(filename, nobuckets=false, buckets=nothing)
    pop, config = load_from_json(filename)
    if buckets != nothing
        config.bucketsizes = buckets
    end
    solutions = frontier(pop, config, nobuckets)
    return solutions
end


function run()
    # Process commandline arguments
    if length(ARGS) === 0
        println("Please specify the input data file. Optionally, specify an output file as a second argument.")
        println("\nUsage: run `julia path/to/data.json [path/to/output.csv]` in the terminal.")
        return
    end
    input = ARGS[1]
    n = parse(Int32, ARGS[2])
    output = length(ARGS)==3 ? ARGS[3] : nothing
    pop, config = load_from_json(input)

    k = length(pop.p) # number of categories
    total_sol = 3k+1

    # Creates initial bucket with the variance of each objective
    mins, maxes = ranges(pop,config)
    buckets_var = maxes - mins

    # Sets lower and uper bounds for binary search (interval [0,1])
    ubound = 1.0
    lbound = 0.0

    solutions_no = Solutions()
    matrix_no = hcat(solutions_no...)'
    buckets = buckets_var
    # Iterates ten times by checking number of solution in each run of compute
    for i in 1:10
        α = (ubound + lbound)/2
        buckets = α * buckets_var
        solutions_no = compute(input, false, buckets)
        matrix_no = hcat(solutions_no...)'
        total_sol = size(matrix_no, 1)
        if total_sol > n
            lbound = α
        else
            ubound = α
        end
    end
    print("Buckets")
    print(*)
    print(round.(buckets,digits=2))
    print(*)
    # Final solutions to print
    solutions = solutions_no
    matrix = matrix_no
    #

    header = [["g$i" for i in 1:k];
             ["t$i" for i in 1:k];
             ["h"];
             ["c$i" for i in 1:k]]
    df = DataFrame(matrix, header)  # TODO: make pretty table headings

    if output === nothing
        # Print solutions to terminal
        println(df)
        # Print some stats
        println("Solution stats per objective")
        println(describe(df[!, 2k+1:3k+1]))
    else
        # Save solutions to output filename
        CSV.write(output, df, writeheader=true)
    end


    return
end

run()
