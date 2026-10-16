# 分任务提示词架构与可直接复用示例

## 统一caption组成
依照模型官方范式，优先写自然英文段落，不写纯标签串。一个句段中尽量按此顺序覆盖：
`MEDIUM + MAIN SCENE + SUBJECT COUNT/IDENTITY + APPEARANCE/ACTION + FOREGROUND/MIDGROUND/BACKGROUND + COMPOSITION/CAMERA + LIGHT + MATERIAL/COLOR + EXACT TEXT + PRESERVATION`。

不是必须机械填满每项，反而应突出该题目的约束。描述在图像中可见的事实，不要暗示模型执行不可见的算法或“精确像素锁定”。

## T2I：人像（皮肤自然）
**输入短请求**：自然皮肤的真实青年女性人像。
**完整caption**：
> Editorial color photograph of an adult woman in her late twenties, framed from chest to head at eye level. She has a naturally proportioned oval face, slight facial asymmetry, visible pores, and dark brown shoulder-length hair with fine individual strands. A plain cream knit top and small silver earrings provide restrained styling. She looks slightly to the left of the lens. Soft window light enters from camera-right, shaping believable shadows along the jaw and cheekbones. The background is a softly out-of-focus muted green interior. Realistic skin color and fabric texture, subtle photographic grain, no artificial plastic-skin finish.

## T2I：完整身体（防手脚异常）
> Full-body editorial fashion photograph of one adult woman standing on a pale stone walkway, both feet fully visible within the frame. She wears a structured navy jacket, straight cream trousers and low-heeled brown shoes, holding one black handbag in her right hand while her left hand rests naturally beside her body. Natural hands with five fingers each, realistic limb proportions, a clear gap between both arms and torso. Camera at waist level, 50 mm perspective, soft cloud-filtered daylight, quiet architectural background.
说明："five fingers" 是希望，不是结构上能保证。

## T2I：精确文字 / 多语言
> Minimalist product advertising photograph of one matte white aluminum bottle standing upright on a pale stone pedestal. The front label contains exactly two readable lines: "AI-KSK" on the first line and "新品上市" on the second line. Keep all letters and Chinese characters exactly as written, without additional words or logos. Dark navy sans-serif text centered on the bottle, controlled soft studio reflections, warm gray backdrop, one folded neutral linen cloth at left. Three-quarter view, crisp but natural surface texture.
建议：已是完整caption可OFF；评价时逐字核验，不保证100%成功。短请求使用PUP可能改写字体/版式，需比较实际最终caption。

## EDIT：改服装颜色，不改版型
> In <ref_image_0>, the same adult woman remains in the same full-body standing pose, with the same face, hairstyle, facial expression, and background composition. Her dress is now a rich emerald green while retaining its original silhouette, neckline, seams, folds, and fabric sheen. Lighting direction, shadows, shoes and accessories remain consistent with the reference. A natural editorial fashion photograph of the unchanged scene except for the dress color.
注意：保留项是目标，不是硬像素锁定。

## EDIT：耳饰 → 五瓣白花
> In <ref_image_0>, the same woman appears in the original close-up composition, with the identical visible face, hairstyle, skin texture and turquoise clothing. The large gold dangling earring on her visible ear is replaced by a single elegant white five-petal flower-shaped earring attached naturally to the earlobe; the original gold earring is absent. The photo keeps the original head pose, soft light, background color and camera perspective. No other accessories are added.
框选版在“visible ear”处加入 `<obj_1>` 并把 `desc` 填为 `white five-petal flower-shaped earring`。只做单图编辑时不必强加 `<obj_1>`。

## MULTI_REF：两张/三张/四张
> One coherent editorial full-body photograph of the same adult woman from <ref_image_0>, preserving her recognizable face, skin tone, and expression. She wears the navy jacket and cream trousers shown in <ref_image_1>, keeping the outfit's cut and material. She stands in the open stone plaza seen in <ref_image_2>, framed at eye level with natural perspective. Match the daylight and shadows to the plaza, with realistic fabric drape and anatomically plausible hands. No additional people.
若仅两图，删除第三张的环境来源并明确用中性背景；四图可添加 `<ref_image_3>` 的道具。不能把参考图视为独立控制层的硬绑定，需对串图做实测。

## LAYOUT_T2I：两框新构图
> A clean modern interior photograph with a slim ceramic floor lamp <obj_1> to the right and a green potted plant <obj_2> to the left. The space is uncluttered with warm white walls, a light oak floor, and soft daylight from a window outside the frame. Balanced architecture and plausible physical scale.
接 `Flux3LayoutPrompt`，在 `CreateBoundingBoxes` 放框并填写 `desc`；例如 obj_1: `slim white floor lamp`, obj_2: `green potted plant`. `Flux3LayoutPrompt` 自动附加结构化JSON。

## LAYOUT_EDIT：杯子变花瓶
> In <ref_image_0>, the same wooden table and minimalist room remain under the original soft window light. At the area marked <obj_1>, the old ceramic mug has been replaced by one clear glass vase holding exactly three white tulips. The vase rests naturally on the tabletop with accurate contact shadow and reflections. Preserve the wall, table grain, furniture, and camera angle elsewhere.
框 `desc` 应描述**目标结果**：`clear glass vase with exactly three white tulips`，不要仍写 `mug`。原图需走参考图编辑链。

## STYLE：用属性而非模仿某作品
> A hand-painted illustration with matte gouache color fields, softly uneven brush edges, restrained warm-cool contrast, simplified shapes, and delicate paper texture. The scene shows [subject/action], with [foreground] and [background] under [lighting]. Keep the silhouette readable and avoid busy decorative marks.

## 避免混写
- 把 `<ref_image_0>` 只用于有参考输入的工作流。
- 把 `<obj_1>` 只用于实际提供了对应元素的框选任务；无对应 box 的 ID 是悬空引用。
- 若有 Logo / 数字 / 文字，需要双引号逐字复制，严禁让 PUP 擅自改写后继续声称“原始文字控制测试”。
- 不写“保持完全相同像素”这种不受框控机制支持的承诺。
