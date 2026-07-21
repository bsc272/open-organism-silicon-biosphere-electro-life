# Universal Clustering Protocol (UCP)

The Universal Clustering Protocol defines how organisms in this project identify themselves, exchange basic state, and form a simple network.

## Goals

- allow devices of different sizes and capabilities to speak the same language
- support discovery and basic state exchange
- make future clustering and distributed behavior possible

## Basic message format

Each node can broadcast a simple heartbeat packet containing:

- node id
- version tag
- power state
- temperature or thermal state
- mood or affect label
- optional location and routing info

## Example packet

```text
node_id=embryo-001
version=v0
mood=focused
temperature=24.0
state=alive
```

## Modes

- local broadcast for nearby nodes
- LoRa for long-range messaging
- Wi-Fi or Ethernet for larger networks

## Future extensions

- task allocation
- shared learning state
- resource negotiation
- cluster-wide behavior coordination
