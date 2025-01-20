course: bits

start:
    action != "stop teleporting"
    action != "standing"

end:
    coin_count >= 3
    action = "star dance ground (doesn't exit)"
