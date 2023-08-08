local full_fadeout_delay = 19
local warp_active = 0
function full_black_fadeout()
    warp_active = Memory.read("transition_type")
    if warp_active ~= 0 then
        if full_fadeout_delay == 0 then
            -- Reset delay
            full_fadeout_delay = 19
            return true
        end
        if memory.readbyte(Memory.MEMORY["transition_type"].address + 1) == 0xB then
            full_fadeout_delay = full_fadeout_delay - 1
        end
    end
    return false
end
function first_visible_frame()
    if Memory.read("action") == "stop teleporting" then return true end
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