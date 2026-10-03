from locust import HttpUser, task, between

class HVFDroneSwarm(HttpUser):
    # Aggressive polling to simulate high-throughput swarm ingestion
    wait_time = between(0.01, 0.05)

    @task
    def send_drone_telemetry(self):
        payload = {
            "R": 120.0,
            "G": 150.0,
            "B": 80.0
        }
        # Target the GLI compute endpoint to stress-test the math engine
        with self.client.post("/compute", json=payload, catch_response=True) as response:
            if response.status_code == 200:
                response.success()
            else:
                response.failure(f"Failed! Status Code: {response.status_code}")

if __name__ == "__main__":
    print("HVF Locust Load Testing Suite Staged. Ready to simulate 10,000 msgs/sec.")
