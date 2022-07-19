import unicodedata

print(unicodedata.east_asian_width("曾"))

def strWidth(chs):
    
    chLength = 0
    for ch in chs:
        if (unicodedata.east_asian_width(ch) in ('F','W','A')):
            chLength += 2
        else:
            chLength += 1
    
    return chLength

print(strWidth("曾剑锋"))
