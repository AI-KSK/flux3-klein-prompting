#!/usr/bin/env python3
"""Read-only static audit of ComfyUI workflow JSON, especially AI-KSK S01-S15 4K PUP ON."""
import argparse, json, sys, re
from pathlib import Path

def audit(path, expect_4k15=False):
    d=json.loads(Path(path).read_text(encoding='utf-8'))
    nodes=d.get('nodes', [])
    links=d.get('links', [])
    node_ids=[n['id'] for n in nodes]
    errors=[]; warnings=[]
    if len(node_ids)!=len(set(node_ids)): errors.append('Duplicate top-level node ids')
    node_map={n['id']:n for n in nodes}
    for link in links:
        if not isinstance(link,list) or len(link)<6:errors.append('Malformed top-level link');continue
        if link[1] not in node_map or link[3] not in node_map:errors.append(f'Dangling top-level link {link[0]}')
    saves=[n for n in nodes if n.get('type')=='SaveImage']
    bboxes=[n for n in nodes if n.get('type')=='CreateBoundingBoxes']
    for node in bboxes:
        w=node.get('widgets_values_named',{})
        has_state=bool(w.get('editor_state'))
        linked=any(x.get('name')=='bboxes' and x.get('link') is not None for x in node.get('inputs',[]))
        if not has_state and not linked: warnings.append(f"CreateBoundingBoxes node {node['id']} EMPTY; cannot claim box control")
    if expect_4k15:
        gen=[n for n in nodes if n.get('type')=='3301b744-2960-415a-83b0-fe8a89d99fdb']
        if len(gen)!=15:errors.append(f'Expected 15 Distilled subgraph instances, found {len(gen)}')
        if len(saves)!=15:errors.append(f'Expected 15 SaveImage nodes, found {len(saves)}')
        seeds=set()
        for n in gen:
            w=n.get('widgets_values_named',{})
            vals=n.get('widgets_values',[])
            on=w.get('switch', vals[1] if len(vals)>1 else None)
            if on is not True:errors.append(f"Instance {n['id']} PUP switch not True")
            width=w.get('width',vals[2] if len(vals)>2 else None)
            height=w.get('height',vals[3] if len(vals)>3 else None)
            if (width,height)!=(3072,4096):errors.append(f"Instance {n['id']} expected 3072x4096, got {width}x{height}")
            seed=w.get('seed',vals[4] if len(vals)>4 else None);seeds.add(seed)
            # No external width/height cables may override local widgets
            overrides=[x.get('name') for x in n.get('inputs',[]) if x.get('name') in ('width','height') and x.get('link') is not None]
            if overrides:errors.append(f"Instance {n['id']} width/height connected to upstream: {overrides}")
        if len(seeds)!=15:errors.append(f'Expected 15 distinct seeds, found {len(seeds)}')
        defs=d.get('definitions',{}).get('subgraphs',[])
        target=next((x for x in defs if x.get('id')=='3301b744-2960-415a-83b0-fe8a89d99fdb'),None)
        if not target: errors.append('Missing referenced subgraph definition')
        else:
            inner={n['id']:n for n in target.get('nodes',[])}
            switch_nodes=[n for n in inner.values() if n.get('type')=='ComfySwitchNode']
            if not switch_nodes:errors.append('Inner ComfySwitchNode missing')
            else:
                sw=switch_nodes[0]
                to_true=next((x.get('link') for x in sw.get('inputs',[]) if x.get('name')=='on_true'),None)
                lk=next((x for x in target.get('links',[]) if x.get('id')==to_true),None)
                if not lk:errors.append('Cannot trace on_true branch')
                elif inner.get(lk.get('origin_id'),{}).get('type')!='TextGenerate':
                    errors.append('Inner on_true NOT connected to TextGenerate')
    return {"path":str(path),"total_nodes":len(nodes),"saves":len(saves),"bbox_nodes":len(bboxes),"errors":errors,"warnings":warnings,"pass":not errors}

def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('json_file');p.add_argument('--expect-4k15',action='store_true')
    a=p.parse_args()
    result=audit(a.json_file,a.expect_4k15)
    print(json.dumps(result,indent=2,ensure_ascii=False))
    return 1 if result['errors'] else 0
if __name__=='__main__':sys.exit(main())
