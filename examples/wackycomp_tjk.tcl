course: bits

start:
    action != "standing"

end:
    coin_count >= 3
    action = "star dance ground (doesn't exit)"
