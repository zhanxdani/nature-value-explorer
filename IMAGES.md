# Картинки для Nature Value Explorer

**Всего: 56 картинок.**
- **Обязательные: 27.** Без них не работают игры с ползунками: персонажи и сцены, которые меняются при движении ползунка.
- **Желательные: 29.** Карточки и иконки. Пока их нет, приложение само показывает эмодзи-заглушку, так что можно генерировать постепенно.

Маленькие иконки интерфейса (вода, деньги, безопасность и т.п.) генерировать не нужно: в приложении для них используются встроенные иконки Material Symbols.

---

## 1. Общие правила (важно для единого вида)

**Базовый стиль — добавляй в начало КАЖДОГО промпта:**

> Flat vector illustration, friendly educational style, soft natural color palette (forest greens, water blues, warm earth tones), clean simple shapes, subtle gradients, soft daylight, no text, no letters, no numbers, no logos, no watermark.

**Для персонажей добавляй:**

> Head-and-shoulders portrait, centered, facing the viewer, plain soft light-green background, same character design style as the rest of the series.

**Для сцен добавляй:**

> Wide landscape, 16:9, slightly elevated three-quarter view.

**Серии состояний — самое важное.** Ползунок «оживает» только если картинки одной серии выглядят как **одно и то же место**, которое меняется. Поэтому:
1. Сначала сгенерируй **базовую** картинку серии (например, `forest_0`).
2. Остальные состояния делай **редактированием этой картинки** (image edit / «измени эту картинку: …»), а не новым промптом с нуля.
3. Так же с Аной: сначала `ana_neutral`, потом меняй только выражение лица.

**Форматы и размеры** (телефонам нужен лёгкий вес):

| Тип | Размер | Формат | Вес |
|---|---|---|---|
| Сцены (16:9) | 1280×720 | WebP, качество ~80 | ≤ 150 KB |
| Персонажи (1:1) | 512×512 | WebP или PNG | ≤ 60 KB |
| Карточки (1:1) | 768×768 | WebP | ≤ 100 KB |

Сжать можно на squoosh.app. Имена файлов — **точно как в таблицах**, папки — как указано (всё внутри `static/img/`).

---

## 2. Обязательные картинки (27)

### 2.1 Персонажи — `static/img/people/` (9 шт., 1:1)

Они появляются в ряду «Who approves?» под каждым ползунком.

| # | Файл | Кто | Промпт (после базового стиля) |
|---|---|---|---|
| 1 | `ana_neutral.webp` | Ана, фермер — **базовая** | A young woman farmer in a straw hat and simple work clothes, thoughtful neutral expression. |
| 2 | `ana_happy.webp` | Ана довольна | *(edit of ana_neutral)* Same woman, big warm smile. |
| 3 | `ana_angry.webp` | Ана недовольна | *(edit of ana_neutral)* Same woman, arms crossed, frowning. |
| 4 | `villagers.webp` | Жители деревни ниже по реке | A small family from a riverside village: a mother, a father and a child, standing together. |
| 5 | `taxpayer.webp` | Налогоплательщик | A city office worker holding a wallet and a paper bill, slightly skeptical expression. |
| 6 | `ecologist.webp` | Эколог | A field ecologist with binoculars around the neck, a notebook and an outdoor vest. |
| 7 | `investor.webp` | Инвестор | A business person in a suit holding a tablet with an upward chart. |
| 8 | `elder.webp` | Старейшина местной общины | A respected elder of an indigenous forest community, kind and wise expression, simple natural clothing, holding a green leaf. Respectful, not stereotyped, not a specific real culture. |
| 9 | `fisher.webp` | Рыбак | A coastal fisher with a fishing net over the shoulder, sea and small boat in the background. |

### 2.2 Лес — `static/img/scenes/` (5 шт., 16:9)

Глава 4 (Tipping point) и глава 6 (Save the forest).

