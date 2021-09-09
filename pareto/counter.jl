#=
MIT License

Optimal Testing and Containment Strategies for Universities in Mexico amid COVID-19

Copyright © 2021 Test and Contain. Luis Benavides-Vázquez, Héctor Alonso Guzmán-Gutiérrez, Jakob Jonnerby, Philip Lazos, Edwin Lock, Francisco J. Marmolejo-Cossío, Ninad Rajgopal,and José Roberto Tello-Ayala. https://www.testandcontain.com/

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
=#
include("frontier.jl")

function count(pop, config)
    k = length(pop.p)
    budget, step, guaranteed = config.budget, config.stepsize, config.guaranteed
    gsize, bsizes = config.groupsizes, config.bucketsizes
    solutions = Dict()
    s = [0 for i in 1:2k]  # preallocate memory for solution
    @showprogress for groups in GroupIterator(gsize, k)
        for tests in TestIterator(budget, step, guaranteed, pop.n .÷ groups, k)
            s[1:k] .= tests  # test portion
            s[k+1:2k] = [tests[i]===0 ? 0 : groups[i] for i in 1:k]  # group portion
            solutions[copy(s)] = true
        end
    end
    return length(solutions)
end


"""Count number of solutions, loading parameters from `filename` file."""
function compute(filename)
    pop, config = load_from_json(filename)
    return count(pop, config)
end


function run()
    # Process commandline arguments
    if length(ARGS) === 0
        println("Please specify the input data file.")
        println("\nUsage: run `julia path/to/data.json` in the terminal.")
        return
    end
    input = ARGS[1]

    # Compute solutions
    println("Number of solutions: ", compute(input))
    return
end

run()