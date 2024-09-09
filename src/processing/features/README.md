# src.processing.features

There are two files, `marshall.py` and `zyskowski.py`, where I attempted to adapt the features from Marshall et al. and
create my own features as well. You can see a brief overview of the features and their descriptions in the tables below.
My hopes are that my features are an improvement upon Marshall et al. and that they are more well-suited for the
specific task of predicting duel outcomes.

### Marshall et al. Features

| Feature                         | Description                                                   |
|---------------------------------|---------------------------------------------------------------|
| `hp`                            | Remaining health points of the player                         |
| `armor`                         | Remaining armor points of the player                          |
| `isBlinded`                     | Whether the player is blinded                                 |
| `isAirborne`                    | Whether the player is airborne                                |
| `isDucking`                     | Whether the player is ducking                                 |
| `isStanding`                    | Whether the player is standing                                |
| `isScoped`                      | Whether the player is aiming down the scope of their weapon   |
| `isWalking`                     | Whether the player is walking (not running)                   |
| `equipmentValue`                | Total player equipment value                                  |
| `cash`                          | Remaining player cash                                         |
| `hasHelmet`                     | Whether the player has a helmet                               |
| `kills_from_avg`                | Distance of players kill count from average                   |
| `deaths_from_avg`               | Distance of players death count from average                  |
| `total_hp_enemy`                | Total health points of enemies                                |
| `total_hp_team`                 | Total health points of teammates                              |
| `num_enemy_alive`               | The number of enemies alive                                   |
| `num_team_alive`                | The number of teammates alive                                 |
| `enemy_in_range_200`            | The number of enemies within 200 units range                  |
| `enemy_in_range_500`            | The number of enemies within 500 units range                  |
| `enemy_in_range_1000`           | The number of enemies within 1000 units range                 |
| `enemy_in_range_2000`           | The number of enemies within 2000 units range                 |
| `enemy_hp_in_range_500`         | The total health points of enemies within 500 units range     |
| `enemy_hp_in_range_1000`        | The total health points of enemies within 1000 units range    |
| `enemy_hp_in_range_2000`        | The total health points of enemies within 2000 units range    |
| `enemy_equipment_in_range_500`  | The total equipment value of enemies within 500 units range   |
| `enemy_equipment_in_range_1000` | The total equipment value of enemies within 1000 units range  |
| `enemy_equipment_in_range_2000` | The total equipment value of enemies within 2000 units range  |
| `team_in_range_200`             | Number of teammates within 200 units range                    |
| `team_in_range_500`             | Number of teammates within 500 units range                    |
| `team_in_range_1000`            | Number of teammates within 1000 units range                   |
| `equipment_value_team`          | Total equipment value of teammates                            |
| `equipment_value_enemy`         | Total equipment value of enemies                              |
| `distance_closest_enemy`        | Distance to closest enemy                                     |
| `hp_closest_enemy`              | Health points of the closest enemy                            |
| `active_weapon`                 | Active weapon category of the player (one-hot encoded)        |
| `weapon_closest_enemy`          | Active weapon category of the closest enemy (one-hot encoded) |

### Zyskowski Features

| Feature                         | Description                                                  |
|---------------------------------|--------------------------------------------------------------|
| `kills_from_avg`                | Distance of players kill count from average                  |
| `deaths_from_avg`               | Distance of players death count from average                 |
| `total_hp_enemy`                | Total health points of enemies                               |
| `total_hp_team`                 | Total health points of teammates                             |
| `num_enemy_alive`               | The number of enemies alive                                  |
| `num_team_alive`                | The number of teammates alive                                |
| `enemy_in_range_200`            | The number of enemies within 200 units range                 |
| `enemy_in_range_500`            | The number of enemies within 500 units range                 |
| `enemy_in_range_1000`           | The number of enemies within 1000 units range                |
| `enemy_in_range_2000`           | The number of enemies within 2000 units range                |
| `enemy_hp_in_range_500`         | The total health points of enemies within 500 units range    |
| `enemy_hp_in_range_1000`        | The total health points of enemies within 1000 units range   |
| `enemy_hp_in_range_2000`        | The total health points of enemies within 2000 units range   |
| `enemy_equipment_in_range_500`  | The total equipment value of enemies within 500 units range  |
| `enemy_equipment_in_range_1000` | The total equipment value of enemies within 1000 units range |
| `enemy_equipment_in_range_2000` | The total equipment value of enemies within 2000 units range |
| `team_in_range_200`             | Number of teammates within 200 units range                   |
| `team_in_range_500`             | Number of teammates within 500 units range                   |
| `team_in_range_1000`            | Number of teammates within 1000 units range                  |
| `equipment_value_team`          | Total equipment value of teammates                           |
| `equipment_value_enemy`         | Total equipment value of enemies                             |

