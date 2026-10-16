# FLUX 3 Image Klein｜30组教学综合测评 V1

> 任务设计与提示词，不是已完成的30合一ComfyUI运行JSON；所有案例尚未GPU实测。

## 一、原始工作流复用原则

保留原始7套JSON不动；在30合一运行副本里只复制现有原生节点/子图和连线，填写本表任务素材、提示词及推荐测试参数；不安装新的自定义节点，不另造推理路线。

**关键修正：** F01/F02 内部 enable_prompt_upsampler=True 才是开启；F03/F04 的 ComfySwitchNode=False 才走 TextGenerate 增强，True 走原始Prompt。F05/F06没有增强器。对公平对比，UP的生成结果必须复用同一份已扩写文本，两模型不能分别随机扩写后宣称同条件。

官方模型参考：Base 50步/CFG3.5，Distilled 16步/CFG1。原压缩包内F02的15步、F03的CFG1、F07的Base25步均需明确处理，不能隐瞒。

## 二、30组总清单

| 编号 | 模块 | 观众关心 | 输入 | 比例 / 宽高 | Seed | 润色 | 原布尔值 |
|---|---|---|---|---|---:|---|---|
| T01 | F01 写实肖像 / 皮肤与发丝 | 自然皮肤、发丝、假脸 | 无需 | 1:1 1024×1024 | 9527 | ON | True |
| T02 | F02 写实肖像 / 皮肤与发丝 | 速度、相同细节 | 无需 | 1:1 1024×1024 | 9527 | ON | True |
| T03 | F01 全身人物 / 手脚与服装 | 双手、双脚、裤缝 | 无需 | 9:16 720×1280 | 9528 | ON | True |
| T04 | F02 全身人物 / 手脚与服装 | 肢体完整性与速度 | 无需 | 9:16 720×1280 | 9528 | ON | True |
| T05 | F01 商用产品 / 中英文字 | 中文、英文准确、商品质感 | 无需 | 4:3 1152×864 | 9529 | OFF | False |
| T06 | F02 商用产品 / 中英文字 | 字形、细节、logo污染 | 无需 | 4:3 1152×864 | 9529 | OFF | False |
| T07 | F01 室内建筑 / 透视与材质 | 桌椅数量、玻璃木纹、透视 | 无需 | 16:9 1280×720 | 9530 | ON | True |
| T08 | F02 室内建筑 / 透视与材质 | 透视失真与耗时 | 无需 | 16:9 1280×720 | 9530 | ON | True |
| T09 | F01 双人复杂叙事 / 关系与空间 | 多人物、手与道具、左右关系 | 无需 | 16:9 1280×720 | 9531 | OFF | False |
| T10 | F02 双人复杂叙事 / 关系与空间 | 提示词关系遵循 | 无需 | 16:9 1280×720 | 9531 | OFF | False |
| T11 | F03 服装改色 / 不改款式 | 只改衣服颜色、背景保留 | A02 | 9:16 720×1280 | 9627 | ON | False |
| T12 | F04 服装改色 / 不改款式 | 服装保真和变色准确 | A02 | 9:16 720×1280 | 9627 | ON | False |
| T13 | F03 金属耳饰换花朵 / 小范围保留 | 金耳环能否变花，脸变不变 | A01 | 1:1 1024×1024 | 9628 | OFF | True |
| T14 | F04 金属耳饰换花朵 / 小范围保留 | 局部准确性、脸部保持 | A01 | 1:1 1024×1024 | 9628 | OFF | True |
| T15 | F03 人物改姿态 / 保持身份 | 改坐姿仍保持脸衣服背景 | A03 | 9:16 720×1280 | 9629 | ON | False |
| T16 | F04 人物改姿态 / 保持身份 | 人物身份漂移、手脚畸形 | A03 | 9:16 720×1280 | 9629 | ON | False |
| T17 | F03 场景物体替换 / 光影一致 | 杯子变花瓶，光影自然 | A04 | 16:9 1280×720 | 9630 | ON | False |
| T18 | F04 场景物体替换 / 光影一致 | 目标替换率、是否留残影 | A04 | 16:9 1280×720 | 9630 | ON | False |
| T19 | F03 招牌文字精确修改 | OPEN→AI-KSK文字，字体稳定 | A05 | 4:3 1152×864 | 9631 | OFF | True |
| T20 | F04 招牌文字精确修改 | 文字准确率与背景保留 | A05 | 4:3 1152×864 | 9631 | OFF | True |
| T21 | F05 双参考 / 脸和衣服 | 脸属于A01、衣服属于R02 | A01 + R02 | 4:3 1152×864 | 9727 | N/A | 不适用 |
| T22 | F05 三参考 / 脸衣服场景 | 脸衣服场景三来源 | A01 + R02 + R03 | 16:9 1280×720 | 9728 | N/A | 不适用 |
| T23 | F05 三参考 / 双人身份和场景 | 两个人不能串脸 | A01 + R05 + R03 | 16:9 1280×720 | 9729 | N/A | 不适用 |
| T24 | F05 四参考 / 人衣景道具 | 4图来源控制与道具持握 | A01 + R02 + R03 + R04 | 9:16 720×1280 | 9730 | N/A | 不适用 |
| T25 | F06 单框替换大物体 / 入门 | 入门单框替换，框与物体对应 | A04 | 16:9 1280×720 | 9827 | N/A | 不适用 |
| T26 | F06 单框耳饰替换 / 精准度挑战 | 耳饰小目标，和T13/T14对照 | A01 | 1:1 1024×1024 | 9828 | N/A | 不适用 |
| T27 | F06 双框布局 / 左右分置 | 左右双框、目标不串位 | A04 | 16:9 1280×720 | 9829 | N/A | 不适用 |
| T28 | F06 三框综合布局 / 空间控制 | 3框与远近层次位置 | A06 | 16:9 1280×720 | 9830 | N/A | 不适用 |
| T29 | F07 结果汇总板 | 5组成对图画质/速度数据 | T01–T10结果 | 混合 按原图 | — | N/A | 不适用 |
| T30 | F07 结果汇总板 | 编辑、参考、布局适用场景 | T11–T28结果 | 混合 按原图 | — | N/A | 不适用 |

