using JSON

using ProgressMeter

include("iterators.jl")

struct Population
    n::Vector{Int}
    p::Vector{Float64}
    q::Vector{Float64}
    v::Vector{Float64}
    d::Array{Float64,2}
    π::Array{Float64,2}
end

mutable struct Config
    budget::Int  # number of tests available
    stepsize::Int  # size at which to bundle tests
    bucketsizes::Union{Nothing, Vector{Float64}}  # bucket size for all objectives (1 health + k quarantine)
    groupsizes::Vector{Int}
    guaranteed::Vector{Int}
end

Solutions = Vector{Vector{Float64}}  # for semantic convenience


"""Newer json reader, to ease automatization"""

function json_automatization(filename)
    data = JSON.parsefile(filename)

    info = data[1]["es"]
    populations = Array{Population}(undef, length(info))
    configs = Array{Config}(undef, length(info))
    file_names = Array{String}(undef, length(info))

    for campus in keys(info)
        n = [collect(values(i))[2] for i in values(info[campus]["categories"])]
        p = convert(Array{Float64, 1}, info[campus]["p"])
        v = convert(Array{Float64, 1}, info[campus]["v"])
        d = convert(Array{Float64, 2}, to_mat(info[campus]["d"]))
        π = convert(Array{Float64, 2}, to_mat(info[campus]["pi"]))
        q = 1 .- p
        populations[parse(Int,campus[7])] = Population(n, p, q, v, d, π)

        budget = info[campus]["budget"]
        stepsize = "stepsize" in keys(info[campus]) ? info[campus]["stepsize"] : 1
        groupsizes = "groupsizes" in keys(info[campus]) ? info[campus]["groupsizes"] : [1, 3, 5, 10]
        k = length(p)
        bucketsize = "bucketsizes" in keys(info[campus]) ? info[campus]["bucketsizes"] : nothing
        guaranteed = "guaranteed" in keys(info[campus]) ? info[campus]["guaranteed"] : zeros(k)
        configs[parse(Int,campus[7])] = Config(budget, stepsize, bucketsize, groupsizes, guaranteed)

        file_names[parse(Int,campus[7])] =  info[campus]["file"]
    end

    return populations, configs, file_names
end



"""Loads population and configuration data from json file."""
function load_from_json(filename)
    data = JSON.parsefile(filename)
    # load population
    n = convert(Array{Int, 1}, data["n"])
    p = convert(Array{Float64, 1}, data["p"])
    v = convert(Array{Float64, 1}, data["v"])
    d = convert(Array{Float64, 2}, to_mat(data["d"]))
    π = convert(Array{Float64, 2}, to_mat(data["pi"]))
    q = 1 .- p
    pop = Population(n, p, q, v, d, π)
    # load config
    budget = data["budget"]
    stepsize = data["stepsize"]
    bucketsize = "bucketsizes" in keys(data) ? data["bucketsizes"] : nothing
    groupsizes = data["groupsizes"]
    k = length(p)
    guaranteed = "guaranteed" in keys(data) ? data["guaranteed"] : zeros(k)
    config = Config(budget, stepsize, bucketsize, groupsizes, guaranteed)
    return pop, config
