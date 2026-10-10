"""Decimal business arithmetic checks; source and legal approvals remain external."""
from decimal import Decimal, InvalidOperation
PRICED={"client-contract","estimate","vendor-quotation","government-quotation","purchase-order"}
def number(value):
    try: n=Decimal(str(value))
    except (InvalidOperation,TypeError): raise ValueError("Invalid numeric value") from None
    if not n.is_finite(): raise ValueError("Nonfinite number")
    return n
def validate(document):
    kind=document.get("template_id")
    if kind in PRICED:
        data=document.get("financials")
        if data is None: return "HOLD_NO_STRUCTURED_FINANCIALS"
        rows=data.get("items",[])
        if not rows: raise ValueError("Missing line items")
        total=Decimal(0)
        for item in rows:
            if not item.get("source_ref") or not item.get("unit"): raise ValueError("Untraced line item")
            q,r,a=(number(item.get(k)) for k in ("quantity","rate","amount"))
            if min(q,r,a)<0 or (q*r).quantize(Decimal("0.01"))!=a.quantize(Decimal("0.01")):
                raise ValueError("Line amount mismatch")
            total+=a
        tax=number(data.get("tax"))
        if total.quantize(Decimal("0.01"))!=number(data.get("subtotal")).quantize(Decimal("0.01")):
            raise ValueError("Subtotal mismatch")
        if (total+tax).quantize(Decimal("0.01"))!=number(data.get("grand_total")).quantize(Decimal("0.01")):
            raise ValueError("Grand total mismatch")
        return "ARITHMETIC_PASS_SOURCE_UNVERIFIED"
    if kind=="material-report":
        rows=document.get("stock_movements")
        if rows is None: return "HOLD_NO_STOCK_LEDGER"
        if not rows: raise ValueError("Empty stock ledger")
        for row in rows:
            if not row.get("source_ref") or not row.get("unit"): raise ValueError("Stock source missing")
            a,b,c,d=(number(row.get(k)) for k in ("opening","receipts","issued","closing"))
            if min(a,b,c,d)<0 or a+b-c!=d: raise ValueError("Stock mismatch")
        return "INVENTORY_ARITHMETIC_PASS_SOURCE_UNVERIFIED"
    if kind in ("salary-contract","payment-slip"):
        pay=document.get("payroll")
        if pay is None:return "HOLD_NO_PAYROLL_RECONCILIATION"
        gross,dec,net=(number(pay.get(k)) for k in ("gross","deductions","net"))
        if min(gross,dec,net)<0 or gross-dec!=net: raise ValueError("Payroll mismatch")
        return "PAYROLL_ARITHMETIC_PASS_SOURCE_UNVERIFIED"
    return "NOT_APPLICABLE"
