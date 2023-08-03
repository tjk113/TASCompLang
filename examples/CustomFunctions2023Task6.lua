local MEDIAN_WATER_LEVEL_ADDRESS = 0x8036118A
local water_level = memory.readdword(MEDIAN_WATER_LEVEL_ADDRESS)
local last_water_level = 9999
local touched_crystals = 0
local water_lowering = false

function crystal_handler()
    water_level = memory.readword(MEDIAN_WATER_LEVEL_ADDRESS)
    -- Don't allow water level to increase
    if water_level > last_water_level then
        DQ("Activated crystals out of descending order")
        return false
    -- Median water level decreases by 10 units each frame of lowering
    elseif water_level == last_water_level - 10 and not water_lowering then
        touched_crystals = touched_crystals + 1
        print('touched crystal ' .. touched_crystals)
        water_lowering = true
    elseif water_level == last_water_level then
        water_lowering = false
    end
    last_water_level = water_level

    return true
end

function touched_all_crystals()
    return touched_crystals == 4
end