### Original Marshall et al. Features

| Feature                         | Explanation                                                   |
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

### Adapted Marshall et al. Features