end
function to_mat(arrs) # for lists-of-lists parsed by JSON
    return Matrix(hcat(Vector{Float64}.(arrs)...)')
end


"""
Evaluate the health and quarantine objectives for given group sizes and number
of tests for each category.

NOTE: health objective is stored negated for simplicity.
"""
function objectives!(pop, prealloc, g, t, do_nothing)
    k = length(g)
    q = pop.q
    n = pop.n
    # Initialise objectives array
    prealloc.obj[1] = h_objective(pop, prealloc, g, t, do_nothing)
    prealloc.obj[2:end] = [q_objective(g[i], t[i], q[i], n[i]) for i in 1:k]
    return nothing
end


"""
Compute quarantine objective for a single category.

Note: Here q, t, q are numbers, not vectors.
"""
@inline q_objective(g, t, q, n) = (n==0 ? 0 : t*g*(q-q^g))


"""
Compute healthcare objective.

Note: the value is negated w.r.t. the IJCAI submission.
"""
@inline function h_objective(pop, prealloc, g, t, do_nothing)
    criticals = critical(pop, prealloc, g, t)
    return criticals - do_nothing
end


"""
Compute number of critical cases that occur when t tests of size g
are applied to each category.
"""
@inline function critical(pop, prealloc, g, t)
    n, p, q, v, π, d = pop.n, pop.p, pop.q, pop.v, pop.π, pop.d
    
    mask = (n.==0)
    n_to_divide = n
    n_to_divide = replace(n, 0=>1)

    z, temp = prealloc.z, prealloc.temp
    k = length(g)
    @. z = (n-t*g)*q/n_to_divide + t*g/n_to_divide*q^g
    @. temp = p*(n-t*g)/n_to_divide

    z[mask] .= 1
    temp[mask] .= 1

    @inbounds cases = sum(
        n[i]*v[i]*z[i]*(1-prod((1-π[i,j]*temp[j])^d[i,j] for j in 1:k))
            for i in 1:k)
    return cases
end


"""
Takes a single value or array and rounds each value to the nearest
multiple of bucketsize `bsize`. If no bucket size is provided, it returns
the original input.
"""
@inline function bucket(a, bsize=nothing)
    bsize === nothing && return a
    return round(a / bsize) * bsize
end


"""
Compute the Pareto frontier, output as an array.

Creates list of Pareto-optimal solutions, each consisting of a
Vector{Float64} with 3k+1 entries.
First 2k entries are for group sizes and number of tests.
Last k+1 entries are for health and quarantine objectives.

NOTE: The health objective is stored negated in order to simplify the code.
"""
function frontier(pop, config, nobuckets)
    k = length(pop.p)
    budget, step, guaranteed = config.budget, config.stepsize, config.guaranteed
    if nobuckets == true
        gsize, bsizes = config.groupsizes, nothing
    else
        gsize, bsizes = config.groupsizes, config.bucketsizes
    end
    solutions = Solutions()  # Create solutions list
    prealloc = preallocate(k)  # Preallocate memory
    # Compute number of critical cases if we apply no tests
    do_nothing = critical(pop, prealloc, ones(Int, k), zeros(Int, k))
    # Iterate over all possible solutions (groups, tests)
    @showprogress for groups in GroupIterator(gsize, k)
        for tests in TestIterator(budget, step, guaranteed, pop.n .÷ groups, k)
            objectives!(pop, prealloc, groups, tests, do_nothing)
            s = Float64[groups; tests; prealloc.obj]
            update!(solutions, s, bsizes)
        end
    end
    return solutions
end


"""
Given a new solution s, updates the list of solutions as follows.
If s is  by any solution in `solutions`, don't do anything.
Otherwise add s to `solutions` and remove all solutions s' in `solutions`
dominated by s.
"""
@inline function update!(solutions::Solutions, s::Vector{Float64}, bsizes=nothing)
    to_delete = Int[]  # collect solutions to be deleted
    for (i, other) in enumerate(solutions)
        # Check if sol dominates, or is dominated by, the current solution
        dominates, is_dominated = compare(s, other, bsizes)
        is_dominated && return nothing  # `s` is dominated by `other`
        dominates && push!(to_delete, i)  # store index for deletion
    end
    deleteat!(solutions, to_delete)  # delete all dominated solutions
    push!(solutions, s)  # add s to solutions
    return nothing
end


"""
Compares solutions `s` and `other` up to bucketing parameters (default=nothing).
Returns tuple (dominates, is_dominated) that expresses whether `s` dominates or
is_dominated by `other`.

NOTE: By default, function implements 'weak' dominance. This deviates from the
IJCAI paper, which stipulates that s dominates s' iff s[i] is strictly greater
than s'[i] for some i, and s[j] >= s[j] for all j.
Set `strong=true` to force `compare()` to follow the latter definition instead.
"""
@inline function compare(s, other, bsizes=nothing; strong=false)
    @assert length(s) === length(other)
    k = (length(s)-1) ÷ 3  # number of categories
    has_less, has_greater = false, false
    for i in 1:k+1
        bsize = bsizes===nothing ? nothing : bsizes[i]
        @inbounds comp = bucket(s[2k+i], bsize) - bucket(other[2k+i], bsize)
        if comp < 0
            has_less = true
        elseif comp > 0
            has_greater = true
        end
    end
    if !strong  # weak dominance parameter is true
        return !has_less, !has_greater
    else  # here we want to return truth values for strong dominance
        return !has_less && has_greater, !has_greater && has_less
    end
end


"""
Merges two solution lists into one. Specifically, it updates `solutions' to
contain the merged solutions and returns nothing.
"""
function merge!(solutions::Solutions, other::Solutions, bsizes=nothing)
    for s in other
        update!(solutions, s, bsizes)
    end
    return solutions
end


"""Preallocates memory for vectors that we compute frequently."""
function preallocate(k)
    s = zeros(Float64, 3k+1)  # new solution
    obj = zeros(k+1)  # objective of new solution
    z = zeros(Float64, k)
    temp = zeros(Float64, k)
    dominated = Int[]
    return (s=s, obj=obj, z=z, temp=temp, dominated=dominated)
end
