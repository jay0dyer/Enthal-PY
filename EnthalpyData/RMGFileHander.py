from RMGEntryProcesser import RequiredDataEntry

class RMGFileProcesser():
    def __init__(self):
        self.loaded_entries = []

    def build_environment(self):
        global R, ReferenceTemperature
        R = 8.314462618e-3
        ReferenceTemperature = 298.15

        def ThermoData(H298, **kwargs): return H298

        def NASAPolynomial(coeffs, **kwargs):
            Enthalpy_Of_Formation = sum([
                coeffs[0],
                (coeffs[1] / 2) * ReferenceTemperature,
                (coeffs[2] / 3) * (ReferenceTemperature ** 2),
                (coeffs[3] / 4) * (ReferenceTemperature ** 3),
                (coeffs[4] / 5) * (ReferenceTemperature ** 4),
                coeffs[5] / ReferenceTemperature
            ]) * R * ReferenceTemperature
            return Enthalpy_Of_Formation

        def NASA(polynomials, **kwargs):
            return polynomials[0]

        def entry_interceptor(**kwargs):
            parsed_entry = RequiredDataEntry(**kwargs)
            self.loaded_entries.append(parsed_entry)

        # Map the names in the data file to our interceptors
        return {
            'entry': entry_interceptor,
            'NASA':NASA,
            'NASAPolynomial':NASAPolynomial
        }

    def process_file(self, file_path):
        with open(file_path, "r") as file:
            env = self.build_environment()
            exec(file.read(), env)

    def get_data(self):
        return self.loaded_entries

parser = RMGFileProcesser()
parser.process_file("RawData/FromRMG/SMILES/CHON_G4.py")
for entry in parser.get_data():
    print(entry.returnInfo())
