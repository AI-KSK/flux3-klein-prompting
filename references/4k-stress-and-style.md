# 4K插画专项：S01–S15（2026-10-16最终口径）

## 官方能力与AI-KSK测试选择须分开
- BFL官方公开说明支持 **最高4K** 原生生成（见`references/sources.md`）；这是模型能力宣称，不是某个本地INT8 / CUDA / ComfyUI组合的无条件通过保证。
- **3072×4096、3:4、12,582,912像素**是本次插画测试的**自选目标尺寸**；不能当作官方唯一支持的4K长宽。
- 每一组的参考图来自用户截图，仅作为编写T2I Caption的目视语义参考；真正T2I生成时**不输入图像参考**。

## 15组确定配置
- 编号：S01–S15，保持原版15组场景Caption；对应见`assets/15_style_prompts.original.json`。
- 模型：`flux3_image_klein_sd_int8_convrot.safetensors`，16步（该次用户选择）；模型具体量化/组合仍按用户安装环境核实。
- 输出：3072×4096、3:4、种子9901–9915固定、每组独立SaveImage命名前缀。
- **用户最终已要求提示词润色全部开启**：本次 `enable_prompt_upsampler=True`，15/15。`ComfySwitchNode.on_true`需要确实接`TextGenerate`扩写输出。
- 模型要求：Qwen3-VL文本编码器、Flux2 VAE、Qwen3.5-9B PUP权重。用户实例选择过`qwen3.5_9b_flux3_prompt_upsampler_w4a8.safetensors`；其他实例可能用INT8 Convrot变体，文件名不通用。
- PUP扩写后必须保存15份最终Caption，否则后续对比仅有原始提示词无法复现完整输入。

## 正式验收分级
1. **静态**：JSON可解析，15个顶层生成实例，15个SaveImage接线，尺寸输入不被ResolutionSelector覆盖，种子与文本一致，PUP ON，内部True接扩写分支。
2. **快速**：只运行S01，采集真实PNG 3072×4096、执行耗时、显存峰值、异常栈；检查其保存的实际Prompt（如后端支持）。
3. **压力**：S01通过后逐个运行剩余14组。即使同一Queue启动，也可能OOM，需分组/串行调度。
4. **报告**：真实完成张数、失败张数、完整尺寸、PUP耗时、采样耗时、GPU、CUDA版本、OOM信息、后续是否做降分辨率对照。

**切忌：** GUI写3072×4096但链接覆盖宽高；把小图放大成4K并称原生4K；PUP ON不记录扩写文本；输出失败后暗中降低分辨率。