## 三、30组全部可复制提示词

> 下面每个T编号都列出完整英文Prompt；成对对比严格使用完全相同的原始Prompt，不应各写一份不同英文文案。

### T01｜写实肖像 / 皮肤与发丝（F01，润色：ON）
素材：无需；尺寸：1024×1024；Seed：9527。

A portrait-oriented editorial photograph of an adult woman in her late twenties with natural facial proportions, slightly asymmetrical features, visible pores and subtle skin texture. She has dark brown shoulder-length hair with individual strands catching soft side window light, a simple cream knit top and understated silver earrings. Frame her from chest up, looking slightly left of camera, with a softly blurred muted green interior behind her. The lighting must produce realistic shadows around the nose and jaw. Avoid airbrushed skin, plastic textures, over-sharpening, extra jewelry and exaggerated glamour.

### T02｜写实肖像 / 皮肤与发丝（F02，润色：ON）
素材：无需；尺寸：1024×1024；Seed：9527。

A portrait-oriented editorial photograph of an adult woman in her late twenties with natural facial proportions, slightly asymmetrical features, visible pores and subtle skin texture. She has dark brown shoulder-length hair with individual strands catching soft side window light, a simple cream knit top and understated silver earrings. Frame her from chest up, looking slightly left of camera, with a softly blurred muted green interior behind her. The lighting must produce realistic shadows around the nose and jaw. Avoid airbrushed skin, plastic textures, over-sharpening, extra jewelry and exaggerated glamour.

### T03｜全身人物 / 手脚与服装（F01，润色：ON）
素材：无需；尺寸：720×1280；Seed：9528。

