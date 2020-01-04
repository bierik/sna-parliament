from seed import seed
from normalize import normalize
from network import generate_networks


# Get all data from lobbywatch.ch
seed()

# Normalize seeded data
normalize()

# Generate graph files
generate_networks()
