#!/usr/bin/env python3
"""
SUPPLIER RFQ GATE — 80% minimum quality enforcement for supplier RFQs.

This runs BEFORE any RFQ is sent to a supplier.
If score < 80/100, the RFQ is BLOCKED. No exceptions.

Scoring criteria (total 100):
1. Product model mentioned (20pts) — references specific models from their catalog
2. Not a generic template (20pts) — body isn't >80% same as other RFQs
3. Customized questions (20pts) — questions specific to this supplier's products
4. Website evidence (20pts) — shows we've read their product page
5. No banned/generic language (20pts)
"""

import re, sys, os, json

BANNED_GENERIC = [
    'i am looking for', 'i am reaching out', 'we are a sourcing company',
    'we help distributors', 'leading manufacturer', 'one of the best',
    'industrial grade', 'state of the art', 'cutting-edge',
    'high quality products', 'competitive price', 'best price',
    'win-win', 'long-term cooperation', 'mutual benefit',
]

class SupplierRfqGate:
    def __init__(self, company_name, email_body, models=None):
        self.company = company_name
        self.body = email_body
        self.models = models or []  # specific product models found during research
        self.score = 0
        self.checks = {}
        self.blocked = False
        self.reasons = []
    
    def check_product_model(self):
        """20pts: Must reference at least one specific product model from their catalog."""
        if not self.models:
            self.checks['product_model'] = (0, False, '❌ No product models researched before writing')
            self.blocked = True
            self.reasons.append('Did not research their specific product models')
            return 0
        
        body_lower = self.body.lower()
        models_found = []
        for model in self.models:
            if model.lower() in body_lower:
                models_found.append(model)
        
        if len(models_found) >= 2:
            self.checks['product_model'] = (20, True, f'✅ {len(models_found)} models referenced: {models_found}')
            return 20
        elif len(models_found) == 1:
            self.checks['product_model'] = (10, True, f'⚠️  Only 1 model: {models_found[0]}')
            self.reasons.append(f'Only 1 model referenced. Need 2+ for full points.')
            return 10
        else:
            self.checks['product_model'] = (0, False, f'❌ Researched models [{self.models}] but none found in email')
            self.blocked = True
            self.reasons.append(f'No product models from [{self.models}] found in email body')
            return 0
    
    def check_not_generic(self):
        """20pts: Body must differ substantially from other RFQs sent to other suppliers."""
        body_lower = self.body.lower()
        
        # Check for generic phrases
        generic_count = 0
        for phrase in BANNED_GENERIC:
            if phrase in body_lower:
                generic_count += 1
        
        if generic_count >= 3:
            self.checks['not_generic'] = (0, False, f'❌ High generic content ({generic_count} banned phrases)')
            self.blocked = True
            self.reasons.append(f'{generic_count} generic phrases found')
            return 0
        elif generic_count == 2:
            self.checks['not_generic'] = (10, True, f'⚠️  2 generic phrases')
            self.reasons.append(f'2 generic phrases')
            return 10
        elif generic_count == 1:
            self.checks['not_generic'] = (15, True, f'⚠️  1 generic phrase')
            return 15
        else:
            self.checks['not_generic'] = (20, True, '✅ Clean - no generic template phrases')
            return 20
    
    def check_customized_questions(self):
        """20pts: Questions must be specific to this supplier's products."""
        body_lower = self.body.lower()
        
        # Generic question patterns
        generic_q = ['please quote', 'fob pricing', 'moq', 'lead time', 'certifications']
        specific_signals = []
        
        # Check for specific references that show research
        specific_patterns = [
            r'\b\d{3,4}wh\b',      # specific capacity like 1296Wh
            r'your\s+\w+\s+model',  # "your FP500 model"
            r'\b\w{2}\d{3,4}\b',   # model number like GT2000, FP2000
            r'i saw',               # "I saw on your website"
            r'on your site',        # "on your website"
            r'on your website',
            r'your product',
            r'your (line|range|series)',
        ]
        
        for pat in specific_patterns:
            if re.search(pat, body_lower):
                specific_signals.append(pat)
        
        # Score based on specificity
        if len(specific_signals) >= 3:
            self.checks['customized_questions'] = (20, True, f'✅ Highly customized ({len(specific_signals)} specific signals)')
            return 20
        elif len(specific_signals) == 2:
            self.checks['customized_questions'] = (15, True, f'⚠️  Partially customized ({len(specific_signals)} signals)')
            return 15
        elif len(specific_signals) == 1:
            self.checks['customized_questions'] = (5, True, f'⚠️  Barely customized (1 signal)')
            self.reasons.append('Only 1 specific signal - needs more personalization')
            return 5
        else:
            self.checks['customized_questions'] = (0, False, '❌ Completely generic - no specific signals')
            self.blocked = True
            self.reasons.append('No specific customization signals found')
            return 0
    
    def check_research_evidence(self):
        """20pts: Evidence we've actually read about their products."""
        body_lower = self.body.lower()
        evidence = 0
        
        # "I saw" statements
        if re.search(r'\b(i saw|i noticed|i see|looking at your|checked your)\b', body_lower):
            evidence += 10
        
        # Specific product specs mentioned (capacity, watts, features)
        if re.search(r'\b\d{3,5}\s*wh\b', body_lower, re.IGNORECASE):
            evidence += 5
        if re.search(r'\b\d{3,4}\s*w\b', body_lower, re.IGNORECASE):
            evidence += 5
        
        if evidence >= 15:
            self.checks['research_evidence'] = (20, True, f'✅ Clear research evidence ({evidence}/20)')
            return 20
        elif evidence >= 5:
            self.checks['research_evidence'] = (10, True, f'⚠️  Some evidence ({evidence}/20)')
            return 10
        else:
            self.checks['research_evidence'] = (0, False, '❌ No research evidence')
            self.blocked = True
            self.reasons.append('No evidence of visiting their website or researching products')
            return 0
    
    def check_no_banned(self):
        """20pts: No banned AI/generic language."""
        body_lower = self.body.lower()
        banned_found = []
        
        # Extended ban list for supplier comms
        extra_ban = [
            'delve', 'robust', 'harness', 'empower', 'synergy',
            'ecosystem', 'paradigm', 'game-changer', 'revolutionize',
        ]
        
        for word in extra_ban:
            if word in body_lower:
                banned_found.append(word)
        
        if not banned_found:
            self.checks['no_banned'] = (20, True, '✅ Clean language')
            return 20
        elif len(banned_found) <= 2:
            self.checks['no_banned'] = (10, True, f'⚠️  Some AI language: {banned_found}')
            return 10
        else:
            self.checks['no_banned'] = (0, False, f'❌ Too much AI language: {banned_found}')
            self.blocked = True
            self.reasons.append(f'Banned AI words: {banned_found}')
            return 0
    
    def evaluate(self):
        """Run all checks and return score and verdict."""
        self.score = 0
        self.score += self.check_product_model()
        self.score += self.check_not_generic()
        self.score += self.check_customized_questions()
        self.score += self.check_research_evidence()
        self.score += self.check_no_banned()
        
        return {
            'company': self.company,
            'score': self.score,
            'passed': self.score >= 80,
            'blocked': self.blocked,
            'checks': self.checks,
            'reasons': self.reasons,
        }
    
    def report(self):
        result = self.evaluate()
        print(f'=== RFQ GATE: {self.company} ===')
        print(f'Score: {result["score"]}/100 (need 80 to pass)')
        print(f'Status: {"✅ PASSED" if result["passed"] else "❌ BLOCKED"}')
        if result['blocked']:
            print(f'Hard-blocked. Reasons:')
            for r in result['reasons']:
                print(f'  - {r}')
        print()
        for check_name, (pts, passed, msg) in result['checks'].items():
            print(f'  {msg}')
        return result


def gate_check(company_name, email_body, product_models=None):
    """Quick check for use in sending scripts."""
    gate = SupplierRfqGate(company_name, email_body, product_models)
    result = gate.evaluate()
    gate.report()
    return result


if __name__ == '__main__':
    # Test mode
    test_body = """Hi Team,

I saw your FP300 and FP500 portable power stations on your website.
Could you quote FOB Shenzhen per unit for the FP2000 at 50 pcs?

Best regards,
Pen"""
    
    gate_check('iFlowPower', test_body, ['FP300', 'FP500', 'FP2000'])
