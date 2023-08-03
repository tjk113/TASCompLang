course: wdw

start:
    action = "standing"

end:
    touched_all_crystals // custom function (see: CustomFunctions2023Task6.lua)
    action = "star dance ground (exits)"

require:
    crystal_handler // custom function

ban:
    blj
    c_up_slide