import sys, json, unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parent.parent
sys.path.insert(0,str(ROOT/'scripts'))
from lint_prompt import lint
from audit_workflow import audit
class Tests(unittest.TestCase):
    def test_refs(self):
        e,w=lint('In <ref_image_2>, a woman wears a blue jacket.', 'multiref',refs=2,caption_ready=True)
        self.assertTrue(e)
    def test_correct_ref(self):
        e,w=lint('In <ref_image_0>, the original face remains while the shirt is changed to blue.', 'edit',refs=1,caption_ready=True)
        self.assertFalse(e)
    def test_bbox_not_in_t2i(self):
        e,w=lint('A person at <obj_1> stands in a bright studio.', 'layout-t2i',boxes=0,caption_ready=True)
        self.assertTrue(e)
    def test_manifest(self):
        d=json.loads((ROOT/'assets/15_4k_run_config.json').read_text())
        self.assertEqual(len(d['cases']),15)
        self.assertTrue(all(x['enable_prompt_upsampler'] for x in d['cases']))
    def test_empty_bbox_is_warned(self):
        import tempfile
        data={'nodes':[{'id':1,'type':'CreateBoundingBoxes','inputs':[],'widgets_values_named':{'editor_state':[]}}],'links':[]}
        with tempfile.TemporaryDirectory() as p:
            path=Path(p)/'w.json';path.write_text(json.dumps(data))
            out=audit(path)
        self.assertTrue(out['warnings']);self.assertTrue(out['pass'])
if __name__=='__main__':unittest.main()