| # | Файл | Состояние | Промпт |
|---|---|---|---|
| 10 | `forest_0.webp` | Здоровый лес — **базовая** | A dense healthy tropical forest valley with a clear blue river winding through it, birds flying, lush green canopy. |
| 11 | `forest_1.webp` | Частично вырублен | *(edit of forest_0)* About a third of the forest cleared into small farm fields at the edges; the river still clear. |
| 12 | `forest_2.webp` | В основном поля | *(edit of forest_0)* Mostly farmland now, only scattered trees left; the river is brown and muddy. |
| 13 | `forest_3.webp` | Коллапс | *(edit of forest_0)* Collapsed landscape: dry cracked soil, erosion gullies, dead trees, an almost dry brown riverbed, hazy dusty sky, failed crops. |
| 14 | `forest_4.webp` | Восстановление | *(edit of forest_3)* People planting young saplings; small green patches returning; the river has a little water again. |

### 2.3 Болото — `static/img/scenes/` (4 шт., 16:9)

Глава 3 (Build or keep?).

| # | Файл | Состояние | Промпт |
|---|---|---|---|
| 15 | `wetland_0.webp` | Целое болото — **базовая** | A wide green wetland floodplain with reeds, ponds and water birds; a small village with houses downstream in the background. |
| 16 | `wetland_1.webp` | Осушена треть | *(edit of wetland_0)* Drainage ditches cut into the wetland; a third of it turned into crop fields. |
| 17 | `wetland_2.webp` | Полностью осушено | *(edit of wetland_0)* The whole wetland drained into rectangular crop fields with straight ditches; the village still in the background. |
| 18 | `wetland_flood.webp` | Осушено + шторм | *(edit of wetland_2)* Heavy storm with dark clouds and rain; the fields and the village downstream are flooded. |

### 2.4 Завтрак — `static/img/scenes/` (3 шт., 16:9)

Глава 1 (What if bees disappeared?).

| # | Файл | Состояние | Промпт |
|---|---|---|---|
| 19 | `breakfast_full.webp` | Все опылители есть — **базовая** | Top-down view of a rich breakfast table: coffee, apples, berries, orange juice, almonds, a jar of honey, bread, a glass of water. |
| 20 | `breakfast_half.webp` | Половина опылителей | *(edit of breakfast_full)* Same table, but half of the fruits, berries, almonds and honey are gone; some plates empty. |
| 21 | `breakfast_bare.webp` | Опылителей нет | *(edit of breakfast_full)* Same table with only bread and a glass of water; the other plates and cups empty. |

### 2.5 Побережье — `static/img/scenes/` (3 шт., 16:9)

Глава 6 (Grey vs green).

| # | Файл | Состояние | Промпт |
|---|---|---|---|
| 22 | `coast_grey.webp` | Только бетон — **базовая** | A tropical coastal village protected by a long grey concrete sea wall; waves hitting the wall; bare grey water. |
| 23 | `coast_mix.webp` | Половина на половину | *(edit of coast_grey)* Half of the coast still concrete wall, the other half protected by a green mangrove belt and a coral reef offshore. |
| 24 | `coast_green.webp` | Только природа | *(edit of coast_grey)* The concrete wall replaced by a wide mangrove belt and a healthy coral reef offshore where waves break; fishing boats nearby. |

### 2.6 Три будущих одного леса — `static/img/scenes/` (3 шт., 16:9)

Глава 5 (Who decides?). Желательно как одна серия.

| # | Файл | Будущее | Промпт |
|---|---|---|---|
| 25 | `future_sacred.webp` | Священный лес — **базовая** | An old-growth forest with one giant ancient tree at the center, small offerings at its roots, local people standing respectfully nearby. Generic, not a specific religion. |
| 26 | `future_agro.webp` | Агролес (деревья + культуры) | *(edit of future_sacred)* The same land as agroforestry: tall trees mixed with crops growing beneath them, a farmer working, bees flying. The giant tree still stands. |
| 27 | `future_plantation.webp` | Плантация | *(edit of future_sacred)* The same land as a monoculture oil palm plantation in straight rows; a bulldozer; the giant tree is gone. |

