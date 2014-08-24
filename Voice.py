import Record

R = Record.Record()
R.read_from('rec_ooh.wav')


def freq_search(record, lbound=20, ubound=2000, divs=5, layers=5):
  diff = float(ubound-lbound)/divs
  freqs = [lbound + (i+0.5)*diff for i in range(divs)] ## 0.5 to center the freqs
  c2, f = max((record.intensity_at(freq), freq) for freq in freqs)
  if layers==0:
    return abs(f)
  else:
    ## so range is 2/5 of previous range (so go over same space
    ## from many different "perspectives" (ways of slicing)):
    return freq_search(record, f-diff, f+diff, divs, layers-1)

def freqs(record, divs=90):
  diff = record.duration/divs
  for i in range(divs):
    t = diff*i
    S = record.sub(t, t+diff)
    print int(t*100)/100.0, '\t', freq_search(S, 20, 2000)
