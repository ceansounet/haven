# Missing sprites (checked against the storyboard)

✅ = already drawn (see `sprites/README.md`)  ·  ❌ = still to draw  ·  ♻️ = can probably reuse an existing sprite

## From the storyboard's sprite list
| Sprite | Status |
|---|---|
| Orpheus | ✅ body, arms, legs, tail, 4 eye/eyebrow sets, 6 mouths |
| Boss evil Daven | ✅ body, spikes, arms, feet, eyes, cheeks, mouth |
| Old master | ❌ not drawn (idea from the storyboard: Orpheus with a long beard, so a **beard** piece + maybe a hat/robe could be added on top of the Orpheus rig) |
| Tree | ✅ |
| Trampoline | ✅ (5 animation frames) |
| Blocks | ✅ plain, brick, cracked, mystery |
| Platform | ❌ not drawn (floating platform for jumping) |
| Fireball | ✅ (2 versions) |
| Snowball / ice ball | ❌ not drawn (the wand shoots fire **and** ice) |

## Stage 1: village cutscene
| Sprite | Status |
|---|---|
| Village houses | ✅ one house (♻️ duplicate/flip it for a village) |
| Fence | ✅ fence_gate |
| Villagers ("his peers") | ❌ |
| Destroyed / burning house | ❌ |
| Fire on the ground (flames, smoke) | ❌ (♻️ fireball flame could be reused for small fires) |
| Orpheus sad / crying / angry face | ♻️ frown + angry eyebrows exist; ❌ tears if wanted |
| Sky / ground background | ♻️ clouds + mountains exist; ❌ ground |

## Stage 2: training
| Sprite | Status |
|---|---|
| Old master on his cloud | ❌ master · ♻️ cloud_1..3 |
| Scarecrow (boss) | ❌ |
| Mystery cube | ✅ block_mystery |
| Boots (double jump) | ❌ |
| Magic wand | ✅ |
| Ice ball | ❌ |
| Dash effect | ♻️ maybe zigzag_1/2, otherwise ❌ |
| Jump / double-jump puff | ❌ |
| Tip bubble / speech bubble | ❌ |

## Stage 3: travel to the castle
| Sprite | Status |
|---|---|
| Ground / terrain tiles | ❌ |
| Traps (spikes, pits, etc.) | ❌ |
| Bad guys / enemies | ❌ |
| Backgrounds | ✅ mountains, clouds, tree · ♻️ evil clouds + rain for a stormy path |
| Castle from outside | ✅ tower, center wall, gate (portcullis) |

## Stage 4: boss fight
| Sprite | Status |
|---|---|
| Castle arena (inside: floor, walls) | ❌ |
| Daven rising from the ground (cracks / dust) | ❌ |
| Daven's fireballs | ✅ |
| Lava (rising) | ❌ |
| Robots | ❌ |
| Frozen robot / ice block effect | ❌ |
| Small Daven running, arms flailing | ♻️ daven_rig scaled down + animated arms |
| Speech bubbles ("waaaa", "what's that, I didn't sign for this!") | ❌ |
| Orpheus closed eyes | ❌ (♻️ `^ ^` happy eyes might work) |
| Floating aura around Orpheus | ❌ |
| Powerful orb | ❌ |
| Daven frozen in place and time | ❌ (ice overlay or color tint) |
| Final explosion / blast | ❌ |
| "The end" screen | ❌ |

## Not in the story yet (drawn but unused)
- `key.png`: no key in the story yet
- `zigzag_1.png`, `zigzag_2.png`: purpose unknown
- `orpheus_hand_1.png`, `orpheus_hand_2.png`: guessed to be hands
- `effects/rain/`: no rain scene yet (could fit stage 3 or the boss intro)
- `game icon maybe.png`: left as is in `asset pack 1/`

## Probably needed but not in the storyboard
- UI: health bar / hearts, boss health bar, ability icons
- Collectible / pickup effect for the wand and boots
- Hit flash / damage effect
