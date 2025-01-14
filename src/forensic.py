
class Forensic:
    def __init__(self):
        self.evidence = []
        
    def analyze_evidence(self, evidence_type):
        # Function to analyze forensic evidence
        if evidence_type == "fingerprint":
            return "Analyzing fingerprint evidence..."
        elif evidence_type == "dna":
            return "Processing DNA sample..."
        else:
            return f"Analyzing {evidence_type} evidence..."

def main():
    forensics = Forensic()
    result = forensics.analyze_evidence("fingerprint")
    print(result)

if __name__ == "__main__":
    main() 
