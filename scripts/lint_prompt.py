#!/usr/bin/env python3
"""Static linting for FLUX 3 Image Klein captions. Does not run inference."""
import argparse
import json
import re
import sys

TAG_REF = re.compile(r'<ref_image_(\d+)>')
TAG_OBJ = re.compile(r'<obj_(\d+)>')

def lint(prompt, mode, refs=0, boxes=0, caption_ready=False):
    errors, warnings = [], []
    prompt=prompt.strip()
    if not prompt: errors.append('提示词为空。');return errors,warnings
    ref_numbers=[int(x) for x in TAG_REF.findall(prompt)]
    obj_numbers=[int(x) for x in TAG_OBJ.findall(prompt)]
    if mode in ('t2i','layout-t2i') and ref_numbers:
        errors.append('纯文生图模式不能引用<ref_image_n>；如需参考图，请改用edit/multiref/layout-edit。')
    if refs<0 or refs>10:errors.append('BFL图像模型支持0-10张参考图。')
    if refs==0 and ref_numbers:
        errors.append('提示词引用了参考图，但refs=0。')
    for i in ref_numbers:
        if i>=refs:errors.append(f'引用<ref_image_{i}>，但提供的参考图只有{refs}张。')
    if mode in ('edit','multiref','layout-edit') and refs==0:
        errors.append('该任务必须有实际参考图，不能只写<ref_image_0>。')
    if mode in ('layout-t2i','layout-edit'):
        if boxes<=0:errors.append('布局模式应至少配置1个Bounding Box。')
        if not obj_numbers:warnings.append('布局模式未见<obj_n>引用，确认是否要在prompt内指定元素。')
        for i in obj_numbers:
            if i<1 or i>boxes:errors.append(f'引用了<obj_{i}>，但提供的框数是{boxes}。')
    elif obj_numbers:
        warnings.append('不是布局模式但出现<obj_n>；请确认下游真有Flux3LayoutPrompt与对应框。')
    if re.search(r'\b(8k|masterpiece|best quality|ultra detailed)\b', prompt, re.I):
        warnings.append('提示词含泛化画质堆词；优先写清主体、构图、材质和光线。')
    if len(prompt.split())<30 and not caption_ready:
        warnings.append('当前英文长度偏短；BFL推荐full scene caption或先经PUP扩写。')
    if re.search(r'\b(exactly the same pixels|pixel[- ]perfect|100% identical)\b',prompt,re.I):
        warnings.append('文本包含像素级保证措辞：BBox/编辑参考不能保证完全锁定。')
    # Optional trailing layout table, only if user manually embeds one.
    jstart=prompt.find('[{')
    if jstart!=-1:
        try:
            regions=json.loads(prompt[jstart:]);ids=[]
            for reg in regions:
                if not isinstance(reg,dict):errors.append('布局表元素应为JSON对象。');continue
                rid=reg.get('id'); ids.append(rid)
                bbox=reg.get('bbox')
                if not isinstance(bbox,list) or len(bbox)!=4 or not all(isinstance(x,(int,float)) for x in bbox):
                    errors.append(f'{rid}: bbox必须是4个数字的[ymin,xmin,ymax,xmax]。')
                    continue
                if not (0<=bbox[0]<bbox[2]<=1000 and 0<=bbox[1]<bbox[3]<=1000):
                    errors.append(f'{rid}: 坐标无效（仅适用于caption的0–1000坐标，CLI另用0–1）。')
            if len(set(ids))!=len(ids):errors.append('布局表存在重复ID。')
            if obj_numbers and not all(f'obj_{i}' in ids for i in obj_numbers):
                warnings.append('正文引用了不存在于手写布局表中的对象。')
            if mode in ('layout-t2i','layout-edit'):
                warnings.append('若使用ComfyUI Flux3LayoutPrompt，勿手写JSON表再由节点附加第二遍。')
        except json.JSONDecodeError:
            warnings.append('发现类似布局JSON，但不能解析；若是由Flux3LayoutPrompt动态生成，可忽略此提示。')
    return errors,warnings

def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--mode', choices=['t2i','edit','multiref','layout-t2i','layout-edit','benchmark'],required=True)
    one=p.add_mutually_exclusive_group(required=True)
    one.add_argument('--prompt')
    one.add_argument('--file')
    p.add_argument('--refs',type=int,default=0)
    p.add_argument('--boxes',type=int,default=0)
    p.add_argument('--caption-ready',action='store_true')
    a=p.parse_args()
    value=a.prompt if a.prompt is not None else open(a.file,encoding='utf-8').read()
    errs,warns=lint(value,a.mode,a.refs,a.boxes,a.caption_ready)
    for x in errs:print('ERROR:',x)
    for x in warns:print('WARN: ',x)
    print('RESULT:', 'FAIL' if errs else ('WARN' if warns else 'PASS'))
    return int(bool(errs))
if __name__=='__main__':sys.exit(main())
