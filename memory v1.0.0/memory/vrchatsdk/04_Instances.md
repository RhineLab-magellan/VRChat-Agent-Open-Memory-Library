---
source: https://vrchat.community/instances
date: 2026-06-10
---

# Instances

Instances are parallel "rooms" or "lobbies" of a world. Each instance can only hold a limited number of users, but there is no limit on how many instances can exist of a world. Instances are uniquely identified by the combined World ID and Instance ID.

As of 2024-05-02, VRChat indicated in a Developer Update an eventual intent to replace the current system with a UUID-ish system similar to User IDs.

## Instance Generator

## Instance ID

The instance ID is the combined sum of all the arguments to the instance e.g. name, friends, hidden, private, canRequestInvite, region, nonce.

### Owner ID

Differentiate two concepts, "Instance Owner" and "Instance Master":

- **Instance Owner**: The creator of the instance, is permanent, and has permission to insta-kick users without having to go through the Voting system.
- **Instance Master**: The Photon sync master and is responsible for object syncing. Whoever has stayed in the instance the longest.

### Nonce

Nonce is the Cryptographic key used to lock non-public instances to prevent people from guessing the Instance ID. It is not included in the location of public instances, and is formatted as `nonce(key)` where key is the cryptographic key.

### Region

Region indicates the geographical location of the Photon servers used for the instance. Default: `us`

| Region | Hosted in | Token |
|--------|-----------|-------|
| USA, West | San José | us |
| USA, East | Washington D.C. | use |
| Europe | Amsterdam | eu |
| Japan | Tokyo | jp |

### Special Values

- `"traveling"` Indicates a user's client is travelling between instances (e.g., downloading world, synchronizing world state)
- Also can be `"traveling:traveling"`