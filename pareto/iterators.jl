struct GroupIterator2
    options::Array{Int,1}  # list of possible group sizes
    k::Int  # number of categories
end
function Base.iterate(iter::GroupIterator2, state::Int=0)
    state >= length(iter.options)^iter.k && return nothing
    k = iter.k
    o = length(iter.options)
    alloc = zeros(Int, k)
    temp = 1
    for i in k:-1:1
        @inbounds alloc[i] = iter.options[state ÷ temp % o + 1]
        temp *= o
    end
    return alloc, state+1
end
Base.length(iter::GroupIterator2) = length(iter.options)^iter.k
Base.eltype(::Type{GroupIterator2}) = Array{Int,1}


struct GroupIterator
    options::Array{Int,1}
    k::Int  # number of categories
end
function Base.iterate(iter::GroupIterator)
    state = ones(Int, iter.k)
    item = map(i->iter.options[i], state)
    return item, (item, state)
end
function Base.iterate(iter::GroupIterator, state)
    state === nothing && return nothing
    _giterate(iter, state) === nothing && return nothing
    return copy(state[1]), state
end
function _giterate(iter::GroupIterator, next, i::Int=1)
    i > iter.k && return nothing
    item, state = next
    @inbounds state[i] += 1
    if state[i] > length(iter.options)  # carry over
        out = _giterate(iter, next, i+1)
        out === nothing && return nothing
        @inbounds state[i] = 1  # reset
    end
    @inbounds item[i] = iter.options[state[i]]
    return true
end
Base.length(iter::GroupIterator) = length(iter.options)^iter.k
Base.eltype(::Type{GroupIterator}) = Array{Int,1}
Base.firstindex(::GroupIterator) = 1

struct TestIterator
    budget::Int
    step::Int
    lower::Vector{Int}
    upper::Vector{Int}
    k::Int  # number of categories
end
function Base.iterate(iter::TestIterator)
    k = iter.k
    t = copy(iter.lower)
    t[k] = iter.budget - sum(t[1:end-1])
    while !(iter.lower[k] <= t[k] <= iter.upper[k])
        !_titerate(iter, t) && return nothing
    end
    return t, t
end
function Base.iterate(iter::TestIterator, t)
    t === nothing && return nothing
    k = iter.k
    !_titerate(iter, t) && return nothing
    while !(iter.lower[k] <= t[k] <= iter.upper[k])
        !_titerate(iter, t) && return nothing
    end
    return t, t
end
"""Iterates to next element. Returns false if spent, true otherwise."""
function _titerate(iter::TestIterator, t)
    # Invariant: t[k] always contains remaining budget
    k = iter.k
    i = k-1
    while i >= 1 && (t[i] >= iter.upper[i] || t[k] < 0)
        # Reset allocation to category i
        t[k] += t[i] - iter.lower[i]  # reclaim budget
        t[i] = iter.lower[i]
        i -= 1
    end
    i === 0 && return false
    t[i] += iter.step
    t[k] -= iter.step
    return true
end
Base.eltype(::Type{TestIterator}) = Vector{Int}
Base.firstindex(::TestIterator) = 1