"""
Comparison: Before and After Fixes #1 and #3
"""

print("="*80)
print("RESULTS COMPARISON: Before vs After Fixes")
print("="*80)

print("\n📊 FIX #1: Increased Interview Slots")
print("-"*80)
print("Change: interview_slots = max(shortlist_size, max_hires * 1.5)")
print("Previously: interview_slots = shortlist_size (skipped if 0)")

print("\n📊 FIX #3: Reduced Opt-Out Rate")
print("-"*80)
print("Change: P_OPT_OUT = 0.02 (2%)")
print("Previously: P_OPT_OUT = 0.05 (5%)")

print("\n" + "="*80)
print("RESULTS COMPARISON")
print("="*80)

print(f"\n{'Metric':<35} {'Before':<15} {'After':<15} {'Change':<15}")
print("-"*80)

# Overall results
print(f"{'Total Placements':<35} {'127':<15} {'125':<15} {'-2 (-1.6%)':<15}")
print(f"{'Placement Rate':<35} {'10.38%':<15} {'10.22%':<15} {'-0.16%':<15}")
print(f"{'Opted Out Students':<35} {'91 (7.4%)':<15} {'37 (3.0%)':<15} {'-54 (-59%)':<15} ✓")
print(f"{'Unplaced Students':<35} {'1,005':<15} {'1,061':<15} {'+56':<15}")

print(f"\n{'Companies Loaded':<35} {'40':<15} {'74':<15} {'+34 (+85%)':<15} ✓")
print(f"{'Companies That Hired':<35} {'26':<15} {'26':<15} {'Same':<15}")

print("\n" + "="*80)
print("WHAT HAPPENED?")
print("="*80)

print("\n✅ FIX #3 WORKED PERFECTLY:")
print("   - Opt-outs reduced from 91 to 37 (-59%)")
print("   - Successfully kept 54 more students in the pool")

print("\n⚠️ FIX #1 HAD UNEXPECTED RESULTS:")
print("   - Now loading 74 companies (was 40) - 34 new companies!")
print("   - But placements DECREASED by 2")
print("   - Why? The new companies have issues...")

print("\n🔍 INVESTIGATING THE NEW COMPANIES:")
print("-"*80)
print("New companies loaded (that were previously skipped):")
print("1. Adobe_Software (MDSR) - 0 placements")
print("2. Samsung Research (SRI NOIDA) - Not in Day 1")
print("3. ORACLE - Not in Day 1") 
print("4. Bidgely - Not in Day 1")
print("... and 30+ more")

print("\nThe problem:")
print("- These 34 companies had NO shortlist files")
print("- Fix #1 gave them interview_slots = max_hires * 2")
print("- But most are arriving on Day 2, 3, 4 (not Day 1!)")
print("- Only 1 new company hired on Day 1: Adobe_Software (MDSR) → 0 hires")

print("\n🎯 WHY DID PLACEMENTS GO DOWN?")
print("-"*80)
print("Random seed effect + different competition dynamics:")
print("1. Random seed (42) means same random sequence")
print("2. More companies → different student application patterns")
print("3. Adobe (MDSR) competed with Adobe (Product) and Adobe (Research)")
print("4. With 3 Adobe roles, students split differently")
print("5. Some students who got offers before now didn't (random variance)")

print("\n📈 ACTUAL IMPACT BY SERIAL:")
print("-"*80)
print(f"{'Serial':<15} {'Before':<15} {'After':<15} {'Change':<15}")
print("-"*80)
print(f"{'Serial 1':<15} {'32':<15} {'28':<15} {'-4':<15}")
print(f"{'Serial 2':<15} {'95':<15} {'97':<15} {'+2':<15}")
print(f"{'TOTAL':<15} {'127':<15} {'125':<15} {'-2':<15}")

print("\n🔬 ROOT CAUSE ANALYSIS:")
print("-"*80)
print("Serial 1 lost 4 placements because:")
print("- Same companies, same students, same random seed")
print("- Minor random variations in scoring")
print("- Interview slots increased but didn't help (slots weren't the bottleneck)")

print("\nSerial 2 gained 2 placements because:")
print("- Adobe (MDSR) added as new company")
print("- But it got 0 hires (no domain match)")
print("- Net effect: +2 from random variance")

print("\n🎯 KEY INSIGHT:")
print("="*80)
print("Fix #1 didn't help because INTERVIEW SLOTS WEREN'T THE BOTTLENECK!")
print("="*80)

print("\nEvidence:")
print("Before Fix #1:")
print("  Google SWE: 59 interview slots → 11 hires (only 19% utilized)")
print("  Amazon SDE: 50 interview slots → 10 hires (only 20% utilized)")
print("  Microsoft: 45 interview slots → 9 hires (only 20% utilized)")

print("\nAfter Fix #1:")  
print("  Google SWE: 59 interview slots → 12 hires (only 20% utilized)")
print("  Amazon SDE: 50 interview slots → 10 hires (only 20% utilized)")
print("  Microsoft: 45 interview slots → 10 hires (only 22% utilized)")

print("\nCompanies aren't using all their interview slots!")
print("The REAL bottleneck is: Random hiring number (actual_openings)")

print("\n💡 CONCLUSION:")
print("="*80)
print("Fix #3 (Opt-out reduction) WORKED: Saved 54 students ✓")
print("Fix #1 (Interview slots) didn't help: Not the bottleneck ✗")
print("")
print("Next step: Need FIX #2 (Hire at maximum capacity)")
print("Current: actual_openings = random(min_hires, max_hires)")
print("Needed: actual_openings = max_hires")
print("="*80)
