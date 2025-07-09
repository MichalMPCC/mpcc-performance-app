def calculate_vo2max(power_5min, weight):
    return (power_5min * 10.8) / weight

def calculate_cp_wprime(p3, p12):
    cp = (p3 * 180 - p12 * 720) / (180 - 720)
    w_prime = 180 * (p3 - cp) / 1000
    return cp, w_prime

def estimate_fatmax(p5):
    return round(p5 * 0.55)

def estimate_vlamax(p15s, p1min):
    ratio = p15s / p1min
    if ratio > 1.8:
        return 0.7
    elif ratio > 1.6:
        return 0.6
    elif ratio > 1.4:
        return 0.5
    else:
        return 0.4

def fuel_split(power, cp):
    pct_cp = power / cp
    if pct_cp <= 0.55:
        fat = 85
    elif pct_cp <= 0.65:
        fat = 70
    elif pct_cp <= 0.75:
        fat = 50
    elif pct_cp <= 0.85:
        fat = 30
    elif pct_cp <= 1.0:
        fat = 15
    else:
        fat = 0
    return fat, 100 - fat
