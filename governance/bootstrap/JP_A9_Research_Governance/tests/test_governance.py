import json
from pathlib import Path
import shutil
import sys
import tempfile
import unittest

SOURCE=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(SOURCE/'scripts'))
import a9
from validate import validate

class GovernanceTests(unittest.TestCase):
    def setUp(self):
        self.temp=tempfile.TemporaryDirectory()
        self.root=Path(self.temp.name)
        shutil.copytree(SOURCE/'schemas',self.root/'schemas')
        (self.root/'projects').mkdir()
        (self.root/'receipts').mkdir()
        a9.save(self.root/'CURRENT.json',{'status':'ACTIVE','repository':{'provider_id':'999999','visibility':'PUBLIC'},'projects':[]})
        a9.init(self.root,'example-research-project','PROJ-999999','discussion')
        self.evidence={'pre_commit':'a'*40,'pre_snapshots':['synthetic-pre-snapshot']}
        self.receipt={'receipt_id':'TEST-RECEIPT','event_id':'synthetic-event','provider':'GITHUB','observed_at':'2026-10-06T10:00:00Z',
                      'object_id':'synthetic-object','revision':'a'*40,'result':'PASS','sha256':None}
        a9.save(self.root/'receipts/test.json',self.receipt)
        self.passed={'status':'PASS','receipt':'receipts/test.json'}

    def tearDown(self):
        self.temp.cleanup()

    def append(self,op,evidence=None):
        return a9.append(self.root,'example-research-project','discussion',op,evidence or {})

    def pre(self):
        self.append('PRE',self.evidence)

    def ready(self):
        self.pre()
        self.append('POST',{'qa':self.passed,'post_snapshots':['synthetic-post-snapshot']})
        self.append('PROVIDER_READBACK',{'readback':self.passed})
        self.append('ACK',{'ack':self.passed})
        self.append('REGISTER',{'registration':self.passed})

    def test_verified_close_and_resume(self):
        self.ready()
        event=self.append('CLOSE',{'next_boundary':'Next separately approved lane.'})
        self.assertEqual(event['status'],'CLOSED')
        self.assertEqual(validate(self.root),[])
        resume=a9.resume(self.root,'example-research-project','discussion')
        self.assertEqual(resume['latest_closed_event'],event['event_id'])
        self.assertLess(len(json.dumps(resume)),3000)

    def test_missing_pre_blocks_mutation(self):
        with self.assertRaises(ValueError): self.append('MUTATE')

    def test_unfinished_pre_cannot_be_replayed(self):
        self.pre()
        with self.assertRaises(ValueError): self.pre()

    def test_close_requires_post_readback_ack_registration(self):
        self.pre()
        with self.assertRaises(ValueError): self.append('CLOSE')

    def test_open_debt_blocks_close(self):
        self.ready()
        with self.assertRaises(ValueError): self.append('CLOSE',{'open_debt':['unverified artifact']})

    def test_missing_receipt_blocks_pass_claim(self):
        self.pre()
        with self.assertRaises(ValueError): self.append('POST',{'qa':{'status':'PASS','receipt':'missing.json'}})

    def test_failed_receipt_blocks_pass_claim(self):
        self.pre()
        a9.save(self.root/'receipts/test.json',{**self.receipt,'result':'FAIL'})
        with self.assertRaises(ValueError): self.append('POST',{'qa':self.passed})

    def test_path_traversal_rejected(self):
        with self.assertRaises(ValueError): a9.init(self.root,'../../outside','PROJ-999998','discussion')
        self.pre()
        with self.assertRaises(ValueError): self.append('POST',{'qa':{'status':'PASS','receipt':'../outside'}})

    def test_current_mismatch_blocks_recovery_replay(self):
        self.pre()
        path=a9.lane_root(self.root,'example-research-project','discussion')/'CURRENT.json'
        current=a9.load(path); current['latest_event']=None; a9.save(path,current)
        with self.assertRaises(ValueError): self.append('MUTATE')
        self.assertTrue(validate(self.root))

    def test_identity_mismatch_rejected(self):
        with self.assertRaises(ValueError): a9.init(self.root,'example-research-project','PROJ-999998','latex')

    def test_correction_requires_real_same_lane_target(self):
        self.pre()
        with self.assertRaises(ValueError): self.append('SUPERSEDE',{'supersedes':'another/lane/target'})

    def test_second_sequence_and_explicit_rollback_debt(self):
        self.ready(); closed=self.append('CLOSE')
        self.pre()
        event=self.append('ROLLBACK_POINTER',{'supersedes':closed['event_id']})
        self.assertEqual(event['status'],'BLOCKED')
        self.assertTrue(event['open_debt'])
        self.assertEqual(validate(self.root),[])

    def test_private_pointer_not_publishable(self):
        self.pre()
        self.append('HASH',{'artifacts':[{'artifact_id':'TEST-ARTIFACT','artifact_type':'thesis_pdf','source_authority':'GOOGLE_DRIVE',
          'drive_id':'synthetic-id','sha256':None,'bytes':None,'visibility':'RESTRICTED','release':None,'reverse_reference_receipt':None}]})
        self.assertTrue(validate(self.root,public=True))
        self.assertEqual(validate(self.root,public=False),[])

    def test_proprietary_fonts_rejected(self):
        (self.root/'private-font.ttf').write_bytes(b'font')
        self.assertTrue(validate(self.root))

    def test_post_without_snapshot_cannot_close(self):
        self.pre()
        self.append('POST',{'qa':self.passed})
        self.append('PROVIDER_READBACK',{'readback':self.passed})
        self.append('ACK',{'ack':self.passed})
        self.append('REGISTER',{'registration':self.passed})
        with self.assertRaises(ValueError): self.append('CLOSE')

    def test_milestone_requires_verified_evidence(self):
        self.pre()
        with self.assertRaises(ValueError): self.append('RELEASE',{'release':'test-v1'})

    def test_debt_register_tracks_resolution(self):
        self.pre()
        self.append('DEBT_REGISTER',{'open_debt':['Verify source hash']})
        self.assertEqual(validate(self.root),[])
        self.append('DEBT_REGISTER',{'open_debt':[]})
        debt=a9.load(self.root/'projects/example-research-project/debt.json')
        self.assertEqual(debt['items'][0]['status'],'RESOLVED')

    def test_committed_history_cannot_be_rewritten(self):
        import subprocess
        from validate import immutable_history
        self.pre()
        for command in [['git','init','-q'],['git','add','.'],['git','-c','user.name=Test','-c','user.email=test@example.invalid','commit','-qm','PRE']]:
            subprocess.run(command,cwd=self.root,check=True)
        base=subprocess.check_output(['git','rev-parse','HEAD'],cwd=self.root,text=True).strip()
        self.assertEqual(immutable_history(self.root,base),[])
        event_path=self.root/'projects/example-research-project/lanes/discussion/events/000001.json'
        event=a9.load(event_path); event['actor']='rewritten'; a9.save(event_path,event)
        self.assertTrue(immutable_history(self.root,base))

    def test_unprovisioned_repository_blocks_live_admission(self):
        a9.save(self.root/'CURRENT.json',{'status':'BOOTSTRAP_NOT_PROVISIONED','repository':{'provider_id':None,'visibility':'UNVERIFIED'},'projects':[]})
        with self.assertRaises(ValueError): a9.init(self.root,'another-research-project','PROJ-999998','discussion')

if __name__=='__main__': unittest.main()