---

## 3. Желательные картинки (29)

Пока их нет, на их месте будут эмодзи.

### 3.1 Экосистемы для игры «Which is worth more?» — `static/img/biomes/` (8 шт., 1:1)

Тропический лес и болото берутся из `forest_0` и `wetland_0`.

| # | Файл | Промпт |
|---|---|---|
| 28 | `estuary.webp` | An estuary where a river meets the sea, sandbanks and birds. |
| 29 | `coral_reef.webp` | A colorful healthy coral reef with fish, underwater view. |
| 30 | `open_ocean.webp` | The open ocean, deep blue waves to the horizon, a whale tail. |
| 31 | `lake_river.webp` | A calm lake with a river flowing in, reeds and hills. |
| 32 | `boreal_forest.webp` | A northern boreal forest of spruces and pines with a small lake. |
| 33 | `grassland.webp` | Wide grassland with grazing cows and wildflowers. |
| 34 | `mangroves.webp` | Mangrove trees with stilt roots in shallow coastal water, small fish among roots. |
| 35 | `farm_field.webp` | A large flat wheat field under a blue sky, a tractor far away. |

### 3.2 Предметы утра — `static/img/items/` (8 шт., 1:1)

Глава 1 (What did you use today?).

| # | Файл | Промпт |
|---|---|---|
| 36 | `coffee.webp` | A cup of coffee next to a coffee plant branch with white flowers and a bee. |
| 37 | `bread.webp` | A loaf of bread next to wheat ears blowing in the wind. |
| 38 | `apple.webp` | A red apple next to apple blossoms with a bee. |
| 39 | `water.webp` | A glass of clean water in front of a forest and stream. |
| 40 | `fish.webp` | A fish on a plate, with mangrove roots in the background. |
| 41 | `air.webp` | A person breathing fresh air in a green forest, leaves around. |
| 42 | `medicine.webp` | A willow branch next to a small medicine bottle and pills. |
| 43 | `hike.webp` | A hiker on a mountain trail looking at a lake. |

### 3.3 Карточки Díaz — `static/img/ncp/` (5 шт., 1:1)

Глава 5 (Good or bad? и Nature or culture?).

| # | Файл | Промпт |
|---|---|---|
| 44 | `wolf.webp` | A wolf standing on a hill, with deer far away on one side and sheep on the other. |
| 45 | `mosquito.webp` | A close-up of a mosquito, slightly menacing but friendly cartoon. |
| 46 | `river_flood.webp` | A river flooding farm fields; after the water, dark fertile soil. |
| 47 | `bee.webp` | A bee pollinating a flower in a field of crops. |
| 48 | `root_bridge.webp` | A living bridge made of tree roots crossing a jungle stream, people walking on it. Original illustration, not copying any photo. |

### 3.4 Карточки решений — `static/img/solutions/` (6 шт., 1:1)

Глава 6 (Six real solutions).

| # | Файл | Промпт |
|---|---|---|
| 49 | `pes.webp` | A farmer and an official shaking hands in front of a standing forest. |
| 50 | `accounting.webp` | An open ledger book with a small forest and river growing out of its pages. |
| 51 | `protected_area.webp` | A landscape of forests and sea under a large transparent protective shield. |
| 52 | `nbs.webp` | People planting mangrove seedlings along a coast. |
| 53 | `comanagement.webp` | Community members and a scientist sitting in a circle under a big tree, discussing a map. |
| 54 | `business.webp` | An office desk with a report showing a leaf-shaped chart, a plant on the desk. |

### 3.5 Начало и финал — `static/img/` (2 шт.)

| # | Файл | Размер | Промпт |
|---|---|---|---|
| 55 | `hero.webp` | 16:9 | A panoramic landscape flowing from mountains and forests through wetlands and farms to the coast and coral reef; people living among it. |
| 56 | `badge.webp` | 1:1 | A round explorer badge emblem with a globe, a leaf and a compass, no text. |