Full-body commercial fashion photograph of an adult woman standing on a pale concrete floor in a spacious contemporary studio. She wears a tailored charcoal blazer, a white crew-neck shirt, straight black trousers and matching white low-top sneakers. Her entire head, both hands with clearly separated fingers and both shoes must be visible inside the frame, with natural anatomy and believable joint positions. One hand loosely holds a small tan leather handbag and the other hangs at her side. Neutral daylight, soft floor shadow, simple background, realistic fabric folds and accurate perspective. No cropped feet or duplicate limbs.

### T04｜全身人物 / 手脚与服装（F02，润色：ON）
素材：无需；尺寸：720×1280；Seed：9528。

Full-body commercial fashion photograph of an adult woman standing on a pale concrete floor in a spacious contemporary studio. She wears a tailored charcoal blazer, a white crew-neck shirt, straight black trousers and matching white low-top sneakers. Her entire head, both hands with clearly separated fingers and both shoes must be visible inside the frame, with natural anatomy and believable joint positions. One hand loosely holds a small tan leather handbag and the other hangs at her side. Neutral daylight, soft floor shadow, simple background, realistic fabric folds and accurate perspective. No cropped feet or duplicate limbs.

### T05｜商用产品 / 中英文字（F01，润色：OFF）
素材：无需；尺寸：1152×864；Seed：9529。

Clean high-end advertising photograph of one matte white reusable aluminum bottle standing upright on a light stone pedestal. The bottle has a single dark navy brand line reading exactly "AI-KSK" and a second larger Chinese line reading exactly "新品上市"; preserve both texts accurately with correct spelling and stroke structure. A small folded linen cloth lies to the left, a water droplet cluster is visible on the bottle and the background is warm gray. Three-quarter product angle, realistic controlled reflections, crisp readable typography, no additional brands, no duplicate products, no floating objects.

### T06｜商用产品 / 中英文字（F02，润色：OFF）
素材：无需；尺寸：1152×864；Seed：9529。

Clean high-end advertising photograph of one matte white reusable aluminum bottle standing upright on a light stone pedestal. The bottle has a single dark navy brand line reading exactly "AI-KSK" and a second larger Chinese line reading exactly "新品上市"; preserve both texts accurately with correct spelling and stroke structure. A small folded linen cloth lies to the left, a water droplet cluster is visible on the bottle and the background is warm gray. Three-quarter product angle, realistic controlled reflections, crisp readable typography, no additional brands, no duplicate products, no floating objects.

### T07｜室内建筑 / 透视与材质（F01，润色：ON）
素材：无需；尺寸：1280×720；Seed：9530。

Wide architectural interior photograph of a quiet modern reading room with one long oak table, exactly four identical dining chairs, floor-to-ceiling windows along the left wall, a single green potted tree near the far right corner and a narrow black metal pendant lamp centered above the table. Linear one-point perspective with consistent window frames and straight verticals. Warm natural sunlight forms coherent shadows across a polished concrete floor. Show realistic glass transparency, wood grain and soft textile cushions, spacious negative space and an uncluttered commercial architectural composition.

### T08｜室内建筑 / 透视与材质（F02，润色：ON）
素材：无需；尺寸：1280×720；Seed：9530。

Wide architectural interior photograph of a quiet modern reading room with one long oak table, exactly four identical dining chairs, floor-to-ceiling windows along the left wall, a single green potted tree near the far right corner and a narrow black metal pendant lamp centered above the table. Linear one-point perspective with consistent window frames and straight verticals. Warm natural sunlight forms coherent shadows across a polished concrete floor. Show realistic glass transparency, wood grain and soft textile cushions, spacious negative space and an uncluttered commercial architectural composition.

### T09｜双人复杂叙事 / 关系与空间（F01，润色：OFF）
素材：无需；尺寸：1280×720；Seed：9531。

