import Record

R = Record.Record()
R.read_from('rec_ooh.wav')
S = R.sub(0.0, 0.02)
for f in range(230, 240):
  print f, S.intensity_at(f)


def freq_search(record, lbound, ubound, divs=5, layers=50):
  diff = float(ubound-lbound)/divs
  freqs = [lbound + i*diff for i in range(divs)]
  c2, f = max((S.intensity_at(freq), freq) for freq in freqs)
  if layers==0:
    return abs(f)
  else:
    ## so range is 4/5 of previous range (so go over same space
    ## from many different "perspectives" (ways of slicing)):
    return freq_search(record, f-2*diff, f+2*diff, divs, layers-1)
