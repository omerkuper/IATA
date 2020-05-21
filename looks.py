lst = [['tlv','cdg'], ['tlv', 'fra']]
dicta = {'cdg':['nyc', 'lax', 'ams', 'syd', 'fra'], 'fra':['chc', 'akl', 'mel','tlv', 'cdg']}

# q = [a[-1] for a in lst]
q = {s for a in lst for s in a}
n = []
for i in range(len(lst)):
  ls = (set(dicta[lst[i][-1]]).difference(q))
  for x in ls:
    n.append(lst[i]+[x])
print(n)
