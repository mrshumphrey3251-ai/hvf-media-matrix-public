# -*- coding: utf-8 -*-
"""
Ebony Chronos Public Tactical Mesh Test Suite
Sanitized Interface Contract Tests for Open Source Builds
Redacted Implementation: Proprietary LPI/LPD hop tables and spread-spectrum parameters removed.
"""
import os
import sys
import unittest

REPO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
MESH_DIR = os.path.join(REPO_ROOT, "chronos_core", "mesh")
if MESH_DIR not in sys.path:
    sys.path.insert(0, MESH_DIR)

from chronos_mesh_network import (
    ChronosTacticalMeshEngine, MeshPacketType, MeshPacketEnvelope, NodePeerStatus
)

class TestChronosTacticalMeshPublic(unittest.TestCase):
    def setUp(self):
        self.engine = ChronosTacticalMeshEngine()

    def test_public_interface_contracts(self):
        # Peer registration contract
        self.engine.register_peer("PEER_01", -65.0, 1)
        self.assertIn("PEER_01", self.engine.peers)

        # Packet creation contract
        pkt = self.engine.create_packet(
            packet_type=MeshPacketType.EMERGENCY_SOS_BROADCAST,
            destination_node="BROADCAST",
            payload_data={"test": "data"}
        )
        self.assertIsInstance(pkt, MeshPacketEnvelope)
        self.assertEqual(pkt.packet_type, MeshPacketType.EMERGENCY_SOS_BROADCAST.value)

        # Packet receive contract
        res = self.engine.receive_packet(pkt)
        self.assertEqual(res["action"], "CONSUMED")

if __name__ == "__main__":
    unittest.main()
