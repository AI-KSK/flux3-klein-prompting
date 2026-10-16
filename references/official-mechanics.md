# 官方机制｜已验证事实与注意事项

来源详情见 [sources.md](sources.md)，以下源于 BFL 官方模型卡、推理仓库、Prompt Upsampler 模型卡和 Hugging Face Diffusers 官方文章。这里的“官方默认”特指 BFL 推荐，而不代表任何用户本地 JSON 必然采用该设置。

1. FLUX 3 Image Klein 是统一的 T2I / image edit / multi-reference / layout 模型。官方最多10张参考图片。使用 Qwen3-VL-4B-Instruct 做文本编码器；5.6B是图像变换器参数量，不包括文本编码器。
2. Base = 未蒸馏，官方推荐50步、CFG3.5；Distilled = 蒸馏16步、不使用额外guidance（Comfy KSampler 接线可能用 CFG=1 的等效实现）。实际速度/画质需要硬件实测。
3. 模型预期输入不是短关键词，而是**full scene caption**。官方提示词增强器是一套 Qwen3.5-9B 视觉语言模型，负责把短请求+可选参考图+可选框扩写为完整描述。可用等效 LLM 按官方 system_prompts.json 方式代替；已预先完成等效扩写的完整caption无需二次随机扩写，但未经扩写的短词直接投模型并非官方推荐。
4. 提示词描述应包括：图像媒介、风格、画面主次与构图、主体身份外观与动作、清晰位置、背景/环境、材质、光影、需准确显示的文本。编辑caption应表述**编辑后的整张图是什么样**，并纳入需保留的原图内容。
5. PUP 的官方四类模式：`t2i`、`i2i`、`t2i_bbox`、`i2i_bbox`。提示词增强对编辑应访问参考图；不能把不看图的纯文本扩写看成相同功能。系统提示词的官方文件链接：https://huggingface.co/black-forest-labs/flux-3-image-klein-pup/blob/main/system_prompts.json
6. `<ref_image_0>` 指第一张参考图，编号从0开始；输入列表顺序不是可交换的。纯文本指向对象时，描述该对象来自何图，并描述输出画面，不只下达“copy face”。
7. Box 是位置/缩放引导，不是强制 mask；原图参考也不是像素锁定。小元素可能没有出现，框外画面可能改变，需要显式测试与人工检查。
8. 在最终caption末尾添加结构化布局表的一般格式：`[{"id":"obj_1","bbox":[ymin,xmin,ymax,xmax],"desc":"..."}]`，比例是0至1000的归一化整数。BFL独立CLI的 `--boxes boxes.json` 又采用0至1浮点数；两者不是同一种直接输入。
9. 文本渲染支持但可能拼错、变形。需提供确切原文（引号内）、位置、字形、颜色、字号层级；尤其中文应逐字符人工核对。
10. 官方许可为 FLUX Kommunity License，商业使用/输出可能有额外条件；不得在教程中断言完全无限制商用。

## 本地模型文件名（仅参考用户提供的当前实例，不等于权重分类标准）
- Base: `flux3_image_klein_base_int8_convrot.safetensors`
- Distilled: `flux3_image_klein_sd_int8_convrot.safetensors`
- Text encoder: `qwen3vl_4b_int8_convrot.safetensors`
- Upsampler: `qwen3.5_9b_flux3_prompt_upsampler_w4a8.safetensors`
- VAE: `flux2-vae.safetensors`
- `flux3_image_klein_int8_convrot.safetensors` 是用户实例中Base的硬链接别名，不是第三套模型。
这些是服务器上已知名称，不要求提示词工作修改/下载/改名。软件架构版本不同可能节点选项不同，应检查实际工作流。

11. BFL官方披露**最高4K原生能力**，实际尺寸、内存与ComfyUI节点版本兼容性必须按任务实测；AI-KSK的3072×4096为自选压力测试，不是BFL统一推荐分辨率。
12. ComfyUI `CreateBoundingBoxes`若`editor_state`为空且`bboxes`无上游，按源码只能输出空元素；`Flux3LayoutPrompt`接到空数组时不会添加布局表。画面符合提示词不能冒充BBox有效。