Wide cinematic street photograph at dusk showing exactly two adult people on a dry city sidewalk. On the left, an adult woman in a mustard yellow coat holds a folded black umbrella in her right hand and looks at the man. On the right, an adult man in a dark blue jacket is holding a white paper coffee cup in his left hand and points toward a small red bicycle parked between them. A lit storefront is behind the pair, with a tree in the distant background. Keep left/right identities, hand-object relationships and the number of people correct. Natural anatomy, believable perspective and coherent dusk lighting.

### T10｜双人复杂叙事 / 关系与空间（F02，润色：OFF）
素材：无需；尺寸：1280×720；Seed：9531。

Wide cinematic street photograph at dusk showing exactly two adult people on a dry city sidewalk. On the left, an adult woman in a mustard yellow coat holds a folded black umbrella in her right hand and looks at the man. On the right, an adult man in a dark blue jacket is holding a white paper coffee cup in his left hand and points toward a small red bicycle parked between them. A lit storefront is behind the pair, with a tree in the distant background. Keep left/right identities, hand-object relationships and the number of people correct. Natural anatomy, believable perspective and coherent dusk lighting.

### T11｜服装改色 / 不改款式（F03，润色：ON）
素材：A02；尺寸：720×1280；Seed：9627。

In <ref_image_0>, change only the original black dress into a deep emerald-green dress. Keep exactly the same garment cut, neckline, seam placements, sleeves, length, wrinkles, texture and fit; recolor fabric consistently, including areas in shadow. Preserve the adult woman’s face, hair, skin tone, body proportions, posture, shoes, background objects, camera angle and lighting. The output should clearly show the original dress design in the new color rather than a redesigned outfit.

### T12｜服装改色 / 不改款式（F04，润色：ON）
素材：A02；尺寸：720×1280；Seed：9627。

In <ref_image_0>, change only the original black dress into a deep emerald-green dress. Keep exactly the same garment cut, neckline, seam placements, sleeves, length, wrinkles, texture and fit; recolor fabric consistently, including areas in shadow. Preserve the adult woman’s face, hair, skin tone, body proportions, posture, shoes, background objects, camera angle and lighting. The output should clearly show the original dress design in the new color rather than a redesigned outfit.

### T13｜金属耳饰换花朵 / 小范围保留（F03，润色：OFF）
素材：A01；尺寸：1024×1024；Seed：9628。

In <ref_image_0>, replace the original large gold dangling earring on the visible ear with one small elegant white five-petal flower-shaped earring, attached naturally at the same earlobe position. The original gold metal ornament must disappear completely. Maintain the woman’s facial identity, ear anatomy, hairstyle, skin texture, eyes, nose, mouth, clothing, camera framing, color grading, shadows and background. Do not add a flower to the hair or cheek. Only the earring design should change.

### T14｜金属耳饰换花朵 / 小范围保留（F04，润色：OFF）
素材：A01；尺寸：1024×1024；Seed：9628。

In <ref_image_0>, replace the original large gold dangling earring on the visible ear with one small elegant white five-petal flower-shaped earring, attached naturally at the same earlobe position. The original gold metal ornament must disappear completely. Maintain the woman’s facial identity, ear anatomy, hairstyle, skin texture, eyes, nose, mouth, clothing, camera framing, color grading, shadows and background. Do not add a flower to the hair or cheek. Only the earring design should change.

### T15｜人物改姿态 / 保持身份（F03，润色：ON）
素材：A03；尺寸：720×1280；Seed：9629。

In <ref_image_0>, show the same adult man seated naturally on a simple wooden chair placed in the same studio, while keeping his recognizable facial features, exact hairstyle, gray jacket, white shirt, dark trousers and shoes. His posture is relaxed, both hands rest naturally on his thighs and his feet touch the floor. Maintain the original camera perspective, realistic anatomy, facial identity, lighting direction, floor and studio background. Do not change the jacket color, age, identity or room design.

