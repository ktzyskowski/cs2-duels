# src.processing.features

| Feature                              | Type   | Time Series? | Description                                                                                         |
|--------------------------------------|--------|--------------|-----------------------------------------------------------------------------------------------------|
| `attacker_crosshair_placement_score` | float  | Yes          | Score between -1 and 1 indicating how aligned the attacker player's crosshair is on their opponent. |
| `defender_crosshair_placement_score` | float  | Yes          | Score between -1 and 1 indicating how aligned the defender player's crosshair is on their opponent. |
| `attacker_x`                         | float  | Yes          | The x component of the attacker player's position.                                                  |
| `attacker_y`                         | float  | Yes          | The y component of the attacker player's position.                                                  |
| `attacker_z`                         | float  | Yes          | The z component of the attacker player's position.                                                  |
| `defender_x`                         | float  | Yes          | The x component of the defender player's position.                                                  |
| `defender_y`                         | float  | Yes          | The y component of the defender player's position.                                                  |
| `defender_z`                         | float  | Yes          | The z component of the defender player's position.                                                  |
| `attacker_vx`                        | float  | Yes          | The x component of the attacker player's velocity.                                                  |
| `attacker_vy`                        | float  | Yes          | The y component of the attacker player's velocity.                                                  |
| `attacker_vz`                        | float  | Yes          | The z component of the attacker player's velocity.                                                  |
| `defender_vx`                        | float  | Yes          | The x component of the defender player's velocity.                                                  |
| `defender_vy`                        | float  | Yes          | The y component of the defender player's velocity.                                                  |
| `defender_vz`                        | float  | Yes          | The z component of the defender player's velocity.                                                  |
| `attacker_is_blinded`                | bool   | No           | Whether the attacker player is blinded.                                                             |
| `defender_is_blinded`                | bool   | No           | Whether the defender player is blinded.                                                             |
| `attacker_is_airborne`               | bool   | No           | Whether the attacker player is airborne.                                                            |
| `defender_is_airborne`               | bool   | No           | Whether the defender player is airborne.                                                            |
| `attacker_is_ducking`                | bool   | No           | Whether the attacker player is ducking.                                                             |
| `defender_is_ducking`                | bool   | No           | Whether the defender player is ducking.                                                             |
| `attacker_is_standing`               | bool   | No           | Whether the attacker player is standing.                                                            |
| `defender_is_standing`               | bool   | No           | Whether the defender player is standing.                                                            |
| `attacker_is_scoped`                 | bool   | No           | Whether the attacker player is aiming down the scope of their weapon.                               |
| `defender_is_scoped`                 | bool   | No           | Whether the defender player is aiming down the scope of their weapon.                               |
| `attacker_is_walking`                | bool   | No           | Whether the attacker player is slow-walking.                                                        |
| `defender_is_walking`                | bool   | No           | Whether the defender player is slow-walking.                                                        |
| `attacker_equipment_value`           | int    | No           | Total attacker player equipment value.                                                              |
| `defender_equipment_value`           | int    | No           | Total defender player equipment value.                                                              |
| `attacker_cash`                      | int    | No           | Remaining attacker player cash.                                                                     |
| `defender_cash`                      | int    | No           | Remaining defender player cash.                                                                     |
| `attacker_has_helmet`                | bool   | No           | Whether the attacker player has a helmet.                                                           |
| `defender_has_helmet`                | bool   | No           | Whether the defender player has a helmet.                                                           |
| `attacker_active_weapon`             | string | No           | Active weapon of the attacker player.                                                               |
| `defender_active_weapon`             | string | No           | Active weapon of the defender player.                                                               |
| `attacker_hp`                        | int    | No           | Remaining health points of the attacker player.                                                     |
| `defender_hp`                        | int    | No           | Remaining health points of the defender player.                                                     |
| `attacker_armor`                     | int    | No           | Remaining armor points of the attacker player.                                                      |
| `defender_armor`                     | int    | No           | Remaining armor points of the defender player.                                                      |
