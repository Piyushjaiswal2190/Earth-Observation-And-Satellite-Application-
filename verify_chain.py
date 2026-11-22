import json, hashlib

prev = "0" * 64
ok = True
checked = 0
with open("logs/astra_ai.jsonl") as f:
    for i, line in enumerate(f, 1):
        line = line.strip()
        if not line:
            continue
        try:
            rec = json.loads(line)
        except json.JSONDecodeError as e:
            print(f"BAD JSON at line {i}: {e}")
            ok = False
            continue
        head = rec.pop("head", None)
        if head is None:
            print(f"MISSING head at line {i} (seq={rec.get('seq')})")
            ok = False
            continue
        body = json.dumps(rec, sort_keys=True, separators=(",", ":"))
        calc = hashlib.sha256(body.encode()).hexdigest()
        if rec["prev"] != prev or calc != head:
            print(f"BROKEN at record {i} (boot={rec.get('boot')}, seq={rec.get('seq')})")
            ok = False
        prev = head
        checked += 1
print(f"Checked {checked} records.")
print("CHAIN OK" if ok else "CHAIN BROKEN")
