from __future__ import annotations
import copy, unittest
from a9_methodology_flow import validate_methodology, expand_methodology_flows
from a9_semantic_checker import check_semantics

def example(n=6):
    src = {'project_id':'TEST_METHOD_ONLY','source_commit':'abc123','source_manifest_id':'TEST_MANIFEST','sources':[{'source_id':'METH-MANUSCRIPT','admission_status':'ADMITTED_CURRENT'}]}
    stages=[{'stage_id':f'M{i:02d}','title':f'Method stage {i}','description':'An actual procedure described by source.', 'output':'Traceable intermediate record','category':'ANALYSIS', 'manuscript_locator':'Chapter 3, section 3.3','evidence_refs':['METH-MANUSCRIPT']} for i in range(n)]
    content={'metadata':{'project_id':'TEST_METHOD_ONLY'},'slides':[{'type':'methodology_flow','scientific_role':'METHOD','title':'Research Methodology','layout':'horizontal_linear','direction':'left_to_right','stages':stages}]}
    return content,src

class MethodologyFlowTests(unittest.TestCase):
    def test_six_stages_semantic_pass(self):
        c,e=example(); self.assertTrue(check_semantics(c,e)['ok'])
    def test_bad_admission_rejected(self):
        c,e=example();e['sources'][0]['admission_status']='CANDIDATE';self.assertFalse(check_semantics(c,e)['ok'])
    def test_missing_locator_rejected(self):
        c,e=example();del c['slides'][0]['stages'][0]['manuscript_locator'];self.assertFalse(validate_methodology(c,e)['ok'])
    def test_duplicate_ids_rejected(self):
        c,e=example();c['slides'][0]['stages'][1]['stage_id']='M00';c['slides'][0]['stages'][0]['stage_id']='M00';self.assertFalse(validate_methodology(c,e)['ok'])
    def test_no_faked_confirmed_rework(self):
        c,e=example();c['slides'][0]['stages'][1]['output']='Confirmed rework cases';self.assertFalse(validate_methodology(c,e)['ok'])
    def test_connector_topology_rejected(self):
        c,e=example();c['slides'][0]['connectors']=[{'from':'M00','to':'M02'}];self.assertFalse(validate_methodology(c,e)['ok'])
    def test_unsupported_layout_rejected(self):
        c,e=example();c['slides'][0]['layout']='horizontal_swimlane';self.assertFalse(validate_methodology(c,e)['ok'])
    def test_pagination_seven_no_loss(self):
        c,e=example(7);ex=expand_methodology_flows(c)
        self.assertEqual([len(s['stages']) for s in ex['slides']],[6,1])
        self.assertEqual(ex['slides'][0]['title'],'Research Methodology (1/2)')
        self.assertEqual(ex['slides'][1]['stages'][0]['stage_id'],'M06')
    def test_researcher_evidence_map_required(self):
        c,e=example();self.assertFalse(validate_methodology(c,None)['ok'])
    def test_other_slide_types_unchanged(self):
        self.assertTrue(validate_methodology({'slides':[{'type':'bullets'}]},None)['ok'])

if __name__=='__main__':unittest.main()
