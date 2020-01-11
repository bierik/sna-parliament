from seed import seed
from normalize import normalize
from network import generate_networks
from analyse import generate_analysis


# Get all data from lobbywatch.ch
seed()

# Normalize seeded data
normalize()

# Generate graph files
generate_networks()

# Generate anaysis
generate_analysis()
