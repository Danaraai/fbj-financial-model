# Prompt: Write a PRD for the FBJ × Amphora 3PL Financial Model Dashboard

---

## Your Role

You are a senior product manager and financial analyst at Goldman Sachs building an internal decision-support tool for a 3PL business partnership. Write a complete, buildable Product Requirements Document (PRD) for an interactive financial dashboard. The PRD must be specific enough that an engineer (or Claude Code) can build the full application without needing any clarifying questions.

This PRD supersedes the existing dashboard at imaginative-puffpuff-ab06ab.netlify.app. Do not replicate that tool's structure — rebuild it correctly per the spec below.

---

## Business Context

**Jack Archer (JA / FBJ)** is an apparel brand with its own warehouse in Canada (FC1). They have excess warehouse capacity and are launching **Fulfilled by Jack (FBJ)** — a 3PL fulfillment service for other brands.

**Amphora** is a European 3PL company. They have agreed to refer their brand clients to FBJ for North American fulfillment. The partnership has two WMS systems coexisting in one warehouse: FBJ's own (Shopify WMS) and Amphora's WMS.

**The core financial question this tool must answer:**
> "Under different rate, volume, and margin-share scenarios, what is FBJ's 24-month net P&L from this partnership — and what are the key assumptions driving it?"

**Primary audience:** David and internal FBJ leadership. This is an internal decision-support tool, not a client-facing deck.

---

## What's Wrong with the Current Tool — 8 Problems to Fix

The existing dashboard at imaginative-puffpuff-ab06ab.netlify.app has good visual design but eight critical problems. All must be fixed in this rebuild.

1. **Opens on Inputs — no context.** User sees 12 sliders with no anchor or base case. Fix: open on Base Case summary screen.

2. **No locked base case.** Every output feels provisional because there is no defined ground truth. Fix: lock and label a base case on Screen 1 that does not change unless the user goes to Inputs (Screen 4).

3. **Scenarios are slider combos, not business stories.** The current Scenarios tab has 8 cards with cryptic one-line descriptions. Fix: three named scenarios (Base Case, Downside, Upside) each with a proper business narrative — what Amphora delivers, what rates apply, what the risk is.

4. **Revenue model is incomplete.** Current Monthly P&L shows only: Fulfill Rev, Ship Rev, Mgmt Rev. Completely missing: Storage revenue (~$9K–$28K/mo at scale), Inbound revenue (~$2.8K–$43K/mo at scale), Returns revenue (~$5K–$52K/mo at scale). These three streams represent ~40% of total revenue. They must be added to the Monthly P&L table and to all KPI calculations.

5. **Shipping margin is $2.00 — should be $1.25.** David's own notes confirm $1.25 is the correct figure (JA's markup over actual carrier cost). $2.00 overstates shipping margin revenue by ~$135K over 24 months. Fix: use $1.25 everywhere — in all defaults, all scenarios, all scenario card outputs.

6. **Brand count is hardcoded, not a slider.** The current tool uses "New Amphora brands per month = 2" but never lets the user set the *starting* brand count. Fix: add a "Starting Amphora brands" slider (default 3, conservative; Excel starts with 6 named brands in Phase 1).

7. **No cost model transparency.** The pick/pack margin (~$0.52/order thin margin) and full cost build-up are never shown or explained. The "Labor" column in the P&L is just $0.25 variable overhead — it does not reflect the $2.48 fully-loaded cost. Fix: add a cost model toggle (Marginal vs Fully-Loaded) and show the margin structure explicitly in an Assumptions panel.

8. **FBJ legacy brands not separately modeled.** Jack Archer's own pre-existing brands (FBJ legacy) keep 100% of shipping margin — no Amphora split. This is shown in the Revenue Share table but never reflected in the P&L math. Fix: model legacy FBJ volume as a separate order pool at 100% shipping margin share.

---

## The Margin Structure — Core Logic of the Model

