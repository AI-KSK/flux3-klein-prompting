#!/usr/bin/env python3
"""Validate local public skill layout/data. Does not use a GPU or network."""
from pathlib import Path
import json, re, sys
ROOT=Path(__file__).resolve().parent.parent
REQUIRED = [
'SKILL.md','README.md','RELEASE_NOTES.md','LICENSE','NOTICE','LICENSE_DECISION.md',
'references/official-mechanics.md','references/prompt-patterns.md',
'references/bounding-box-workflow.md','references/upsampler-and-comparison.md',
'references/4k-stress-and-style.md','references/empirical-notes.md','references/sources.md',
'assets/30_cases.source.json','assets/30_cases.skill_review.json',
'assets/15_style_prompts.original.json','assets/15_4k_run_config.json',
'scripts/lint_prompt.py','scripts/audit_workflow.py']
for rel in REQUIRED:
    assert (ROOT/rel).is_file(),f'Missing {rel}'
for x in ROOT.rglob('*.json'):json.loads(x.read_text(encoding='utf-8'))
txt=(ROOT/'SKILL.md').read_text(encoding='utf-8');assert txt.startswith('---\n')
head=txt.split('---',2)[1]
name=re.search(r'^name:\s*(\S+)',head,re.M).group(1)
assert re.fullmatch('[a-z0-9]+(?:-[a-z0-9]+)*',name) and len(name)<=64, (
    f'SKILL.md frontmatter name must be lower-kebab-case and <=64 chars, got {name!r}')
assert name==ROOT.name, (
    f'Skill folder is named {ROOT.name!r} but SKILL.md declares name: {name!r}. '
    f'The Agent Skills specification requires the folder name to match the skill name. '
    f'Rename this folder to {name!r} (for example: git clone <repo-url> {name}) and re-run.')
m=re.search(r'^description:\s*(.*)',head,re.M)
assert m and 1<=len(m.group(1))<=1024
for rel in re.findall(r'\]\((references/[^)]+|assets/[^)]+|scripts/[^)]+)\)',txt):
    assert (ROOT/rel).exists(),f'Broken skill link: {rel}'
d=json.loads((ROOT/'assets/30_cases.source.json').read_text(encoding='utf-8'))
assert len(d['cases'])==30 and len({c['编号'] for c in d['cases']})==30
v=json.loads((ROOT/'assets/30_cases.skill_review.json').read_text(encoding='utf-8'))
assert len(v['cases'])==30
styles=json.loads((ROOT/'assets/15_style_prompts.original.json').read_text(encoding='utf-8'))
run=json.loads((ROOT/'assets/15_4k_run_config.json').read_text(encoding='utf-8'))
assert len(styles)==len(run['cases'])==15
assert {c['id'] for c in styles}=={c['id'] for c in run['cases']}
assert all(c['width']==3072 and c['height']==4096 and c['enable_prompt_upsampler'] is True for c in run['cases'])
# Very conservative checks for common leaked tokens; deliberately do not print matches
for path in ROOT.rglob('*'):
    if not path.is_file() or path.suffix not in ('.md','.py','.yml','.json','.txt','.csv'):continue
    t=path.read_text(encoding='utf-8')
    # Regex split construction prevents false matching this code itself
    patterns=[r'(?<![A-Za-z0-9])'+'hf_'+'[A-Za-z0-9]{24,}',r'(?<![A-Za-z0-9])'+'ghp_'+'[A-Za-z0-9]{24,}',r'(?<![A-Za-z0-9])'+'github_pat_'+'[A-Za-z0-9_]{30,}',r'(?<![A-Za-z0-9])'+'sk-'+'[A-Za-z0-9_-]{30,}']
    assert not any(re.search(x,t) for x in patterns),f'Potential secret in {path.relative_to(ROOT)}'
print('PASS: skill spec, references, 30+15 cases, 4K ON configuration, basic secret scan')
