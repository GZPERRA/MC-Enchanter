def p(pwp):
    """Calculates XP cost for the prior work penalty (pwp)"""
    #https://minecraft.gamepedia.com/Anvil/Mechanics#Prior_work_penalty
    return pow(2, pwp)-1
