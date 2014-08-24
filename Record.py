import wave, struct
from math import pi, sin, cos

RATE = 44100
AMPLITUDE = 32767
def int_to_doub(i):
  return (1.0*i)/AMPLITUDE
def doub_to_int(doub):
  doub = max(-1.0, min(1.0, doub)) ## bound into [-1, 1]
  return doub*32767

class Record:
  def __init__(self, amps=[]):
    self.duration = float(len(amps))/RATE
    self.amps = amps
  def intensity_at(self, freq):
    sample_omega = 2*pi*freq / RATE
    integral_s = sum(self.amps[i] * sin(sample_omega*i) for i in range(len(self.amps))) / (self.duration*RATE/2)
    integral_c = sum(self.amps[i] * cos(sample_omega*i) for i in range(len(self.amps))) / (self.duration*RATE/2)
    return integral_s**2 + integral_c**2
  def sub(self, start, end):
    sample_start, sample_end = int(start*RATE), int(end*RATE)
    return Record(self.amps[sample_start:sample_end])
  def read_from(self, filename):
    ''' THX to http://stackoverflow.com/questions/2060628/how-to-read-wav-file-in-python '''
    self.amps = []
    wav_file = wave.open(filename, 'r')
    for i in range(wav_file.getnframes()):
      next_frame = wav_file.readframes(1)
      value = int(struct.unpack('h', next_frame)[0])
      self.amps.append(int_to_doub(value))
    self.duration = float(len(self.amps))/RATE
  def write_to(self, filename):
    ''' THX to http://soledadpenades.com/2009/10/29/fastest-way-to-generate-wav-files-in-python-using-the-wave-module/ '''
    wav_file = wave.open(filename, 'w')
    wav_file.setparams((1, 2, RATE, 0, 'NONE', 'not compressed'))

    values = []
    for amp in self.amps:
      packed_value = struct.pack('h', doub_to_int(amp))
      values.append(packed_value)

    value_str = ''.join(values)
    wav_file.writeframes(value_str)
    
