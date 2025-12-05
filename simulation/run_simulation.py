import os
import sys
import time
import json

# Try to import traci, if fails, try to append SUMO_HOME/tools
try:
    import traci
except ImportError:
    if 'SUMO_HOME' in os.environ:
        tools = os.path.join(os.environ['SUMO_HOME'], 'tools')
        sys.path.append(tools)
        import traci
    else:
        # Try to auto-detect SUMO_HOME on macOS/Linux
        try:
            import subprocess
            result = subprocess.run(['brew', '--prefix', 'sumo'], capture_output=True, text=True)
            if result.returncode == 0:
                sumo_root = result.stdout.strip()
                sumo_home = os.path.join(sumo_root, 'share', 'sumo')
                os.environ['SUMO_HOME'] = sumo_home
                tools = os.path.join(sumo_home, 'tools')
                sys.path.append(tools)
                import traci
                print(f"✅ Auto-detected SUMO_HOME: {sumo_home}")
            else:
                raise ImportError("Could not auto-detect SUMO_HOME")
        except Exception as e:
            raise ImportError("Please declare environment variable 'SUMO_HOME' or install traci via pip")

def run_simulation():
    """Run SUMO simulation and detect parking violations."""
    
    # Start SUMO
    # Try GUI first, fallback to headless if fails
    sumoBinary = os.environ.get("SUMO_BINARY", "sumo-gui")
    sumoCmd = [sumoBinary, "-c", "simulation/parking.sumocfg"]
    
    print(f"🚀 Starting SUMO Simulation using {sumoBinary}...")
    
    try:
        # Reduce retries to fail fast if GUI doesn't start
        traci.start(sumoCmd, numRetries=3)
    except traci.exceptions.FatalTraCIError:
        print("⚠️  Failed to start SUMO GUI (likely missing XQuartz).")
        print("🔄 Switching to headless mode (no window)...")
        sumoBinary = "sumo"
        sumoCmd = [sumoBinary, "-c", "simulation/parking.sumocfg"]
        traci.start(sumoCmd)
    
    step = 0
    violations = []
    
    # State file path
    state_file = "simulation/simulation_state.json"
    
    while step < 5000:
        traci.simulationStep()
        
        # Get all vehicle IDs
        vehicles = traci.vehicle.getIDList()
        
        current_violations = []
        
        for veh_id in vehicles:
            # Get speed and lane
            speed = traci.vehicle.getSpeed(veh_id)
            lane_id = traci.vehicle.getLaneID(veh_id)
            
            # Check for illegal parking
            # Condition: Stopped (speed < 0.1) on 'A0B0_0' (Parking Lane)
            if speed < 0.1 and lane_id == "A0B0_0":
                current_violations.append(veh_id)
                if veh_id not in violations:
                    print(f"⚠️ VIOLATION DETECTED: Vehicle {veh_id} parked illegally on {lane_id} at step {step}")
                    violations.append(veh_id)
                    
                    # Highlight vehicle in GUI (Red)
                    try:
                        traci.vehicle.setColor(veh_id, (255, 0, 0, 255))
                    except:
                        pass # Ignore if headless
        
        # Write state to file
        state = {
            "active_violations": current_violations,
            "timestamp": time.time(),
            "step": step
        }
        with open(state_file, "w") as f:
            json.dump(state, f)
            
        step += 1
        time.sleep(0.1) # Slow down for visualization

    traci.close()
    print("✅ Simulation Finished.")

if __name__ == "__main__":
    run_simulation()