This is the conceptual foundation. Display this as a labeled assumptions panel on Screen 1 and Screen 4.

### How FBJ makes money per order

**Pick/Pack (fulfillment margin):**
```
FBJ charges client:  $2.90/order + ($0.85 × 2.2 units) + $0.95 packaging = $5.72/order
FBJ's cost:          $2.75/order + ($0.95 × 2.2 units) + $0.363 packaging = $5.20/order
──────────────────────────────────────────────────────────────────────────────────────
Fulfillment margin:  ~$0.52/order  ← thin but real, already net of cost
```
Note: Pick/pack revenue is already net of FBJ's own labor and packaging cost. No further cost deduction needed for this stream.

**Shipping margin (the negotiated split):**
```
JA's shipping markup per order:  $1.25  ← markup over actual carrier cost
This $1.25 is split based on who brought the brand and whose rates are used:

  Amphora brand + Amphora rate  →  FBJ keeps 30%  =  $0.375/order
  Amphora brand + FBJ rate      →  FBJ keeps 50%  =  $0.625/order
  FBJ brand + FBJ rate          →  FBJ keeps 70%  =  $0.875/order
  FBJ legacy brand (JA own)     →  FBJ keeps 100% =  $1.250/order
```
Note: For Jack Archer's own pre-existing brands (legacy FBJ volume), shipping margin is 100% — no Amphora share.

**Storage (near-pure margin):**
```
Revenue: $28/pallet/month  ← charged to client
Cost:    ~$0  ← spare warehouse space, no incremental cost
Margin:  ~$28/pallet/month
```

**Inbound receipts:**
```
Revenue: $2.75/case received
Cost:    $1.73/case  ($25.98/hr labor ÷ 15 cases/hr)
Margin:  ~$1.02/case
```

**Returns:**
```
Revenue: $4.75/return order + $1.25/item × 1.7 avg units = ~$6.88/return
Cost:    $1.30/return  ($25.98/hr ÷ 20 returns/hr)
Margin:  ~$5.58/return
```

**Account management & onboarding (pure margin):**
```
$350/brand/month  ← no incremental cost
$2,000/brand onboarding (one-time)  ← no incremental cost
```

---

## Volume Model — How Brands and Orders Are Forecast

### Brand structure

The model has **two brand pools** with different margin profiles:

**Pool 1 — Amphora-introduced brands:**
- Brands Amphora refers to FBJ
- FBJ splits shipping margin with Amphora (30–70% depending on whose rates)
- Modeled via sliders: starting brand count + new brands added per month

**Pool 2 — FBJ legacy / JA own brands:**
- Jack Archer's pre-existing brands fulfilling through the warehouse
- FBJ keeps 100% of shipping margin
- Modeled as a fixed baseline with growth rate

### Key volume assumption — display explicitly in UI

> **"Each Amphora brand is assumed to contribute 5,000 orders/month at steady state."**
> Note: David's Excel brand-level data suggests ~2,300/brand based on actual named brands. 5,000 is the planning assumption. Adjust the slider to stress-test.

### Brand ramp

```
Starting Amphora brands (Month 1):   [slider, default 3]
New Amphora brands added per month:  [slider, default 2]
Amphora brands at month m:           starting_brands + new_per_month × (m - 1)

FBJ legacy orders/month (Month 1):   [input, default 5,000]
FBJ legacy order growth per month:   [slider, default 5%]
FBJ legacy orders at month m:        5,000 × (1.05)^(m-1)
```

From the Excel, the actual Phase 1 starts with 6 named brands. The default of 3 is intentionally conservative.

---

## Complete Revenue Model

All seven revenue streams must be modeled. This is the full picture — not just fulfillment and shipping.

### 1. Fulfillment Revenue (Pick/Pack)

