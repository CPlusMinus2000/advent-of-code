
OPERATORS = {
    [0] = function(a, b) return a == nil and b or a + b end,
    [1] = function(a, b) return a == nil and b or a * b end,
    [2] = function(a, b) return a == nil and b or math.min(a, b) end,
    [3] = function(a, b) return a == nil and b or math.max(a, b) end,
    [5] = function(a, b) return a > b and 1 or 0 end,
    [6] = function(a, b) return a < b and 1 or 0 end,
    [7] = function(a, b) return a == b and 1 or 0 end
}

-- Read from the file
function ReadFromFile(file)
    local f = io.open(file, "r")
    local t = f:read("*all")
    f:close()
    return t
end

-- Convert a number to a binary string
function BinaryText(val, length)
    local text = ""
    local size = 2 ^ (length - 1)
    while size > 0 do
        text = string.format("%d", val % 2) .. text
        val = val // 2
        if size == 1 then size = 0 end
        size = size / 2
    end
    return text
end

-- Converts the hexadecimal string to a binary string
function HexToBinary(hex)
    local binary = ""
    for i = 1, #hex do
        binary = binary .. BinaryText(tonumber(hex:sub(i, i), 16), 4)
    end
    return binary
end

-- read a packet recursively
function ReadPacket(packet, index)
    local versionbits = packet:sub(index, index + 2)
    local version = tonumber(versionbits, 2)
    local type = packet:sub(index + 3, index + 5)
    local length = 6
    if tonumber(type, 2) == 4 then
        -- packet containing constant
        local groupIndex = index + 1
        local groupValueString = ""
        repeat
            groupIndex = groupIndex + 5
            local group = packet:sub(groupIndex + 1, groupIndex + 4)
            groupValueString = groupValueString .. group
            length = length + 5
        until packet:sub(groupIndex, groupIndex) == "0"
        return length, version, tonumber(groupValueString, 2)
    else
        -- packet containing subpackets
        local lengthTypeID = packet:sub(index + 6, index + 6)
        local total = 0
        local value = nil
        local subs = {}
        if tonumber(lengthTypeID) == 0 then
            local lengthBitLength = tonumber(packet:sub(index + 7, index + 21), 2)
            index = index + 22
            length = length + 16
            while lengthBitLength > 0 do
                local packetLength, packetSum, packetValue = ReadPacket(packet, index)
                index = index + packetLength
                length = length + packetLength
                total = total + packetSum
                lengthBitLength = lengthBitLength - packetLength

                if tonumber(type, 2) < 5 then
                    value = OPERATORS[tonumber(type, 2)](value, packetValue)
                else
                    subs[#subs + 1] = packetValue
                end
            end
        else
            local numPackets = tonumber(packet:sub(index + 7, index + 17), 2)
            index = index + 18
            length = length + 12
            for i = 1, numPackets do
                local packetLength, packetSum, packetValue = ReadPacket(packet, index)
                index = index + packetLength
                length = length + packetLength
                total = total + packetSum

                if tonumber(type, 2) < 5 then
                    value = OPERATORS[tonumber(type, 2)](value, packetValue)
                else
                    subs[#subs + 1] = packetValue
                end
            end
        end

        if tonumber(type, 2) >= 5 then
            value = OPERATORS[tonumber(type, 2)](subs[1], subs[2])
        end

        return length, total + version, value
    end
end

function Solve(input)
    local decoded = HexToBinary(input)
    local ret, a, b = ReadPacket(decoded, 1)
    print(ret, a, b)
    return ret
end

-- print(Solve("D2FE28"))
-- Solve("38006F45291200") -- Length ID type 0
-- Solve("EE00D40C823060") -- Length ID type 1
-- Solve("8A004A801A8002F478")
-- Solve("620080001611562C8802118E34")
Solve("0054FEC8C54DC02295D5AE9B243D2F4FEA154493A43E0E60084E61CE802419A95E38958DE4F100B9708300466AB2AB7D80291DA471EB9110010328F820084D5742D2C8E600AC8DF3DBD486C010999B44CCDBD401C9BBCE3FD3DCA624652C400007FC97B113B8C4600A6002A33907E9C83ECB4F709FD51400B3002C4009202E9D00AF260290D400D70038400E7003C400A201B01400B401609C008201115003915002D002525003A6EB49C751ED114C013865800BFCA234E677512952E20040649A26DFA1C90087D600A8803F0CA1AC1F00042A3E41F8D31EE7C8D800FD97E43CCE401A9E802D377B5B751A95BCD3E574124017CF00341353E672A32E2D2356B9EE79088032AF005E7E8F33F47F95EC29AD3018038000864658471280010C8FD1D63C080390E61D44600092645366202933C9FA2F460095006E40008742A8E70F80010F8DF0AA264B331004C52B647D004E6EEF534C8600BCC93E802D38B5311AC7E7B02D804629DD034DFBB1E2D4E2ACBDE9F9FF8ED2F10099DE828803C7C0068E7B9A7D9EE69F263B7D427541200806582E49725CFA64240050A20043E25C148CC600F45C8E717C8010E84506E1F18023600A4D934DC379B9EC96B242402504A027006E200085C6B8D51200010F89913629A805925FBD3322191A1C45A9EACB4733FBC5631A210805315A7E3BC324BCE8573ACF3222600BCD6B3997E7430F004E37CED091401293BEAC2D138402496508873967A840E00E41E99DE6B9D3CCB5E3F9A69802B2368E7558056802E200D4458AF1180010A82B1520DB80212588014C009803B2A3134DD32706009498C600664200F4558630F840188E11EE3B200C292B59124AFF9AE6775ED8BE73D4FEEFFAD4CE7E72FFBB7BB49005FB3BEBFA84140096CD5FEDF048C011B004A5B327F96CC9E653C9060174EA0CF15CA0E4D044F9E4B6258A5065400D9B68")
Solve("020D74FCE27E600A78020200DC298F1070401C8EF1F21A4D6394F9F48F4C1C00E3003500C74602F0080B1720298C400B7002540095003DC00F601B98806351003D004F66011148039450025C00B2007024717AFB5FBC11A7E73AF60F660094E5793A4E811C0123CECED79104ECED791380069D2522B96A53A81286B18263F75A300526246F60094A6651429ADB3B0068937BCF31A009ADB4C289C9C66526014CB33CB81CB3649B849911803B2EB1327F3CFC60094B01CBB4B80351E66E26B2DD0530070401C82D182080803D1C627C330004320C43789C40192D002F93566A9AFE5967372B378001F525DDDCF0C010A00D440010E84D10A2D0803D1761045C9EA9D9802FE00ACF1448844E9C30078723101912594FEE9C9A548D57A5B8B04012F6002092845284D3301A8951C8C008973D30046136001B705A79BD400B9ECCFD30E3004E62BD56B004E465D911C8CBB2258B06009D802C00087C628C71C4001088C113E27C6B10064C01E86F042181002131EE26C5D20043E34C798246009E80293F9E530052A4910A7E87240195CC7C6340129A967EF9352CFDF0802059210972C977094281007664E206CD57292201349AA4943554D91C9CCBADB80232C6927DE5E92D7A10463005A4657D4597002BC9AF51A24A54B7B33A73E2CE005CBFB3B4A30052801F69DB4B08F3B6961024AD4B43E6B319AA020020F15E4B46E40282CCDBF8CA56802600084C788CB088401A8911C20ECC436C2401CED0048325CC7A7F8CAA912AC72B7024007F24B1F789C0F9EC8810090D801AB8803D11E34C3B00043E27C6989B2C52A01348E24B53531291C4FF4884C9C2C10401B8C9D2D875A0072E6FB75E92AC205CA0154CE7398FB0053DAC3F43295519C9AE080250E657410600BC9EAD9CA56001BF3CEF07A5194C013E00542462332DA4295680")