### T16｜人物改姿态 / 保持身份（F04，润色：ON）
素材：A03；尺寸：720×1280；Seed：9629。

In <ref_image_0>, show the same adult man seated naturally on a simple wooden chair placed in the same studio, while keeping his recognizable facial features, exact hairstyle, gray jacket, white shirt, dark trousers and shoes. His posture is relaxed, both hands rest naturally on his thighs and his feet touch the floor. Maintain the original camera perspective, realistic anatomy, facial identity, lighting direction, floor and studio background. Do not change the jacket color, age, identity or room design.

### T17｜场景物体替换 / 光影一致（F03，润色：ON）
素材：A04；尺寸：1280×720；Seed：9630。

In <ref_image_0>, replace the dark ceramic coffee mug located on the wooden table with one clear cylindrical glass vase containing exactly three white tulips. Put the vase at the mug’s original position and scale, standing naturally on the tabletop with a believable contact shadow, accurate glass reflections and stems visible through the water. Completely remove the original mug. Keep the rest of the room, table grain, surrounding objects, viewpoint, crop and illumination unchanged.

### T18｜场景物体替换 / 光影一致（F04，润色：ON）
素材：A04；尺寸：1280×720；Seed：9630。

In <ref_image_0>, replace the dark ceramic coffee mug located on the wooden table with one clear cylindrical glass vase containing exactly three white tulips. Put the vase at the mug’s original position and scale, standing naturally on the tabletop with a believable contact shadow, accurate glass reflections and stems visible through the water. Completely remove the original mug. Keep the rest of the room, table grain, surrounding objects, viewpoint, crop and illumination unchanged.

### T19｜招牌文字精确修改（F03，润色：OFF）
素材：A05；尺寸：1152×864；Seed：9631。

In <ref_image_0>, replace only the word "OPEN" on the main storefront sign with the exact uppercase text "AI-KSK". Keep the sign’s original position, size, color palette, typographic style, lighting, shadow and surrounding border. The new lettering must be legible, evenly spaced and spelled A I hyphen K S K, without extra or missing characters. Preserve every other part of the storefront and street scene, including doors, windows, reflections and camera angle.

### T20｜招牌文字精确修改（F04，润色：OFF）
素材：A05；尺寸：1152×864；Seed：9631。

In <ref_image_0>, replace only the word "OPEN" on the main storefront sign with the exact uppercase text "AI-KSK". Keep the sign’s original position, size, color palette, typographic style, lighting, shadow and surrounding border. The new lettering must be legible, evenly spaced and spelled A I hyphen K S K, without extra or missing characters. Preserve every other part of the storefront and street scene, including doors, windows, reflections and camera angle.

### T21｜双参考 / 脸和衣服（F05，润色：N/A）
素材：A01 + R02；尺寸：1152×864；Seed：9727。

Produce a realistic half-body studio fashion portrait. Use the adult woman’s facial identity and hairstyle from <ref_image_0> as the identity reference, and use the cut, color, fabric and seam details of the jacket shown in <ref_image_1> as the garment reference. Dress the same identifiable woman in that jacket in a neutral softly lit studio. Keep facial anatomy faithful to the first reference, do not copy a mannequin or any person from the clothing reference, and integrate the garment with natural folds and shadows.

### T22｜三参考 / 脸衣服场景（F05，润色：N/A）
素材：A01 + R02 + R03；尺寸：1280×720；Seed：9728。

Create one coherent fashion editorial photograph of the adult woman from <ref_image_0> wearing the complete outfit from <ref_image_1> inside the architectural setting shown in <ref_image_2>. Preserve the woman’s recognizable facial proportions and hairstyle from reference zero, the exact clothing colors and silhouette from reference one, and the essential furniture placement and illumination of the background from reference two. Make perspective, body scale, floor contact and shadows coherent. Do not merge faces or import unwanted objects from the clothing photograph.