```
fulfillment_rev(m) = total_orders(m) × [tiered_order_rate + (avg_units × tiered_unit_rate) + packaging_fee]

Tiered rates (FBJ proposed):
  < 5K orders/mo:   $3.00/order + $0.95/unit + $0.95 packaging
  5K–25K/mo:        $2.90/order + $0.85/unit + $0.95 packaging
  25K–75K/mo:       $2.75/order + $0.75/unit + $0.95 packaging
```

### 2. Shipping Margin Revenue

```
Amphora orders(m) = amphora_brands(m) × 5,000 orders/brand

Before month_direct_rates_secured:
  ship_rev(m) = amphora_orders(m) × $1.25 × 30%    [Amphora brand / Amphora rate]
              + fbj_legacy_orders(m) × $1.25 × 100% [FBJ legacy, full margin]

From month_direct_rates_secured onward:
  ship_rev(m) = amphora_orders(m) × $1.25 × 50%    [Amphora brand / FBJ rate]
              + fbj_legacy_orders(m) × $1.25 × 100% [FBJ legacy, full margin]
```

The shipping margin slider controls the Amphora share %. Scenario markers show where to set it.

### 3. Storage Revenue

```
Per-brand storage assumptions (averages from Excel brand data):
  Avg pallets per Amphora brand:     15 pallets
  Avg SKUs (pick facings) per brand: 143 SKUs

storage_rev(m) = amphora_brands(m) × 15 × $28/pallet
               + amphora_brands(m) × 143 × $12/SKU
```

Display note in UI: *"Storage is near-pure margin — FBJ's warehouse has spare capacity."*

### 4. Inbound Revenue

```
Per-brand inbound assumptions (averages from Excel):
  Avg cases inbound per brand per month: 340 cases
  Avg units per case: 12 (apparel average)

inbound_rev(m)  = amphora_brands(m) × 340 × $2.75/case
inbound_cost(m) = amphora_brands(m) × 340 × $1.73/case  [$25.98/hr ÷ 15 cases/hr]
```

### 5. Returns Revenue

```
return_rate = 15% of orders
avg_units_per_return = 1.7

returns_rev(m)  = total_orders(m) × 15% × [$4.75/order + (1.7 × $1.25/item)]
returns_cost(m) = total_orders(m) × 15% × $1.30/return  [$25.98/hr ÷ 20 returns/hr]
```

### 6. Account Management Revenue

```
mgmt_rev(m) = amphora_brands(m) × $350/brand/month
```
Pure margin. No cost offset.

### 7. Brand Onboarding Revenue

```
onboarding_rev(m) = new_brands_added(m) × $2,000  [one-time, month brand is onboarded]
new_brands_added(1) = starting_brands
new_brands_added(m) = new_per_month  for m > 1
```
Pure margin. No cost offset.

### Total Revenue

```
total_rev(m) = fulfillment_rev + shipping_rev + storage_rev + inbound_rev
             + returns_rev + mgmt_rev + onboarding_rev
```

---

## Complete Cost Model

Two modes toggled in Inputs (Screen 4). Toggle updates all cost calculations live.

### Mode A — Marginal Cost (default)
*Assumption: Amphora rides existing JA warehouse capacity. No new headcount until volume threshold.*

```
pick_pack_cost    = already netted in fulfillment margin above — DO NOT double-count
inbound_cost(m)   = amphora_brands(m) × 340 × $1.73/case
returns_cost(m)   = total_orders(m) × 15% × $1.30/return
wms_cost(m)       = total_orders(m) × $0.20  [waived if total_orders > 50,000/mo]
integration(m)    = $25,000 if m == integration_month, else $0
overhead(m)       = total_orders(m) × $0.25  [variable labor/overhead]

total_cost(m) = overhead + inbound_cost + returns_cost + wms_cost + integration
```

### Mode B — Fully-Loaded Cost
*Assumption: Amphora requires new warehouse resources. Full labor allocated per order.*

