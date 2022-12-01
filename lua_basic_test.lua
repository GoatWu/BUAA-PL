print('Hello lua!')

--this is a comment

function max(a, b)
    if a > b then
        return a
    else
        return b
    end
end

x = 3

print('Result: ', max(x, 5) + 6 / 2)