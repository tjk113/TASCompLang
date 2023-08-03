course:
    sl

start:
    action = "standing"

end:
    coin_count = 14
    action = "disappeared"

require:
    action_count "wall kick air" <= 3
    action_count "sideflip" <= 3
    action_count "long jump" <= 3