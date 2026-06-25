#!/usr/bin/env python3
"""
PRECISION GATE — 99% email quality enforcement
Runs after email is composed, BEFORE it hits SMTP.
If score < 95, the email is BLOCKED. No exceptions.

Scoring criteria (each 0-20 points, total 100):
1. Company name mentioned (20pts) — must name the target company
2. Specific business fact (20pts) — their products, brands, market position
3. Quantified value prop (20pts) — savings %, dollar amount, margin improvement
4. Pricing data present (20pts) — verified factory prices in the email
5. No AI/generic language (20pts) — no banned words, no generic hooks
"""

import re
import sys

# === BANNED AI/GENERIC WORDS ===
AI_BAN = [
    'delve', 'landscape', 'robust', 'unprecedented', 'cutting-edge',
    'game-changer', 'revolutionize', 'harness', 'empower', 'synergy',
    'ecosystem', 'paradigm', 'bespoke', 'AI-powered', 'leverage',
]

# === GENERIC HOOKS (these should NOT appear) ===
GENERIC_HOOKS = [
    'one of the fastest-growing categories',
    'cross-border trade connector',
    'zero installation cost',
    'plug-and-play products',
    'are you currently sourcing',
    'happy to discuss',
    '15-minute call to discuss how this might fit',
    'I am reaching out',
    'would you be open to',
]

