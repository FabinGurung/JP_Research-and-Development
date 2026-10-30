#!/usr/bin/env python3
"""No-network regression for reservation PR writes, collision and merge barrier."""
import base64
import copy
import json
import os
import unittest
from unittest.mock import patch
import researcher_sequence as engine

class FakeGitHub:
    def __init__(self):
        self.repo='owner/repo'; self.calls=[]; self.branches={}; self.prs=[]
        self.data=engine.load(engine.LEDGER)
    def main_sha(self):return 'mainsha'
    def file(self,path,ref):
        if path == engine.LEDGER:
            text=json.dumps(self.branches.get(ref,self.data))
        elif path == engine.STYLE:text='shared style'
        elif path == engine.TOWER:text=json.dumps({'version':'2.4.0'})
        else:text=json.dumps(engine.load(path))
        return {'sha':'blobsha'},text
    def api(self,method,path,body=None):
        self.calls.append((method,path,body))
        if method=='GET' and path.startswith('/git/trees/'):return {'tree':[]},200
        if method=='GET' and path.startswith('/git/ref/heads/'):
            return ({'object':{'sha':'mainsha'}},200) if path.removeprefix('/git/ref/heads/') in self.branches else ({},404)
        if method=='POST' and path=='/git/refs':
            self.branches[body['ref'].removeprefix('refs/heads/')]=copy.deepcopy(self.data)
            return {'object':{'sha':body['sha']}},201
        if method=='PUT' and path.startswith('/contents/'):
            assert body['branch']!='main', 'Direct main write forbidden'
            if path=='/contents/'+engine.LEDGER:
                self.branches[body['branch']]=json.loads(base64.b64decode(body['content']))
            return {},201
        if method=='GET' and path.startswith('/contents/'):return {},404
        if method=='GET' and path.startswith('/pulls?'):return self.prs,200
        if method=='POST' and path=='/pulls':
            pr={'html_url':'https://example.test/pr'};self.prs.append(pr);return pr,201
        raise AssertionError((method,path))

class Tests(unittest.TestCase):
    def setUp(self):
        self.gh=FakeGitHub()
        self.env=patch.dict(os.environ,{'GITHUB_ACTIONS':'true','GITHUB_REF':'refs/heads/main','GITHUB_RUN_ID':'123'})
        self.env.start();self.addCleanup(self.env.stop)
        p=patch.object(engine,'Github',return_value=self.gh);p.start();self.addCleanup(p.stop)
    def test_proposal_retry_and_finalize_barrier(self):
        engine.reserve('saugat-paneru','test',False)
        proposal=self.gh.branches['reservation/latex/gha-123']
        self.assertEqual(engine.plan(self.gh.data,'saugat-paneru','test')['sequence'],29)
        engine.reserve('saugat-paneru','test',False)
        self.assertEqual(len(self.gh.prs),1)
        with self.assertRaisesRegex(RuntimeError,'No accepted'):
            engine.finalize('saugat-paneru','gha:123',False)
        self.gh.data=proposal # simulated accepted merge, no provider write
        engine.finalize('saugat-paneru','gha:123',False)
        self.assertIn('thesis/saugat-paneru/latex/seq029-test',self.gh.branches)
        writes=[c for c in self.gh.calls if c[0] in ('PUT','POST','PATCH')]
        self.assertFalse(any(c[2].get('branch')=='main' for c in writes))
    def test_collision_and_history_mutation(self):
        engine.reserve('nabin-bista','test',False)
        proposal=self.gh.branches['reservation/latex/gha-123']
        engine.reservation_delta(self.gh.data,proposal,'reservation/latex/gha-123')
        accepted=copy.deepcopy(proposal)
        with self.assertRaises(ValueError):engine.reservation_delta(accepted,proposal,'reservation/latex/gha-123')
        altered=copy.deepcopy(proposal);altered['researchers'][0]['baseline']['last_historical_sequence']=99
        with self.assertRaises(ValueError):engine.reservation_delta(self.gh.data,altered,'reservation/latex/gha-123')
    def test_every_unknown_baseline_blocks_without_writes(self):
        for row in self.gh.data['researchers']:
            if row['baseline']['last_historical_sequence'] is None:
                with self.assertRaisesRegex(ValueError,'HOLD_BASELINE'):engine.reserve(row['slug'],'test',False)
        self.assertFalse(any(c[0]!='GET' for c in self.gh.calls))
    def test_wrong_owner_key_cannot_finalize(self):
        engine.reserve('saugat-paneru','test',False)
        self.gh.data=self.gh.branches['reservation/latex/gha-123']
        with self.assertRaisesRegex(RuntimeError,'No accepted'):engine.finalize('nabin-bista','gha:123',False)

if __name__=='__main__':unittest.main()