| Feature                    | Type   | Time Series? | Description                                                           |
|----------------------------|--------|--------------|-----------------------------------------------------------------------|
| `attacker_hp`              | int    | No           | Remaining health points of the attacker player.                       |
| `defender_hp`              | int    | No           | Remaining health points of the defender player.                       |
| `attacker_armor`           | int    | No           | Remaining armor points of the attacker player.                        |
| `defender_armor`           | int    | No           | Remaining armor points of the defender player.                        |
| `attacker_x`               | float  | Yes          | The x component of the attacker player's position.                    |
| `attacker_y`               | float  | Yes          | The y component of the attacker player's position.                    |
| `attacker_z`               | float  | Yes          | The z component of the attacker player's position.                    |
| `defender_x`               | float  | Yes          | The x component of the defender player's position.                    |
| `defender_y`               | float  | Yes          | The y component of the defender player's position.                    |
| `defender_z`               | float  | Yes          | The z component of the defender player's position.                    |
| `attacker_vx`              | float  | Yes          | The x component of the attacker player's velocity.                    |
| `attacker_vy`              | float  | Yes          | The y component of the attacker player's velocity.                    |
| `attacker_vz`              | float  | Yes          | The z component of the attacker player's velocity.                    |
| `defender_vx`              | float  | Yes          | The x component of the defender player's velocity.                    |
| `defender_vy`              | float  | Yes          | The y component of the defender player's velocity.                    |
| `defender_vz`              | float  | Yes          | The z component of the defender player's velocity.                    |
| `attacker_is_blinded`      | bool   | No           | Whether the attacker player is blinded.                               |
| `defender_is_blinded`      | bool   | No           | Whether the defender player is blinded.                               |
| `attacker_is_airborne`     | bool   | No           | Whether the attacker player is airborne.                              |
| `defender_is_airborne`     | bool   | No           | Whether the defender player is airborne.                              |
| `attacker_is_ducking`      | bool   | No           | Whether the attacker player is ducking.                               |
| `defender_is_ducking`      | bool   | No           | Whether the defender player is ducking.                               |
| `attacker_is_standing`     | bool   | No           | Whether the attacker player is standing.                              |
| `defender_is_standing`     | bool   | No           | Whether the defender player is standing.                              |
| `attacker_is_scoped`       | bool   | No           | Whether the attacker player is aiming down the scope of their weapon. |
| `defender_is_scoped`       | bool   | No           | Whether the defender player is aiming down the scope of their weapon. |
| `attacker_is_walking`      | bool   | No           | Whether the attacker player is slow-walking.                          |
| `defender_is_walking`      | bool   | No           | Whether the defender player is slow-walking.                          |
| `attacker_equipment_value` | int    | No           | Total attacker player equipment value.                                |
| `defender_equipment_value` | int    | No           | Total defender player equipment value.                                |
| `attacker_cash`            | int    | No           | Remaining attacker player cash.                                       |
| `defender_cash`            | int    | No           | Remaining defender player cash.                                       |
| `attacker_has_helmet`      | bool   | No           | Whether the attacker player has a helmet.                             |
| `defender_has_helmet`      | bool   | No           | Whether the defender player has a helmet.                             |
| `attacker_active_weapon`   | string | No           | Active weapon of the attacker player.                                 |
| `defender_active_weapon`   | string | No           | Active weapon of the defender player.                                 |
