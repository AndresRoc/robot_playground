# Robot Playground

This is a workspace designed for those who want to play with ROS2 and robots

## Purpose

This repository is structured as a development platform for three robot platforms:
- 6-DOF manipulator
- 4-DOF SCARA
- Mobile base (2 drive wheels + 4 casters)

Current status:
- URDF robot models are present and valid.
- Kinematics and planning packages are available intentionally empty.
- Bringup package provides launch/config infrastructure.

## Workspace Structure

- `src/robot_description`
  - Robot URDF files and future mesh/config assets.
  - Owns robot geometry and joint structure.
- `src/robot_kinematics`
  - Package reserved for FK/IK solvers and kinematic utilities.
  - Currently placeholder-only.
- `src/robot_planning`
  - Package reserved for trajectory/path planners and post-processors.
  - Currently placeholder-only.
- `src/robot_control`
  - Package reserved for control-side execution (trajectory following and low-level command interfaces).
  - Currently template-only.
- `src/robot_bringup`
  - Launch entry points and YAML configuration.
  - Orchestrates model loading, state publishing, and RViz.

## Package for

### robot_description

Contains the robot digital twins and should remain focused on model data:
- `urdf/manipulator_robot.urdf`
- `urdf/scara_robot.urdf`
- `urdf/mobile_robot.urdf`

Design rule:
- No control/planning logic in this package.
- Only robot description artifacts (URDF/Xacro/meshes/config).

### robot_kinematics

Intended for:
- FK libraries per robot type.
- IK solvers (analytic where possible, numerical fallback where needed).
- Jacobian computation, singularity checks, and workspace constraints.

Planned module split:
- `solvers/` for FK/IK implementations.
- `models/` for DH or geometric parameter definitions.
- `utils/` for math helpers and numeric checks.

### robot_planning

Intended for:
- Joint-space path generation.
- Cartesian path generation.
- Time parameterization and trajectory smoothing.
- Feasibility checks (joint limits, velocity/acceleration bounds).

Planned module split:
- `planners/` for algorithm families.
- `constraints/` for limit and safety checks.
- `adapters/` for consuming kinematics outputs.

### robot_bringup

Current role:
- Hosts launch files and parameter sets for development runs.

Planned role:
- Runtime profiles per robot (`manipulator`, `scara`, `mobile`).
- Environment-specific launch variants (`sim`, `rviz_only`, `algorithm_test`).
- Central point for selecting robot model + algorithm stack.

### robot_control

Intended for:
- Consume planner outputs (joint trajectories, velocity commands, setpoints).
- Convert high-level commands into controller-compatible references.
- Enforce runtime limits and safety gates before actuation.
- Provide execution feedback (tracking error, state, completion/fault status).

Planned module split:
- `controllers/` for controller implementations (joint, differential drive, etc.).
- `interfaces/` for hardware/simulator command adapters.
- `safety/` for limit enforcement, watchdogs, and emergency stop logic.
- `monitoring/` for execution state and diagnostics.

Initial controller targets:
- Manipulator: joint trajectory tracking controller.
- SCARA: joint trajectory tracking with prismatic axis support.
- Mobile: differential drive velocity controller.

Safety control baseline:
- Joint position/velocity/effort clamps.
- Command timeout watchdog.
- Soft-stop and hard-stop states.
- Fault propagation to bringup/monitoring layer.

## Data and Execution Flow

Intended runtime flow:
1. `robot_description` provides URDF.
2. `robot_state_publisher` publishes TF tree from URDF.
3. `robot_kinematics` consumes robot model and computes kinematic transforms/IK.
4. `robot_planning` consumes kinematics interfaces and generates trajectories.
5. `robot_control` validates commands and executes control loops.
6. Hardware/simulator interfaces receive final commands and publish feedback.

## Control Architecture (Planned)

Control stack layering:
1. Planning output layer:
   - Joint trajectory or velocity command messages.
2. Reference manager layer (`robot_control`):
   - Validates message structure and timing.
   - Applies limits/rate filters.
3. Controller layer (`robot_control/controllers`):
   - Computes actuator-level targets from references + current state.
4. Interface layer (`robot_control/interfaces`):
   - Sends commands to sim/hardware.
   - Receives measured states.
5. Monitoring/safety layer (`robot_control/monitoring`, `robot_control/safety`):
   - Tracks tracking error, latency, and fault conditions.

Control modes to support:
- `position_control`
- `velocity_control`
- `trajectory_control`

Runtime profile split:
- `sim`: permissive for development, detailed logging, rapid iteration.
- `hardware`: strict timing, stricter safety, deterministic command handling.

## Development Phases

### Phase 1: Model and Interface Stability

- Keep URDFs stable and versioned.
- Define common interfaces for kinematics and planning modules.
- Add baseline unit tests for package import and interface contracts.

### Phase 2: Kinematics Core

- Implement FK for each robot.
- Implement IK for manipulator and SCARA.
- Add solver validation against known poses.

### Phase 3: Planning Core

- Implement interpolation and basic planners.
- Add constraint checking and trajectory validation.
- Add benchmark scripts for solver/planner performance.

### Phase 4: Integration and Execution

- Add execution adapter package (`robot_control` and/or simulator integration).
- Connect planner outputs to executable trajectories.
- Add end-to-end integration tests with launch-based scenarios.

### Phase 5: Closed-Loop Control Validation

- Add baseline controllers per robot family.
- Validate tracking on canonical trajectories.
- Add safety/fault injection tests.
- Define acceptance metrics (tracking error, settle time, command latency).

## Conventions

- Keep algorithm code out of `robot_description`.
- Keep launch/runtime logic out of algorithm packages.
- Keep robot-specific constants isolated from generic solver logic.
- Prefer deterministic APIs with explicit inputs/outputs.

## Build and Environment

```bash
cd /home/dev/ros2_ws
source /opt/ros/kilted/setup.bash
colcon build
source install/setup.bash
```

### `robot_bringup` launch

Manipulator:

```bash
ros2 launch robot_bringup dev_stack.launch.py \
  model:=/src/robot_description/urdf/manipulator_robot.urdf
```

SCARA:

```bash
ros2 launch robot_bringup dev_stack.launch.py \
  model:=/src/robot_description/urdf/scara_robot.urdf
```

Mobile base:

```bash
ros2 launch robot_bringup dev_stack.launch.py \
  model:=/src/robot_description/urdf/mobile_robot.urdf
```

In RViz:
- Set `Fixed Frame` to `base_link`.
- Add `RobotModel` display if not already present.

## Notes

- Kinematics and planning scripts are intentionally empty placeholders.
- Control scripts/templates are also intentionally empty placeholders.
- This repository is now focused on architecture readiness and incremental implementation.
