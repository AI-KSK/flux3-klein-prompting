# Prompt Upsampler策略与公平横评

## 官方机制 vs AI-KSK测试策略
- **官方**：原始自然语言请求（含图像编辑）应先经 PUP 或等效LLM扩写为 full scene caption；四系统模式分别 `t2i`, `i2i`, `t2i_bbox`, `i2i_bbox`。对编辑，增强器应看见参考图。
- **测试策略（非官方强制）**：若已有经过人工完整编写的 caption，可以让图像模型直接读取这份文本，即关闭工作流中的**再次扩写**；若只有短请求，ON或先在独立流程中预扩写。
- **PUP A/B试验**要记录“原始请求”“PUP输出完整文本”“PUP耗时”“图像模型耗时”，不能把短提示词OFF失败直接归因模型本身差。
- **Base vs Distilled 同输入测试**不能各自通过随机/不同的 PUP 生成两段 caption 然后归咎模型；预扩写一次，锁定后两支复用。

## 统一开关映射（按用户2026-10-16上传JSON审计；非所有官方版本通用）
| 工作流 | 当前开关概况 | 注意 |
|---|---|---|
| F01 Base T2I, F02 Distilled T2I | 包含TextGenerate与ComfySwitchNode，在子图内 | 必须检查 Switch input 的真实 False/True 接线，不能仅从UI文案判断 |
| F03 Base Edit, F04 Distilled Edit | 包含TextGenerate、PrimitiveStringMultiline、ComfySwitchNode、LayoutPrompt等 | 该上传版的 switch `False` 为经过 TextGenerate 的路线，`True` 为直通原始提示词；导入后再次校验 |
| F05/F06 自定义增强 | 使用完整人工提示词，无PUP链 | 不应为了整齐强行添加TextGenerate |
| F07 原横评 | 只做模型两分支比较，不内置PUP | 建议喂同一份已锁定caption |

注意：`switch=True` 是哪路必须**看节点实际连线**，不能根据“True=开启增强”推断。统一导演台可以在外部标为 `Upsampler ON/OFF`，内部根据现有线路映射相反值。

## 官方推荐推理参数（不等于最终本地运行配置）
| 检查点 | Steps | Guidance/CFG | 比较方法 |
|---|---:|---|---|
| Base（undistilled） | 50 | CFG 3.5 | 官方推荐画质/性能基线 |
| Distilled | 16 | no guidance / 某些ComfyUI实现CFG=1 | 官方推荐速度/性能基线 |

1. 推荐设置横评：两支步数不同，结论应同时给质量与每图耗时；这是**同画面条件，不是同算力**。
2. 等步数/等时间横评：作为**独立实验**，避免混合进推荐设置排名。
3. 输出用完全相同的最终caption、Seed、尺寸、参考图顺序、裁切与版本；每类至少2–3个Seed检验稳健性。
4. T2I没有可依托的参考图，不要写 `<ref_image_0>`；编辑要实际输入图片而不只是引用标记。
5. 精确字符、包装、字体的对比不宜让两个分支扩写两次。原样引用字符串，记录是否漏字/错字/新增字。
6. 人工评分：细节真实、构图、提示词遵循、身体结构、编辑目标正确、原图保留、布局控制，多参考来源分辨度。性能：预处理/PUP与推理时间分离、峰值显存、失败率。

## 30组计划如何执行
- 用户原始 `assets/30_cases.source.json` 中的 `Upsampler建议` 是**原计划**，保留原样存档。
- `assets/30_cases.skill_review.json` 是技能审阅层：若给图像模型的输入已经是完整caption，建议 `final_caption_locked=true` 且当前图片模型入口 `upsampler_during_branch=OFF`；如果想做原始短请求的PUP/无PUP对照，请独立建立小样本A/B，不占用Base/Distilled的公平比较配额。
- OFF **绝不是**模型建议“永远不用Upsampler”。离线PUP已展开的caption→OFF是合理的。用户可以保留ON产生不同风格，但不归入同提示词对照。

## 2026-10-16 15组独立压力测试开关例外
用户最新确认15组插画S01–S15 **全部要开启 PUP**。此处以用户决定为准：子图顶层`switch=True`且子图的`on_true`应确实接TextGenerate输出；每次扩写会使最终Caption有变化，必须保存生成文本。**旧15组提示词包的Upsampler OFF是历史草案，不是最新运行选择。** 两模型横评时仍须锁定最终Caption后复用。
