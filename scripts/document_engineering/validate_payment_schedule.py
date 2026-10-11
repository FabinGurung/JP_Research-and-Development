#!/usr/bin/env python3
"""Validate a private project milestone schedule against A9 shared payment controls.

This script performs arithmetic/structural checks only; it never approves legal terms.
"""
import argparse
import json
from decimal import Decimal, InvalidOperation, ROUND_HALF_UP
from pathlib import Path

REQUIRED_TRIGGERS = {"COMMENCEMENT", "COMPLETION", "RETENTION_RELEASE"}
def dec(x, name):
    try: value=Decimal(str(x))
    except (InvalidOperation, TypeError): raise ValueError("Invalid number: "+name) from None
    if not value.is_finite() or value<0:raise ValueError("Negative/nonfinite: "+name)
    return value
def validate(data):
    currency=data.get("currency")
    if not isinstance(currency,str) or len(currency)!=3 or not currency.isalpha():
        raise ValueError("ISO currency code required")
    total=dec(data.get("total_contract_value"),"total")
    rows=data.get("milestones")
    if not isinstance(rows,list) or not rows:raise ValueError("milestones required")
    sum_percent=Decimal(0); sum_value=Decimal(0)
    for i,row in enumerate(rows,1):
        if row.get("number")!=i:raise ValueError("Missing or duplicated milestone numbering")
        if row.get("trigger") not in REQUIRED_TRIGGERS:raise ValueError("Unknown trigger")
        if not str(row.get("event","")).strip():raise ValueError("Missing milestone description")
        p=dec(row.get("percent"),"percent"); money=dec(row.get("amount"),"amount")
        expected=(total*p/100).quantize(Decimal("0.01"),rounding=ROUND_HALF_UP)
        if money.quantize(Decimal("0.01"))!=expected:
            raise ValueError(f"Milestone {i}: amount {money} != {expected}")
        sum_percent+=p;sum_value+=money
    if sum_percent!=Decimal(100) or sum_value.quantize(Decimal("0.01"))!=total.quantize(Decimal("0.01")):
        raise ValueError("Schedule does not sum to 100% and exact contract value")
    retention=data.get("retention")
    if retention:
        r=dec(retention.get("rate_percent"),"retention_rate")
        amount=dec(retention.get("amount_npr" if currency=="NPR" else "amount"),"retention_amount")
        if (total*r/100).quantize(Decimal("0.01"))!=amount.quantize(Decimal("0.01")):
            raise ValueError("Retention percentage/amount mismatch")
        if retention.get("model")=="FINAL_RETAINED_INSTALMENT":
            last=rows[-1]
            if last.get("trigger")!="RETENTION_RELEASE" or dec(last.get("amount"),"last amount")!=amount:
                raise ValueError("Final retained instalment must match final payment row")
        if retention.get("independent_of_defects_expiry") is not True:
            raise ValueError("Retention and defects-liability periods must be independent")
    dlp=data.get("defects_liability")
    if dlp:
        if int(dlp.get("period_months",0))<1:raise ValueError("Invalid defects period")
        if dlp.get("not_part_of_payment_trigger_cell") is not True:
            raise ValueError("Defects period should be a separate agreement note")
    return {"arithmetic":"PASS","row_count":len(rows),
            "percent_total":str(sum_percent),"value_total":str(sum_value),
            "currency":currency,"signable":False,
            "human_review":"STILL_REQUIRED"}
def selftest():
    sample={"currency":"NPR","total_contract_value":"1000",
            "milestones":[{"number":1,"event":"Demo only","trigger":"COMPLETION","percent":"100","amount":"1000"}]}
    assert validate(sample)["arithmetic"]=="PASS"
    sample["milestones"][0]["amount"]="999"
    try:validate(sample)
    except ValueError:pass
    else:raise AssertionError("Mismatched amount was not rejected")
    print("PASS milestone Decimal maths and mismatch rejection")
if __name__=="__main__":
    ap=argparse.ArgumentParser()
    ap.add_argument("--data",type=Path);ap.add_argument("--self-test",action="store_true")
    args=ap.parse_args()
    if args.self_test:selftest()
    elif args.data:print(json.dumps(validate(json.loads(args.data.read_text())),indent=2))
    else:ap.error("Provide --self-test or --data")