### T23｜三参考 / 双人身份和场景（F05，润色：N/A）
素材：A01 + R05 + R03；尺寸：1280×720；Seed：9729。

Create a natural wide photograph with exactly two adult people: the woman from <ref_image_0> stands on the left and the man from <ref_image_1> stands on the right, meeting in the environment shown in <ref_image_2>. Preserve each person’s own facial identity, hairstyle and general clothing identity separately; do not swap or blend their faces. Both people should have correctly formed hands and believable ground contact, and the background layout, lighting and perspective should closely follow the scene reference. Show a calm conversation, not an embrace.

### T24｜四参考 / 人衣景道具（F05，润色：N/A）
素材：A01 + R02 + R03 + R04；尺寸：720×1280；Seed：9730。

Create a full-body commercial fashion photograph of the woman from <ref_image_0> dressed in the jacket and trousers from <ref_image_1>, standing in the location shown in <ref_image_2>, holding the single tan leather travel bag from <ref_image_3> in her right hand. Preserve facial identity, the exact clothing design, recognizable location geometry and the bag’s silhouette and color. The person must be correctly scaled to the setting; the bag should make natural contact with the hand. Do not borrow faces or clothing from non-identity references.

### T25｜单框替换大物体 / 入门（F06，润色：N/A）
素材：A04；尺寸：1280×720；Seed：9827。

In <ref_image_0>, replace the ceramic mug located at <obj_1> with a clear glass vase containing three white tulips. The object must occupy the specified bounding box on the tabletop, matching the existing perspective, contact shadow, light direction and scene style. Remove the original mug and keep the rest of the photograph, furniture and camera angle as close as possible to the reference.

### T26｜单框耳饰替换 / 精准度挑战（F06，润色：N/A）
素材：A01；尺寸：1024×1024；Seed：9828。

In <ref_image_0>, replace the large golden earring at <obj_1> with one small white five-petal flower-shaped earring. The flower must be physically attached to the visible earlobe within the specified bounding box, not placed on the cheek or in the hair. Remove the original golden earring entirely. Preserve the model’s recognizable face, skin texture, hairstyle, blouse, light and background. This is a localized object instruction, not a request to reposition the whole person.

### T27｜双框布局 / 左右分置（F06，润色：N/A）
素材：A04；尺寸：1280×720；Seed：9829。

In <ref_image_0>, place a small white ceramic vase containing two yellow flowers at <obj_1> on the left area of the tabletop, and one closed dark-blue hardcover book at <obj_2> on the right area. Respect the two non-overlapping target regions and the correct left-right order. Each object must have natural perspective, correct scale and contact shadows. Keep the room, table, camera framing and lighting consistent with the reference image; do not create additional copies of either object.

### T28｜三框综合布局 / 空间控制（F06，润色：N/A）
素材：A06；尺寸：1280×720；Seed：9830。

In <ref_image_0>, arrange a single modern beige armchair at <obj_1> in the left foreground, one slender black floor lamp at <obj_2> in the right middle ground and one medium green potted plant at <obj_3> beside the far wall. Respect the specified spatial positions, relative sizes, object counts and depth order. Keep walls, window geometry, floor materials and daylight direction as close as possible to the reference image. Avoid overlapping objects or extra chairs, lamps or plants.

### T29｜结果汇总板（F07，润色：N/A）
素材：T01–T10结果；尺寸：按原图；Seed：—。

不调用生图提示词；从已有输出构建对照板，展示图像与参数、原图、耗时。

### T30｜结果汇总板（F07，润色：N/A）
素材：T11–T28结果；尺寸：按原图；Seed：—。

不调用生图提示词；从已有输出构建对照板，展示图像与参数、原图、耗时。

## 四、输入图素材生成提示词（后续生成，不是现在已生成）

素材须在编辑/多参考对照组之间共享，绝不能临时替换源图。

