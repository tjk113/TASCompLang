local delay = 19
local warp_active = 0
function full_black_fadeout()
    warp_active = Memory.read("transition_type")
    if warp_active ~= 0 then
        if delay == 0 then return true end
        if memory.readbyte(Memory.MEMORY["transition_type"].address + 1) == 0xB then
            delay = delay - 1
        end
    end
    return false
end
-- UNIMPLEMENTED
local has_wallkicked = false
function wallkick_before_each(object)
    if Memory.read("action") == "wall kick air" then
        has_wallkicked = true
    -- TODO: implement whatever check object.iteracted is
    elseif has_wallkicked and object.iteracted then
        has_wallkicked = false -- Reset if true
    elseif not has_wallkicked and object.iteracted then
        return false
    end
    return true
end
-- UNIMPLEMENTED
local last_interacted_object = nil
function alternate(object1, object2)
    local iteracting_object = object1.interacted and object1 or object2
    if last_interacted_object == iteracting_object then
        return false
    else
        last_interacted_object = iteracting_object
        return true
    end
end