```
pick_pack_cost(m) = total_orders(m) × ($2.48 labor + $0.363 packaging)
inbound_cost(m)   = amphora_brands(m) × 340 × $1.73/case
returns_cost(m)   = total_orders(m) × 15% × $1.30/return
wms_cost(m)       = total_orders(m) × $0.20  [waived if total_orders > 50,000/mo]
integration(m)    = $25,000 if m == integration_month, else $0
other_cost(m)     = total_rev(m) × 5%

total_cost(m) = pick_pack_cost + inbound_cost + returns_cost + wms_cost + integration + other_cost
```

**Critical:** In Mode A, pick/pack revenue minus pick/pack cost flows through as ~$0.52/order fulfillment margin. In Mode B, the full labor+packaging cost is added back explicitly. Do not double-count in either mode.

---

## UX / Design Requirements

### Navigation (4 tabs)

```
[ Base Case ] [ Scenarios ] [ Monthly P&L ] [ Inputs (advanced) ]
```

Opens on **Base Case**. No sliders visible until Screen 4.

---

### Screen 1 — Base Case (Landing Page)

The anchor. Communicates the plan without any interactive elements.

**1. Assumptions panel** (visible on load, collapsible):

> **How FBJ makes money — base case assumptions**
>
> | Stream | Revenue | Cost | Margin |
> |--------|---------|------|--------|
> | Pick/pack | ~$5.72/order | ~$5.20/order | ~$0.52/order |
> | Shipping margin | $1.25/order × 30% share | $0 | $0.375/order (Amphora brands) |
> | Storage | $28/pallet/mo | ~$0 | ~$28/pallet/mo |
> | Inbound | $2.75/case | $1.73/case | ~$1.02/case |
> | Returns | ~$6.88/return | $1.30/return | ~$5.58/return |
> | Mgmt fees | $350/brand/mo | $0 | $350/brand/mo |
>
> **Volume:** 5,000 orders/month per Amphora brand. Starting brands: 3. Adding 2/month.
> *David's Excel named-brand data implies ~2,300/brand actual — 5,000 is the planning assumption.*

**2. Narrative banner** (locked, not editable):
> "Base case: FBJ onboards 3 Amphora brands at go-live, adds 2/month at 5,000 orders/brand. FBJ secures direct carrier rates by Month 12. Marginal cost model (existing warehouse capacity)."

**3. KPI cards (top row, recalculated from corrected model):**
- 24-Month Cumulative Net
- Break-Even Month
- Peak Orders/Month (Month 24)
- Peak Brands Active (Month 24)

**4. Revenue mix bar** — horizontal stacked bar, 24-month totals by stream:
`Fulfillment | Shipping | Storage | Inbound | Returns | Mgmt & Onboarding`

**5. Key Risk callout** (amber highlight box):
> "⚠ Key risk: Shipping margin share is the most sensitive variable. Securing direct carrier rates (moving from 30% → 50% share) is the single biggest lever. See Scenarios tab for range of outcomes."

**No sliders on this screen.**

---

### Screen 2 — Scenarios

Three pre-loaded scenario cards, side by side. No sliders. Each card has a named business narrative.

**IMPORTANT:** All scenario outputs must be calculated using $1.25 shipping margin (not $2.00). The existing tool uses $2.00 which is incorrect.

**Base Case** (green border, default selected):
- *FBJ onboards 3 Amphora brands at launch, adds 2/month at 5K orders/brand. FBJ secures direct carrier rates Month 12 (50% share from then). Marginal cost model. $1.25 shipping margin.*
- Key outputs: 24-mo net, break-even month, peak orders/mo, peak brands active

**Downside:**
- *Amphora ramp is 50% slower — 1 new brand/month. FBJ never secures direct carrier rates (30% Amphora/Amphora share throughout all 24 months). Amphora counter rates accepted on fulfillment. $1.25 shipping margin.*
- Uses Amphora counter rates: $0.55/order + $0.45/unit fulfillment; $10/pallet storage; $1.80/case inbound; $0 returns (Amphora excluded these from their counter)
- Key outputs: same format, shown in red if cumulative net is negative