### A01｜方形清晰人像与金耳饰｜1:1
生成：单人成人女性，正面略偏侧、可见单侧耳朵、硕大的金色吊坠耳饰、耳饰和脸缘没有遮挡、素色上衣、干净室内背景。

A realistic close-up three-quarter portrait of an adult woman with natural skin texture, dark hair tucked behind one ear, and one clearly visible large gold dangling metal earring. The ear and ornament are unobstructed; both eyes, nose and mouth are sharp. Simple teal blouse, soft neutral studio background, diffused daylight and believable pores. No flowers, no extra jewelry, no lettering.

### A02｜全身黑色连衣裙｜9:16
生成：全身成年女性穿黑裙，裙子完整可见，不要外套、花纹或大面积阴影。

Full-length straightforward editorial photograph of an adult woman wearing a solid black midi dress with visible sleeves, neckline, seams and folds. Both feet in neutral shoes are entirely visible. Plain bright studio backdrop, natural human proportions, even daylight, no coat, no printed patterns, no jewelry drawing attention from the dress.

### A03｜站姿男性与工作室｜9:16
生成：男模全身站立，灰外套、白上衣、深色裤，留旁边椅子空间，方便改坐姿。

Full-body documentary studio photograph of one adult man in a medium-gray casual jacket, plain white shirt, dark trousers and dark shoes. He stands naturally on a clean pale floor, facing three-quarters toward the camera. A simple wooden chair is visible beside him with ample clear space. Lighting is soft and directional, facial features clear, no one else in frame.

### A04｜桌上深色马克杯｜16:9
生成：深色马克杯放在木桌左侧，桌面右边留白，利于物体替换和框选。

Wide realistic interior photo of a bright minimalist kitchen dining corner. A single dark ceramic coffee mug sits on the left half of a large wooden table. The right half of the table is intentionally empty and clear. Soft daylight enters from the left, consistent tabletop grain, simple blurred background, no flowers, no vase, no books, no people.

### A05｜OPEN商店招牌｜4:3
生成：干净店铺门面，中央明显英文OPEN字样，方便测试改文字。

Realistic straight-on photograph of a small contemporary neighborhood shop facade. Above the glass entrance is one large rectangular black sign displaying the clearly readable uppercase word OPEN in simple white sans-serif letters. No other text anywhere. Even daylight, straight architectural lines, visible doorway and windows, clean simple composition.

### A06｜空旷极简客厅｜16:9
生成：空客厅，地板和墙面有明显透视，中间留空供三框摆家具。

Wide clean photograph of a largely empty contemporary living room with pale plaster walls, wood flooring, a large window on the left and soft consistent natural daylight. The room contains no chair, no lamp and no plant, leaving empty areas in the foreground and beside the far wall. Architectural perspective and floor boundary are clear.

### R02｜服装参考 / 外套与长裤｜4:3
服装平铺或人台，无面部，便于确认身份究竟来自R01。

High-resolution catalog product photograph of a tailored cobalt blue cropped jacket and matching straight trousers displayed on a featureless dress form without a human head or face. Seam lines, fabric texture, collar, front closures and garment silhouette clearly visible. Neutral gray seamless background, even studio lighting and no brand labels.

### R03｜场景参考 / 城市广场｜16:9
空旷广场、建筑轮廓和地平线明显，可用于2人和多参考融合。

Realistic wide daytime photograph of a quiet modern pedestrian plaza with geometric stone paving, a low planter, several trees and distinctive glass-and-brick buildings. Correct straight architectural perspective, no people, no vehicles and enough open foreground space for fashion models.

### R04｜道具参考 / 棕色旅行包｜4:3
单独清晰旅行手袋，无logo、无人手、无复杂背景。

Commercial catalog photo of one tan brown leather travel handbag with two sturdy handles, simple brass buckles and a distinctive rectangular silhouette. Three-quarter angle on a neutral pale background, clean realistic texture and shadows, no logos, no people or hands.

### R05｜双人测试 / 男性身份参考｜1:1
独立成年男性脸部清晰肖像，不能与A01相似。

