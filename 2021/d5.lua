
-- Read from the file
function read_from_file(file)
    local f = io.open(file, "r")
    local t = f:read("*all")
    f:close()
    return t
end

-- fill a table with point data from the file
function fill_table(file, table)
    local f = io.open(file, "r")
    for line in f:lines() do
        local x, y, a, b = line:match("(%d+),(%d+)%s.*%s(%d+),(%d+)")
        table[#table + 1] = {
            sx = tonumber(x),
            sy = tonumber(y),
            ex = tonumber(a),
            ey = tonumber(b)
        }
    end
    f:close()
end

function part1(file)
    local maxX, maxY = 0, 0
    -- find the max X and Y in the table
    table = {}
    fill_table(file, table)
    for i = 1, #table do
        maxX = math.max(maxX, table[i].sx, table[i].ex)
        maxY = math.max(maxY, table[i].sy, table[i].ey)
    end

    -- create a table of 0s
    local grid = {}
    for i = 0, maxY do
        grid[i] = {}
        for j = 0, maxX do
            grid[i][j] = 0
        end
    end

    -- fill out the lines
    for i = 1, #table do
        local signY = table[i].ey >= table[i].sy and 1 or -1
        local signX = table[i].ex >= table[i].sx and 1 or -1

        -- check that the line is v or h
        if table[i].sx == table[i].ex or table[i].sy == table[i].ey then
            for y = table[i].sy, table[i].ey, signY do
                for x = table[i].sx, table[i].ex, signX do
                    grid[y][x] = grid[y][x] + 1
                end
            end
        else
            -- calculate diagonals
            local x = table[i].sx
            local y = table[i].sy
            while x ~= table[i].ex + signX and y ~= table[i].ey + signY do
            -- for x = table[i].sx, table[i].ex + signX, signX do
                grid[y][x] = grid[y][x] + 1
                x = x + signX
                y = y + signY
            end
        end
    end

    -- count the number of more-than-one spots
    local count = 0
    for i = 0, maxY do
        for j = 0, maxX do
            if grid[i][j] > 1 then
                count = count + 1
            end
        end
    end

    return count
end

print(part1("inputs/d5.txt"))
