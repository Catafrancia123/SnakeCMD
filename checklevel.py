def calculateBadge(level, proLevel):
    
    if level >= 69420:
        return "Meme based"
    elif level >= 5000:
        return "God of the game"
    elif level >= 1000:
        return "World Class"
    elif level >= 500:
        return "Master"
    elif level >= 100:
        return "Expert"
    elif level >= proLevel:
        return "Professional"
    elif level < proLevel:
        return ""
    else:
        return "Calculation error."