# 来源索引与可信度（核对时间 2026-10-16）

## 第一手官方资料（优先）
1. Black Forest Labs ComfyUI model card（完整caption、最多10图、步骤/CFG、布局格式）：https://huggingface.co/black-forest-labs/flux-3-image-klein-comfy/blob/main/README.md
2. Black Forest Labs reference inference repository（CLI、PUP、0–1 boxes.json、GPU规则）：https://github.com/black-forest-labs/flux-3-image-klein
3. BFL official Prompt Upsampler model card（四模式、参考输入、英文caption）：https://huggingface.co/black-forest-labs/flux-3-image-klein-pup
4. 官方 system prompts（仅链接，**不在本技能包内转载系统提示词原文**）：https://huggingface.co/black-forest-labs/flux-3-image-klein-pup/blob/main/system_prompts.json
5. Hugging Face Diffusers 官方介绍（多参考、0–1000布局caption）：https://huggingface.co/blog/flux-3
6. ComfyUI 官方节点实现（`Flux3LayoutPrompt`）：https://github.com/Comfy-Org/ComfyUI/blob/master/comfy_extras/nodes_flux.py
7. ComfyUI 官方节点实现（`ReferenceMultiLatent`）：https://github.com/Comfy-Org/ComfyUI/blob/master/comfy_extras/nodes_edit_model.py
8. ComfyUI 官方节点实现（`CreateBoundingBoxes`）：https://github.com/Comfy-Org/ComfyUI/blob/master/comfy_extras/nodes_bounding_boxes.py
9. ComfyUI官方模板仓库：https://github.com/Comfy-Org/workflow_templates
10. Agent Skills开放格式规范：https://agentskills.io/specification

## 社区观察（证据等级较低；不能替代官方或本地复现）
11. Reddit /r/comfyui 首发讨论：https://www.reddit.com/r/comfyui/comments/1x6p7lt/flux_3_klein_releases_with_comfyui_built_models/
12. Reddit /r/StableDiffusion Base vs Distilled 本地对照：https://www.reddit.com/r/StableDiffusion/comments/1x6wgyt/flux_3_klein_base_vs_distilled_tested_locally/
13. Reddit /r/comfyui NVFP4社区样例：https://www.reddit.com/r/comfyui/comments/1x6x7s2/flux3_image_klein_nvfp4_tests_moonlit_sorceress/

## AI-KSK提供的工作资料（不是官方证据）
- `_workflows (4)(1).zip`：7套当前本地JSON，用于审查流程节点和实际开关接线。未含于本技能包，避免误把修改版标成官方原版。
- `FLUX3_Klein_AI-KSK_30组教学测评_完整提示词素材与评分_V1.zip`：此前约定的T01–T30方案。已复制核心数据到 `assets/` 并保留原样。

**证据纪律**：官方实现与官方模型卡 > 本地JSON可见接口 > 社区个别测试经验 > 本技能新增推理建议。任何GPU推理效果必须实测，不得仅凭提示词宣称通过。
14. Black Forest Labs 2026-10-15官方发布博客：https://bfl.ai/blog/flux-3-image-klein

15. BFL 2026-10-15 official release (native 4K headline): https://bfl.ai/blog/flux-3-image-klein
16. Agent Skills official specification (SKILL.md/frontmatter): https://agentskills.io/specification
17. BFL official FLUX general prompting skills (background reference; not copied): https://github.com/black-forest-labs/skills

**核验口径**：上述URL用于以后复核，官方模型卡和仓库在发布后仍会更新。本项目v1.1.0校准于2026-10-16。
