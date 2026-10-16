# AI-KSK FLUX 3 Image Klein Prompting Skill

[中文](#中文说明) · [English](#english)

> **Community-authored skill; not an official Black Forest Labs or ComfyUI release.**
>
> 本仓库是 AI-KSK 提示词与教学评测技能；不包括 FLUX 模型权重、第三方生成图片、API Token 或用户私有测试输出。

## 中文说明

面向 **FLUX 3 Image Klein Base / Distilled** 的跨 Agent 提示词技能。按照 [Agent Skills specification](https://agentskills.io/specification) 组织：根目录 `SKILL.md`、`references/`、`assets/`、`scripts/`。

**支持：** 文生图、单图编辑、至多10图参考融合、ComfyUI Bounding Box、提示词增强器四种模式、Base/Distilled公平横评，以及自选的3072×4096/15组4K压力测试。

**1.1.0改动：**
- 修正“关闭PUP”措辞：未扩写短提示词不应作为正常生成推荐；完整且已校准的Caption可避免再次随机扩写。
- BBox增加硬性验收：无有效`editor_state`/`bboxes`时不得称为框选控制通过。
- 加入用户最终15组 **PUP ON** 与3:4 `3072×4096`测试口径；声明是自选压力配置而非保证硬件可跑。
- 区分T2I和EDIT的PUP输入、F01–F04实际开关接线、精确文字与多人参考。
- 完善GitHub发布资料、数据和静态测试工具。

### 安装

克隆仓库或解压到你的 Agent Skills 根目录，并保证技能文件夹名为 `flux3-klein-prompting`。例如：

```bash
mkdir -p ~/.agents/skills
cp -a flux3-klein-prompting ~/.agents/skills/
python3 ~/.agents/skills/flux3-klein-prompting/scripts/validate_skill.py
```

Agent 是否自动发现/启用技能，取决于具体客户端；如果没有自动发现，请显式读取 `SKILL.md`。

### 本地验证

```bash
python3 scripts/validate_skill.py
python3 -m unittest discover -s tests -v
python3 scripts/lint_prompt.py --mode t2i --file examples/t2i_portrait.txt --caption-ready
python3 scripts/audit_workflow.py /path/to/your_15_group_workflow.json --expect-4k15
```

`audit_workflow.py`是结构检测，不运行GPU；是否真实完成4K生成需另看结果图尺寸、日志及显存。

### 目录

- `SKILL.md`: agent执行规范
- `references/`: 官方机制、PUP、BBox、4K、横评与经验
- `assets/`: 30组与15组测试方案、模板及参考素材提示词（不含模型权重）
- `scripts/`: 格式/提示词/工作流静态验证
- `examples/`: 可直接复制的Prompt
- `LICENSE` / `NOTICE` / `LICENSE_DECISION.md`: 许可与第三方边界
- `RELEASE_NOTES.md`: 更新说明

### 许可

本仓库 AI-KSK 原创内容采用 **Apache-2.0**（见 `LICENSE`），署名与第三方排除范围见 `NOTICE`，决定记录见 `LICENSE_DECISION.md`。

**该许可不覆盖**：FLUX 3 模型权重（BFL 采用 **FLUX Kommunity License**，与本仓库不是同一许可体系，且不随仓库分发）、BFL 参考代码、提示词增强器、ComfyUI 及其自定义节点、任何第三方图片或生成结果。不要复制 BFL 许可文字来冒充本技能许可。

## English

Community-maintained Agent Skill for writing full-scene captions for FLUX 3 Image Klein. Handles text-to-image, reference-guided edits, up to ten references, ComfyUI bounding boxes, prompt upsampling, quality benchmarking, and 4K stress-test planning. Built-in validators do **not** execute inference. See `SKILL.md`, `references/`, and `GITHUB_PUBLISH_TASK.md`.
