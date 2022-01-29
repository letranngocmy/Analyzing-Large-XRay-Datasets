class Pixel:

  def __init__(self, intensities):
    self.intensities = intensities

  def getIntensities(self):
    return self.intensities

  def denoise(self, threshold):
    for i in range(0,len(self.intensities)):
      if self.intensities[i] < threshold:
        self.intensities[i] = 0