**Upside:**
- *Strong Amphora ramp — 3 new brands/month. FBJ secures direct carrier rates by Month 9 (50% share from Month 9). FBJ legacy volume grows 10%/month. $1.25 shipping margin.*
- Key outputs: same format, shown in green

Each card includes:
- One-sentence narrative (as above)
- 24-Mo Cumulative Net (large, colored)
- Break-even month
- Peak orders/month
- "View monthly detail →" button — loads this scenario in Monthly P&L tab

**Note to engineer:** Do not use any hardcoded scenario output numbers. Compute all three scenarios from the financial model logic using the input overrides defined above. This ensures the numbers are always consistent with the model.

---

### Screen 3 — Monthly P&L

Table, months 1–24. No sliders. Reflects last selected scenario (default: Base Case).

**Columns (in this order):**

| Month | Phase | Amphora Brands | Amphora Orders | FBJ Orders | Total Orders | Fulfill Rev | Ship Rev | Storage Rev | Inbound Rev | Returns Rev | Mgmt Rev | Total Rev | Total Cost | Monthly Net | Cumulative Net |

**Column details:**
- **Amphora Brands** — count of active brands that month (new column, was missing in David's tool)
- **Fulfill Rev** — pick/pack + per unit + packaging fees
- **Ship Rev** — FBJ's share of $1.25 shipping margin only (NOT the full shipping charge)
- **Storage Rev** — pallet storage + pick facing/SKU storage (was completely missing)
- **Inbound Rev** — receipt fees at $2.75/case (was completely missing)
- **Returns Rev** — return order fees + per item fees (was completely missing)
- **Mgmt Rev** — monthly mgmt fees + onboarding fees for new brands that month

**Formatting:**
- Phase badge: RAMP (amber, mo 1–3), GROWTH (teal, mo 4–6), SCALE (green, mo 7+)
- Monthly Net: green text if positive, red text if negative
- Cumulative Net: bold; highlight the row where it first crosses zero (break-even row) with a subtle amber background
- Numbers formatted as $XK for thousands, $X.XM for millions
- Zebra row striping, right-aligned numbers, monospace font for number columns

---

### Screen 4 — Inputs (Advanced / Internal)

**Warning banner (amber):**
> "⚠ Internal use only. Changing these inputs updates all scenarios. Currently showing: Base Case values."

**Two-column layout:**

#### Left Column — Volume & Cost

**Brand volume:**
- Starting Amphora brands (Month 1): slider, default **3**, range 1–10
  - Sub-label: *"Conservative default. David's Excel has 6 named Phase 1 brands. Set to 6 to match Excel."*
- New Amphora brands/month: slider, default **2**, range 0–5
  - Sub-label: *"Brands added each month after Month 1."*
- Orders per Amphora brand/month: text input, default **5,000**
  - Sub-label: *"Planning assumption. David's Excel actual named-brand average = ~2,300/mo. Use 5,000 for planning; reduce to stress-test."*
- FBJ legacy orders (Month 1): text input, default **5,000**
  - Sub-label: *"Jack Archer's own pre-existing brand volume. These orders keep 100% of shipping margin — no Amphora split."*
- FBJ legacy order growth/month: slider, default **5%**, range 0–15%
- Avg units per order: slider, default **2.2**, range 1–5

**Cost model toggle:**
```
[ Marginal (existing capacity) ]   [ Fully-loaded (new resources) ]
```
Sub-label: *"Marginal = Amphora rides JA's existing capacity, $0.25 variable overhead. Fully-loaded = new resources required, $2.843 blended CPO."*

**Other cost inputs:**
- WMS per-label fee: slider, default **$0.20**, range $0–$0.50
  - Sub-label: *"Waived above WMS threshold"*
- WMS fee waiver threshold: text input, default **50,000** orders/mo
- Integration build cost (one-time): text input, default **$25,000**
- Month integration cost incurred: slider, default **Month 6**, range Month 1–12

#### Right Column — Pricing & Revenue Share

**Fulfillment pricing (editable table):**

| Tier | Per Order | Per Unit | Packaging |
|------|-----------|----------|-----------|
| < 5K orders/mo | $3.00 | $0.95 | $0.95 |
| 5K–25K/mo | $2.90 | $0.85 | $0.95 |
| 25K–75K/mo | $2.75 | $0.75 | $0.95 |

Label: *"FBJ proposed rates per V3 agreement. Edit only if negotiating otherwise."*

**Other fee inputs:**
- Pallet storage rate: text input, default **$28**/pallet/mo
- Inbound receipt rate: text input, default **$2.75**/case
- Returns per order: text input, default **$4.75**
- Returns per item: text input, default **$1.25**
- Account mgmt fee: text input, default **$350**/brand/mo
- Brand onboarding fee: text input, default **$2,000**/brand

**Shipping margin slider (with scenario markers — CRITICAL UX):**

```
Conservative    Base Case    Optimistic
     ↓              ↓             ↓
  ───|──────────────|─────────────|───
  $0.75          $1.25          $1.75
[slider handle freely movable across full range]

Label: "JA's markup over actual carrier cost per order.
        At $1.25 with 30% Amphora share → FBJ earns $0.375/order on Amphora-rate volume."
```

**Revenue share sliders (ONE slider per type, with scenario markers — CRITICAL UX):**

For each slider: thin vertical tick marks above the track show scenario reference points. Slider handle is freely movable. Markers are guides only.

**FBJ Share — Amphora Brand + Amphora Rate:**
```
Conservative   Base Case   Optimistic
    20%           30%          45%
Label: "Applies months 1 through [direct rates month].
        Amphora introduced the brand, using Amphora's WMS rates."
Default: 30%
```

**FBJ Share — Amphora Brand + FBJ Rate:**
```
Conservative   Base Case   Optimistic
    35%           50%          65%
Label: "Applies from [direct rates month] onward.
        Amphora brand, but FBJ has secured direct carrier rates."
Default: 50%
```

**FBJ Share — FBJ Brand + FBJ Rate:**
```
Conservative   Base Case   Optimistic
    60%           70%          80%
Label: "FBJ-sourced brands using FBJ direct rates."
Default: 70%
```

**Note below all share sliders:**
> "FBJ legacy / JA own brands always = 100% share. These are Jack Archer's pre-existing brands — no Amphora revenue split applies."

**Month FBJ direct carrier rates secured:**
```
Slider, default Month 12, range Month 1–24
Label: "Before this month: Amphora-brand orders use Amphora rate (30% share).
        From this month: FBJ direct rate applies (50% share)."
```

---

## Financial Model Logic (Complete Pseudocode)

All calculations are reactive. Any input change updates all four screens instantly.

```javascript
// ── VOLUME ──────────────────────────────────────────────────────────────────
amphora_brands(m)     = starting_brands + new_per_month * (m - 1)
new_brands_added(m)   = m === 1 ? starting_brands : new_per_month
amphora_orders(m)     = amphora_brands(m) * orders_per_brand          // default 5,000
fbj_orders(m)         = fbj_start * Math.pow(1 + fbj_growth, m - 1)
total_orders(m)       = amphora_orders(m) + fbj_orders(m)

// ── TIER LOOKUP ──────────────────────────────────────────────────────────────
function getTier(orders) {
  if (orders < 5000)  return { order: 3.00, unit: 0.95 }
  if (orders < 25000) return { order: 2.90, unit: 0.85 }
  return                     { order: 2.75, unit: 0.75 }
}
packaging_fee = 0.95  // per order, all tiers

// ── REVENUE ──────────────────────────────────────────────────────────────────
fulfillment_rev(m) = total_orders(m) * (tier.order + avg_units * tier.unit + packaging_fee)

// Shipping: split changes at direct_rates_month
if (m < direct_rates_month) {
  ship_rev(m) = amphora_orders(m) * ship_margin * amphora_amphora_share   // default 30%
              + fbj_orders(m)     * ship_margin * 1.00                    // legacy = 100%
} else {
  ship_rev(m) = amphora_orders(m) * ship_margin * amphora_fbj_share       // default 50%
              + fbj_orders(m)     * ship_margin * 1.00                    // legacy = 100%
}

storage_rev(m)     = amphora_brands(m) * 15 * 28          // $28/pallet × 15 pallets/brand
                   + amphora_brands(m) * 143 * 12          // $12/SKU × 143 SKUs/brand

cases_inbound(m)   = amphora_brands(m) * 340               // 340 cases/brand/mo
inbound_rev(m)     = cases_inbound(m) * inbound_rate        // default $2.75/case

return_orders(m)   = total_orders(m) * return_rate          // default 15%
returns_rev(m)     = return_orders(m) * (returns_order_fee + avg_units_per_return * returns_item_fee)
                   // = return_orders * ($4.75 + 1.7 * $1.25) = return_orders * $6.875

mgmt_rev(m)        = amphora_brands(m) * mgmt_fee           // $350/brand/mo
onboarding_rev(m)  = new_brands_added(m) * onboarding_fee   // $2,000 one-time

total_rev(m)       = fulfillment_rev + ship_rev + storage_rev
                   + inbound_rev + returns_rev + mgmt_rev + onboarding_rev

// ── COSTS ────────────────────────────────────────────────────────────────────
inbound_cost(m)    = cases_inbound(m) * 1.73               // $25.98/hr ÷ 15 cases/hr
returns_cost(m)    = return_orders(m) * 1.30               // $25.98/hr ÷ 20 returns/hr
wms_cost(m)        = total_orders(m) > wms_threshold ? 0 : total_orders(m) * wms_fee
integration(m)     = m === integration_month ? integration_cost : 0

if (cost_mode === 'MARGINAL') {
  overhead(m)      = total_orders(m) * 0.25
  total_cost(m)    = overhead + inbound_cost + returns_cost + wms_cost + integration
}

if (cost_mode === 'FULLY_LOADED') {
  pick_cost(m)     = total_orders(m) * (2.48 + 0.363)      // labor + packaging
  other_cost(m)    = total_rev(m) * 0.05
  total_cost(m)    = pick_cost + inbound_cost + returns_cost + wms_cost + integration + other_cost
}

// ── P&L ──────────────────────────────────────────────────────────────────────
monthly_net(m)     = total_rev(m) - total_cost(m)
cumulative_net(m)  = sum of monthly_net(1) through monthly_net(m)
break_even_month   = first m where cumulative_net(m) >= 0
```

---

## Base Case Default Values

| Parameter | Default | Note |
|-----------|---------|------|
| Starting Amphora brands | **3** | Conservative; Excel starts with 6 named brands |
| New brands/month | 2 | David's model |
| Orders per Amphora brand | **5,000/mo** | Planning assumption; Excel avg ~2,300 |
| FBJ legacy orders (Month 1) | 5,000 | David's model |
| FBJ legacy growth/month | 5% | David's model |
| Avg units per order | 2.2 | Excel unit economics |
| Shipping margin per order | **$1.25** | Corrected from David's incorrect $2.00 |
| FBJ share — Amphora/Amphora rate | 30% | David's model |
| FBJ share — Amphora/FBJ rate | 50% | David's model |
| FBJ share — FBJ/FBJ rate | 70% | David's model |
| FBJ share — JA legacy | **100%** | Pre-existing brands, no Amphora split |
| Month FBJ direct rates secured | Month 12 | David's model |
| Cost model | Marginal | David's current dashboard default |
| WMS per-label fee | $0.20 | David's model |
| WMS fee waiver threshold | 50,000 orders/mo | David's model |
| Integration cost | $25,000 at Month 6 | David's model |
| Variable overhead (marginal) | $0.25/order | David's model |
| Labor cost (fully-loaded) | $2.48/order | Excel unit economics |
| Packaging cost | $0.363/order | Excel unit economics |
| Return rate | 15% | Excel assumptions |
| Avg units per return | 1.7 | Excel assumptions |
| Pallets per Amphora brand | 15 | Excel brand-level average |
| SKUs per Amphora brand | 143 | Excel brand-level average |
| Cases inbound per brand/mo | 340 | Excel brand-level average |
| Pallet storage rate | $28/pallet/mo | Excel fee structure |
| Inbound receipt rate | $2.75/case | Excel fee structure |
| Returns per order fee | $4.75 | Excel fee structure |
| Returns per item fee | $1.25 | Excel fee structure |
| Account mgmt fee | $350/brand/mo | David's model |
| Brand onboarding fee | $2,000/brand | David's model |

---

## Known Open Items — Flag as Code Comments, Do Not Block Build

```javascript
// TODO [DR to confirm]: Shipping margin corrected to $1.25/order (was $2.00 in original dashboard).
//   At 25K orders/mo that's a ~$5,625/mo difference — $135K over 24 months. Confirm before external use.

// TODO: B2B order volume not modeled separately.
//   Tiny Cottons has 500 B2B orders/mo with pallet/case fee structure ($18/pallet, $6/case).
//   Currently all orders treated as B2C pick/pack. Add B2B volume split per brand in V2.

// TODO: Dual-WMS overhead cost not included.
//   Running Amphora WMS alongside Shopify WMS in same warehouse has an incremental tech cost.
//   Confirm monthly cost with Amphora before finalizing cost model.

// TODO: Amphora counter rates exclude returns, onboarding, and mgmt fees entirely.
//   Downside scenario models these as $0 (per Amphora counter). Confirm whether these are
//   truly excluded from the agreement or just absent from Amphora's counter draft.

// TODO: Storage SKU fee UOM mismatch.
//   FBJ charges $12/SKU/month. Amphora counter is $6/linear ft. Not directly comparable.
//   Need to align UOM before finalizing storage revenue in negotiation scenario.

// TODO: 5,000 orders/brand planning assumption vs ~2,300 Excel actual.
//   The model uses 5,000/brand as the planning assumption. David's Excel named-brand data
//   implies ~2,300/brand at steady state. This is intentionally conservative/aspirational.
//   Add a note in the UI so users understand this delta.
```

---

## Visual Design

- **Color palette:** Navy `#1a2744`, Gold `#c9a227`, White `#ffffff`, Light grey `#f5f5f5`, Red `#c0392b`, Green `#27ae60`
- **Font:** Inter or equivalent clean sans-serif
- **Tone:** Institutional, data-first. Goldman Sachs analyst aesthetic. No gradients, no decorative elements.
- **KPI cards:** White, light shadow, colored top accent bar (gold = revenue, navy = net, green = positive, red = loss)
- **Scenario cards:** Equal width, side by side. Selected = green border. Others = muted grey border.
- **Tables:** Zebra striping, monospace numbers, right-aligned values. Negative net = red. Positive = green.
- **Phase badges:** RAMP = amber, GROWTH = teal, SCALE = green
- **Slider markers:** Thin vertical tick lines above slider track with small text label. Do not obstruct slider handle.
- **Charts (nice-to-have):** Cumulative net line with break-even crossover marker; stacked bar of 24-mo revenue by stream

---

## What NOT to Build

- No authentication or login
- No PDF/Excel export in V1
- No real-time data fetching — all computed from inputs
- No mobile optimization in V1 — desktop only
- No Amphora WMS integration — financial model only

---

## Deliverable

Single-page web application (React or plain HTML/CSS/JS — engineer's choice for what ships fastest and cleanest). Four tabs navigable by click. All calculations reactive — any input change updates all screens instantly. Default state on load = Base Case values. No sliders on Screens 1, 2, or 3.
