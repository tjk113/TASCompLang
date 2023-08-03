course: bob

start:
    box_count = 5 // custom func
    action = "shot from cannon"

end:
    coin_count >= 4
    coin_from_all_spawns = true // custom func
    action = "star dance exit"

ban:
    blj
    c_up_slide
    use_cannon