Realistic head-and-shoulders portrait of an adult man in his thirties with short slightly wavy black hair, clean-shaven face, distinct angular jaw and a neutral dark blue overshirt. Even natural window lighting, plain soft background, direct gaze, anatomically normal face and clear identity details.

## 五、F06 Bounding Box 手动画框说明

Bounding Box节点的元素字段写对象短描述，主提示词由Flux3LayoutPrompt输出，不要把坐标JSON手写进文本。首框=obj_1，第二框=obj_2；Nodes2.0显示画布后绘制。框仅布局引导、非Mask。

### T25｜画布1280×720，参考图A04

- obj_1 desc = `clear glass vase with three white tulips`；框位置：左侧木桌原马克杯范围，约x=20–43%, y=46–85%

百分比仅示意；图片实际目标位置以导入画布后人工目测定位为准，不保证自动坐标适配。

### T26｜画布1024×1024，参考图A01

- obj_1 desc = `small white five-petal flower-shaped earring`；框位置：贴耳垂上的金色耳饰周边，尽量不包含眼睛、嘴或头发

百分比仅示意；图片实际目标位置以导入画布后人工目测定位为准，不保证自动坐标适配。

### T27｜画布1280×720，参考图A04

- obj_1 desc = `white ceramic vase with two yellow flowers`；框位置：左桌面，约x=18–37%, y=45–80%
- obj_2 desc = `one closed navy hardcover book`；框位置：右桌面，约x=61–81%, y=59–78%

百分比仅示意；图片实际目标位置以导入画布后人工目测定位为准，不保证自动坐标适配。

### T28｜画布1280×720，参考图A06

- obj_1 desc = `one modern beige armchair`；框位置：左前景，约x=12–37%, y=45–92%
- obj_2 desc = `one slender black floor lamp`；框位置：右中景，约x=71–82%, y=19–86%
- obj_3 desc = `one medium green potted plant`；框位置：靠远墙中右，约x=52–68%, y=48–81%

百分比仅示意；图片实际目标位置以导入画布后人工目测定位为准，不保证自动坐标适配。

## 六、推荐的测试执行与评分规范

两个主模型分别按官方推荐设置比较：Base=50步/CFG3.5；Distilled=16步/CFG1。主线属于推荐配置对比，不是同等算力对比。

每组记录：原图ID、原Prompt、Upsampler实际展开文本、Seed、宽高、模型文件、采样器、调度器、步数、CFG、纯采样耗时、端到端耗时、最大显存、最终PNG。

人工评分（1–5，按适用项）：画质、提示词遵循、手部/脸部、文本准确率、编辑对象命中、原图不变区域稳定度、多图来源保持、布局遵循。无人类可判质量分时保持空白，不要自动冒充客观评级。

F07汇总板 T29/T30 不另算出图次数；所有例子仅一轮得到28幅图片，建议再按种子做重复测试以研究稳定性，重复出图次数单独记账。

## 七、异常及验收提醒

- 在官方原文件备份外操作。F03/F04 原JSON中 TextGenerate的upsampler文件仍是旧`..._int8_convrot.safetensors`，现服务器有 `..._w4a8.safetensors`，运行副本需统一引用。
- F05原文件只有两张参考图实际接入，T22–T24必须复制已有LoadImage（不新增技术节点）并连接对应动态槽位。
- F06上传的bbox示例为耳饰，且画布1376×752；各测试组需分别更换背景图及宽高，不能拿一张耳饰框兼用。
- F07 JSON有自己的额外采样节点，且Base为25步，若选“汇总优先”应直接使用F01–F06生成的结果，而不是重复执行F07；独立F07实验单独列出。
- 28个独立出图分支若一次排队执行，显存和时长可能失控；建议分批排队、独立保存，别让同时载入Base/Distilled造成OOM。
- 本表只是策略、素材与Prompt设计，未执行真实GPU推理。
