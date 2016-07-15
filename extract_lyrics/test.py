from collections import defaultdict

def dictSum(*dicts):
    ret = defaultdict(int)
    for d in dicts:
        for k, v in d.items():
            ret[k][0] += v[0]
            ret[k][1] += v[1]
    return dict(ret)
    
finalDict = {}

tokens = ["Hugo", "Mariana", "Mariana", "hue"]

freqDict = defaultdict(int)
for token in tokens:
    if token in freqDict:
        freqDict[token][0] += 1
    else:
        freqDict[token] = [1,1]
        
finalDict = dictSum(finalDict, freqDict)
        
        
print(finalDict)