class PrecisionGate:
    def __init__(self, company_name, email_body, company_info=None):
        self.company = company_name
        self.body = email_body
        self.info = company_info or {}
        self.score = 0
        self.checks = {}
        self.blocked = False
        self.reasons = []
    
    def check_company_name(self):
        """20pts: Must mention target company by name."""
        if self.company.lower() in self.body.lower():
            self.checks['company_name'] = (20, True, f'✅ Company name \"{self.company}\" found')
            return 20
        # Try partial match
        company_words = self.company.split()
        for word in company_words:
            if len(word) > 3 and word.lower() in self.body.lower():
                self.checks['company_name'] = (10, True, f'⚠️  Partial match: \"{word}\"')
                return 10
        self.checks['company_name'] = (0, False, f'❌ Company name \"{self.company}\" NOT in email')
        self.blocked = True
        self.reasons.append(f'Missing company name: {self.company}')
        return 0
    
    def check_business_fact(self):
        """20pts: Must reference at least one specific fact about their business."""
        # Check for product mentions
        product_kw = ['EcoFlow', 'Bluetti', 'Jackery', 'solar', 'LFP', 'LiFePO4', 'battery', 
                      'dealer', 'distributor', 'installer', 'retailer', 'authorized',
                      'DELTA', 'River', 'inverter', 'energy storage', 'power station',
                      'fábrica', 'estación', 'energía', 'marca', 'línea', 'OEM',
                      'portátil', 'paneles', 'generador']
        facts_found = []
        for kw in product_kw:
            if kw.lower() in self.body.lower():
                facts_found.append(kw)
        
        # Also check for brand detected in research
        if self.info.get('brands'):
            for brand in self.info['brands']:
                if brand.lower() in self.body.lower():
                    if brand not in facts_found:
                        facts_found.append(brand)
        
        # Must have at least 2 specific facts
        if len(facts_found) >= 2:
            self.checks['business_fact'] = (20, True, f'✅ {len(facts_found)} business facts: {facts_found[:5]}')
            return 20
        elif len(facts_found) == 1:
            self.checks['business_fact'] = (10, True, f'⚠️  Only 1 fact: {facts_found}')
            self.reasons.append(f'Only 1 business fact found. Need 2+ specific references.')
            return 10
        else:
            self.checks['business_fact'] = (0, False, '❌ No specific business facts')
            self.blocked = True
            self.reasons.append('No specific business facts about the company')
            return 0
    
    def check_quantified_value(self):
        """20pts: Must have a quantified value proposition."""
        # Look for dollar amounts, percentages, savings calculations
        patterns = [
            (r'USD\s*\d{1,3}(?:,\d{3})*(?:\.\d+)?', 'USD amount'),
            (r'\$\d{1,3}(?:,\d{3})*(?:\.\d+)?', 'dollar amount'),
            (r'\d{2,3}%', 'percentage'),
            (r'sav(e|ing).*?\d+', 'savings mention'),
            (r'\d{1,3}(?:,\d{3})*\s*(?:monthly|annual|per year|per month)', 'time-based value'),
            (r'margin.*?\d{1,3}', 'margin mention'),
            (r'delta.*?\d+', 'delta/improvement'),
            (r'\d+.*?(?:cheaper|less|below|saved|saving)', 'cost reduction'),
        ]
        
        found = []
        for pattern, label in patterns:
            matches = re.findall(pattern, self.body, re.IGNORECASE)
            if matches:
                found.append(label)
        
        if len(found) >= 2:
            self.checks['quantified_value'] = (20, True, f'✅ Value quantified: {found[:4]}')
            return 20
        elif len(found) == 1:
            self.checks['quantified_value'] = (10, True, f'⚠️  Only 1 value metric: {found}')
            self.reasons.append('Only 1 quantified value metric. Need more specific savings/price data.')
            return 10
        else:
            self.checks['quantified_value'] = (0, False, '❌ No quantified value proposition')
            self.blocked = True
            self.reasons.append('No quantified value (no dollar amounts, percentages, or savings data)')
            return 0
    
    def check_pricing(self):
        """20pts: Must include specific pricing data."""
        has_factory_price = bool(re.search(r'(?:USD\s*)?\$?\s*(?:145|150|240|298|430|199|300|500|130|249|288|620|610|898|918)\b', self.body))
        has_price_list = bool(re.search(r'(?:600W|1000W|2500W|299Wh|1024Wh|2048Wh)', self.body))
        
        if has_factory_price and has_price_list:
            self.checks['pricing'] = (20, True, '✅ Contains factory pricing + capacity specs')
            return 20
        elif has_factory_price:
            self.checks['pricing'] = (15, True, '⚠️  Has pricing but no capacity breakdown')
            return 15
        elif has_price_list:
            self.checks['pricing'] = (10, True, '⚠️  Has specs but no specific prices')
            self.reasons.append('Has product specs but missing specific factory prices')
            return 10
        else:
            self.checks['pricing'] = (0, False, '❌ No pricing data')
            self.blocked = True
            self.reasons.append('No factory pricing data in email')
            return 0
    
    def check_language(self):
        """20pts: No AI words, no generic hooks, strong CTA required."""
        penalties = 0
        issues = []
        
        # Check AI words
        for word in AI_BAN:
            pattern = r'\b' + re.escape(word.lower()) + r'\b'
            if re.search(pattern, self.body.lower()):
                issues.append(f'AI word: "{word}"')
                penalties += 2
        
        # Check generic hooks
        for hook in GENERIC_HOOKS:
            if hook.lower() in self.body.lower():
                issues.append(f'Generic: "{hook[:40]}..."')
                penalties += 3
        
        # Check CTA strength (6th precision requirement)
        strong_ctas = ['spec sheet', 'formal quotation', 'quotation', 'interested in',
                       'catálogo', 'cotización', 'muestras', 'catálogo completo']
        weak_ctas = ['would you be open to', 'happy to discuss', '15-minute call to discuss how this might fit']
        
        has_strong = any(c in self.body.lower() for c in strong_ctas)
        has_weak = any(c in self.body.lower() for c in weak_ctas)
        
        if has_weak and not has_strong:
            penalties += 5
            issues.append('Weak CTA: use "spec sheets" or "formal quotation" instead')
        elif not has_strong and not has_weak:
            penalties += 3
            issues.append('Missing CTA: add "Interested in spec sheets?" or similar')
        
        score = max(0, 20 - penalties)
        
        if penalties == 0:
            self.checks['language'] = (20, True, '✅ Clean language, strong CTA')
        elif score >= 15:
            self.checks['language'] = (score, True, f'⚠️  Minor: {issues}')
            self.reasons.extend(issues)
        else:
            self.checks['language'] = (score, False, f'❌ Issues: {issues}')
            self.blocked = True
            self.reasons.extend(issues)
            self.reasons.extend(issues)
        
        return score
    
    def evaluate(self):
        """Run all checks and return (total_score, passed, details)."""
        scores = [
            self.check_company_name(),
            self.check_business_fact(),
            self.check_quantified_value(),
            self.check_pricing(),
            self.check_language(),
        ]
        
        self.score = sum(scores)
        passed = self.score >= 95 and not self.blocked
        
        # Add truth check reminder (cannot be automated)
        result = {
            'score': self.score,
            'passed': passed,
            'threshold': 95,
            'checks': self.checks,
            'blocked_reasons': self.reasons,
            'verdict': '✅ APPROVED' if passed else '🚫 BLOCKED',
        }
        
        # Non-automated truth check reminder
        print(f"\n  ⚠ TRUTH CHECK (manual):")
        print(f"    [ ] All numbers verified from real sources?")
        print(f"    [ ] Not pretending to be something we're not?")
        print(f"    [ ] Would I say this face-to-face?")
        print(f"    [ ] Does this pass Pen's '真实与真诚' test?\n")
        
        return result


