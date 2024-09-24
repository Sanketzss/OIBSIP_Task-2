def pounds_to_kg(pounds):
    return pounds * 0.453592

def feet_inches_to_meters(feet, inches):
    return feet * 0.3048 + inches * 0.0254

def kg_to_pounds(kg):
    return kg / 0.453592

def meters_to_feet_inches(meters):
    feet = int(meters // 0.3048)
    inches = int((meters % 0.3048) / 0.0254)
    return feet, inches
