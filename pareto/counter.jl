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