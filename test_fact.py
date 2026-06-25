"""Test fact_list with a sample bullet"""
import sys
sys.path.insert(0, "C:/nichenexusglobal")
from fact_list import verify_facts

# Sample: better version of Mascom bullet
msg = """Hello Mascom team,

I am Pen from Nichenexusglobal, a sourcing company based in China. I see you stock EcoFlow RIVER 3 (245Wh) at KSh 33,000 in Nairobi.

We source LiFePO4 power stations from partner factories in China. A 2009Wh/1200W unit is available at $298 EXW.

Would your customers be interested in a product at this price point?"""

verify_facts(msg)
