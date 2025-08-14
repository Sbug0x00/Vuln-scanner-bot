def load_targets(file_path):
    """Load targets from text file"""
    with open(file_path, 'r') as f:
        return [line.strip() for line in f.readlines() if line.strip()]

def save_results(data, file_path):
    """Save scan results"""
    with open(file_path, 'w') as f:
        json.dump(data, f, indent=2)
