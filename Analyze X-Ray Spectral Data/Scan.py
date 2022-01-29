class Scan:

    def __init__(self, path, nRow, nCol, minEnergy, maxEnergy): # -1 for unknown
        self.path = path
        self.allPixels = [[None for j in range(nCol)] for i in range(nRow)]
        self.minEnergy = minEnergy
        self.maxEnergy = maxEnergy
        self.stepNumber = -1
        if self.minEnergy == -1 or self.maxEnergy == -1:
            self.bool = False
        else: # True if the energy range is known
            self.bool = True
        self.text = None
        self.string = None

    def getText(self):
        return self.text

    def getString(self):
        return self.string

    def getPath(self):
        return self.path

    def getNRow(self):
        return len(self.allPixels)

    def getNCol(self):
        return len(self.allPixels[0])

    def getAllPixels(self):
        return self.allPixels

    def getEnergies(self):
        import numpy as np
        return list(np.arange(self.minEnergy, self.maxEnergy + self.stepNumber, self.stepNumber))

    def getMinEnergy(self):
        return self.minEnergy

    def getMaxEnergy(self):
        return self.maxEnergy

    def getStepNumber(self):
        return self.stepNumber

    def getBool(self):
        return self.bool

    def insertPixel(self, pixel, row, col, threshold):
        pixel.denoise(threshold)
        self.allPixels[row][col] = pixel
        if self.stepNumber == -1:
            n = len(pixel.getIntensities())
            if self.bool == False: # set temporary energy range
                self.minEnergy = 0
                self.maxEnergy = n-1
                self.stepNumber = 1
            else:
                self.stepNumber = float(self.maxEnergy-self.minEnergy)/(n-1)

    def getEnergyIndex(self, energy):
        n = (energy - self.minEnergy)/self.stepNumber
        if n % 1 == 0:
            return int(n),-1
        else:
            import math
            return int(math.floor(n)),int(math.ceil(n))

    def getIntensitiesAtEnergy(self, energy):
        energy = round(energy, 4)
        if energy >= self.minEnergy and energy <= self.maxEnergy:
            nRow = self.getNRow()
            nCol = self.getNCol()
            intensities = [[None for j in range(nCol)] for i in range(nRow)]
            index1, index2 = self.getEnergyIndex(energy)
            if index2 == -1:
                for i in range(0, nRow):
                    for j in range(0, nCol):
                        intensities[i][j] = self.allPixels[i][j].getIntensities()[index1]
            else:
                temp = round((energy - (index1 * self.stepNumber + self.minEnergy)) / self.stepNumber,10)
                from fractions import Fraction as frac
                denominator = frac(str(temp)).denominator
                energies = self.getEnergies()
                from scipy.interpolate import make_interp_spline # spline
                import numpy as np
                list_x_new = list(np.round(np.linspace(energies[0], energies[-1], denominator * (len(energies) - 1) + 1), 4))
                for i in range(0, nRow):
                    for j in range(0, nCol):
                        list_y_smooth = make_interp_spline(energies, self.allPixels[i][j].getIntensities())(list_x_new)
                        intensities[i][j] = list_y_smooth[list_x_new.index(energy)]
            return intensities
        else:
            return []

    def plotIntensitiesAtEnergy(self, energy):
        self.text = None
        intensities = self.getIntensitiesAtEnergy(energy)
        if intensities != []:
            import matplotlib.pyplot as plt
            fig, ax = plt.subplots()
            p = ax.imshow(intensities)
            cb = plt.colorbar(p, shrink=0.5)
            ax.set_xlabel('Column')
            ax.set_ylabel('Row')
            cb.set_label('Intensity')
            plt.title("Intensities at " + str(energy)+"eV")
            self.string = self.path + "/" + str(energy) + "eV" + ".png"
            plt.savefig(self.string)
            plt.close(fig)
        else:
            self.text = "The energy entered is out of range."
            print(self.text)

    def getTotalIntensitiesInEnergyRange(self,startEnergy,endEnergy):
        startEnergy = round(startEnergy,4)
        endEnergy = round(endEnergy,4)
        self.text = None
        if endEnergy < self.minEnergy or startEnergy == self.maxEnergy:
            self.text = "The energies entered are out of range."
            return []
        else:
            if startEnergy == endEnergy or startEnergy == self.maxEnergy or endEnergy == self.minEnergy:
                self.text = "Invalid inputs since the overlap of this energy range and the range from the minimum energy to the maximum energy has width 0."
                return []
            else:
                if startEnergy < self.minEnergy:
                    startEnergy = self.minEnergy
                if endEnergy > self.maxEnergy:
                    endEnergy = self.maxEnergy
                index1s, index2s = self.getEnergyIndex(startEnergy)
                index1e, index2e = self.getEnergyIndex(endEnergy)
                nRow = self.getNRow()
                nCol = self.getNCol()
                total = [[None for j in range(nCol)] for i in range(nRow)]
                if index2s == -1 and index2e == -1:
                    energies = self.getEnergies()[index1s:index1e + 1]
                    for i in range(0, nRow):
                        for j in range(0, nCol):
                            intensities = self.allPixels[i][j].getIntensities()[index1s:index1e + 1]
                            import numpy as np
                            total[i][j] = np.trapz(intensities, energies)
                else:
                    from fractions import Fraction as frac
                    if index2s != -1:
                        temp = round((startEnergy - (index1s * self.stepNumber + self.minEnergy)) / self.stepNumber,10)
                        denominator1 = frac(str(temp)).denominator
                    else:
                        denominator1 = 0
                    if index2e != -1:
                        temp = round((endEnergy - (index1e * self.stepNumber + self.minEnergy)) / self.stepNumber,10)
                        denominator2 = frac(str(temp)).denominator
                        energies = self.getEnergies()[index1s:index2e + 1]
                    else:
                        denominator2 = 0
                        energies = self.getEnergies()[index1s:index1e + 1]
                    if denominator1 != 0 and denominator2 != 0:
                        denominator = denominator1
                        while denominator % denominator2 != 0:
                            denominator = denominator + denominator1
                    else:
                        denominator = max(denominator1, denominator2)
                    from scipy.interpolate import make_interp_spline # spline
                    import numpy as np
                    list_x_new = list(
                        np.round(np.linspace(energies[0], energies[-1], denominator * (len(energies) - 1) + 1), 4))
                    indexs = list_x_new.index(startEnergy)
                    indexe = list_x_new.index(endEnergy)
                    final_energies = list_x_new[indexs:indexe + 1]
                    for i in range(0, nRow):
                        for j in range(0, nCol):
                            if index2e != -1:
                                intensities = self.allPixels[i][j].getIntensities()[index1s:index2e + 1]
                            else:
                                intensities = self.allPixels[i][j].getIntensities()[index1s:index1e + 1]
                            list_y_smooth = make_interp_spline(energies, intensities)(list_x_new)
                            final_intensities = list_y_smooth[indexs:indexe + 1]
                            total[i][j] = np.trapz(final_intensities, final_energies)
                return total

    def plotTotalIntensitiesInEnergyRange(self, startEnergy, endEnergy):
        total = self.getTotalIntensitiesInEnergyRange(startEnergy, endEnergy)
        if total != []:
            import matplotlib.pyplot as plt
            fig, ax = plt.subplots()
            p = ax.imshow(total)
            cb = plt.colorbar(p, shrink=0.5)
            ax.set_xlabel('Column')
            ax.set_ylabel('Row')
            cb.set_label('Total Intensity')
            plt.title("Total Intensities in the Energy Range Between " + str(startEnergy) + "eV and " + str(endEnergy) + "eV")
            self.string = self.path + "/" + str(startEnergy) + "eV_" + str(endEnergy) + "eV" + ".png"
            plt.savefig(self.string)
            plt.close(fig)

        else:
            print(self.text)

    def updateEnergyRange(self, minEnergy, maxEnergy):
        bool = False
        while bool == False:
            try:
                minEnergy = float(minEnergy)
                maxEnergy = float(maxEnergy)
                if minEnergy < maxEnergy and minEnergy >= 0:
                    bool == True
                else:
                    print("Invalid energy range.")
                    minEnergy = input("Enter minimum energy: ")
                    maxEnergy = input("Enter maximum energy: ")
            except:
                print("Invalid energy range.")
                minEnergy = input("Enter minimum energy: ")
                maxEnergy = input("Enter maximum energy: ")
        self.minEnergy = minEnergy
        self.maxEnergy = maxEnergy
        self.stepNumber = float(self.maxEnergy - self.minEnergy) / (len(self.allPixels[0][0].getIntensities()) - 1)
        self.bool = True