def gate_check(company_name, email_body, company_info=None):
    """Main entry point. Returns (passed, report_dict)."""
    gate = PrecisionGate(company_name, email_body, company_info)
    result = gate.evaluate()
    
    print(f"\n{'='*60}")
    print(f"PRECISION GATE: {company_name}")
    print(f"{'='*60}")
    
    for check_name, (pts, ok, msg) in result['checks'].items():
        print(f"  [{pts:2d}/20] {msg}")
    
    print(f"\n  TOTAL: {result['score']}/100 (need {result['threshold']})")
    print(f"  VERDICT: {result['verdict']}")
    
    if result['blocked_reasons']:
        print(f"\n  BLOCKED BECAUSE:")
        for reason in result['blocked_reasons']:
            print(f"    - {reason}")
    
    return result['passed'], result


if __name__ == '__main__':
    # Test with the RapidTech email
    test_email = '''RapidTech is an authorized EcoFlow dealer in Nairobi — you already have the customer base, the distribution, and the market knowledge for portable power stations.

Here is the opportunity: equivalent LiFePO4 portable power stations at factory-direct pricing.

Your current supply chain:
EcoFlow DELTA 3 Plus (1024Wh) — wholesale approximately USD 600/unit, retail USD 999

Our verified factory pricing (same chemistry, same capacity class):
ALLPOWERS R600 (299Wh): USD 150/unit
Pecron E1000LFP (1024Wh/1800W): USD 240/unit — landed Kenya approximately USD 310
Pecron E2400LFP (2048Wh/2400W): USD 430/unit — landed approximately USD 550

Delta per unit vs your current EcoFlow wholesale on the 1024Wh class: approximately USD 290 saved per unit. At 50 units per month, that is USD 14,500 in monthly savings — USD 174,000 annually.

Minimum order 50-100 units. 7-35 day production. All factories verified.

This is not a replacement for your EcoFlow line. It is a parallel private-label or house-brand opportunity at significantly better unit economics.

Would you like spec sheets and a formal quotation for the 1024Wh and 2048Wh models?

Pen
nichenexusglobal.com'''
    
    passed, result = gate_check('RapidTech', test_email)
    
    if not passed:
        print(f"\n🚫 EMAIL BLOCKED — score {result['score']}/100 (need 95)")
        sys.exit(1)
    else:
        print(f"\n✅ EMAIL APPROVED — score {result['score']}/100")
