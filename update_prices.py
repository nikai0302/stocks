import yfinance as yf
import json
from datetime import datetime, timezone

STOCKS = {
    'JFC':  'JFC.PS',
    'BDO':  'BDO.PS',
    'SMPH': 'SMPH.PS',
    'MBT':  'MBT.PS',
    'URC':  'URC.PS',
    'AC':   'AC.PS',
    'ALI':  'ALI.PS',
    'SM':   'SM.PS',
}

results = {}
errors = []

for name, sym in STOCKS.items():
    try:
        t = yf.Ticker(sym)
        fi = t.fast_info
        price = round(float(fi.last_price), 2)
        prev  = round(float(fi.previous_close or fi.open or price), 2)
        chg   = round(price - prev, 2)
        pct   = round(((price - prev) / prev) * 100, 4) if prev else 0
        results[name] = {
            'price': price,
            'prev':  prev,
            'chg':   chg,
            'pct':   pct,
        }
        print(f"  {name}: {price} ({pct:+.2f}%)")
    except Exception as e:
        errors.append(f"{name}: {e}")
        print(f"  WARN {name}: {e}")

output = {
    'prices':  results,
    'updated': datetime.now(timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ'),
    'errors':  errors,
    'count':   len(results),
}

with open('prices.json', 'w') as f:
    json.dump(output, f, indent=2)

print(f"\nDone: {len(results)}/{len(STOCKS)} stocks written to prices.json")
