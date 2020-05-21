
dicta = {'cdg':['nyc', 'lax', 'syd', 'fra'], 'fra':['chc', 'akl', 'mel','tlv', 'cdg', 'tyu'], 'tlv': ['cdg', 'fra', 'per'], 'ams':['lhr', 'mad'], 'tyu':['lhr', 'nml']}

def look(lst, end, p):
  if len(lst) == 1:
    ad = [[lst[0], e] if e is not end else print([lst[0], e]) for e in dicta[lst[0]]]
    look(ad, end, 0)
  else:
    # q = [a[-1] for a in lst]
    q = {s for a in lst for s in a}
    n = []
    for i in range(len(lst)):
      try:
        ls = (set(dicta[lst[i][-1]]).difference(q))    
        for x in ls:
          if x == end:
            print(lst[i]+[x])
            p += 1
          n.append(lst[i]+[x])
      except:
        pass
    if p != 1:
      look(n, end, p)

    
look(['tlv'], 'lhr',0)
