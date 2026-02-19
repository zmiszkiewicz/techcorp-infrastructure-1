#!/usr/bin/env python3
"""
manual_dns.py — The "old way" of managing DNS.

This is what happens when someone writes a one-off script on their laptop.
Run it twice and notice the problems.
"""
import os
import random
import time

API_KEY = os.environ.get("BLOXONE_API_KEY", "HARDCODED_KEY_OOPS")
BASE_URL = "https://csp.infoblox.com/api/ddi/v1"
RUN_LOG = "/tmp/.manual_dns_runs"

# Hardcoded records — no environment separation
records = [
    {"name": "webserver", "ip": "10.0.0.5"},
    {"name": "dbserver", "ip": "10.0.0.6"},
    {"name": "appserver", "ip": "10.0.0.7"},
]

# Track how many times this script has been run
run_count = 0
if os.path.exists(RUN_LOG):
    with open(RUN_LOG) as f:
        run_count = int(f.read().strip() or "0")
run_count += 1
with open(RUN_LOG, "w") as f:
    f.write(str(run_count))

if run_count == 1:
    # First run — looks like it "works"
    print("Running DNS provisioning script...")
    print(f"Using API key: {API_KEY[:10]}... (hardcoded in script)")
    print()
    for r in records:
        time.sleep(0.3)
        print(f"  Creating {r['name']}.techcorp.local -> {r['ip']}...")
        print(f"    -> POST /dns/record ... 201 Created")
    print()
    print(f"Done! {len(records)} records created.")
    print()
    print("Looks good, right? Now run it again and see what happens...")

elif run_count == 2:
    # Second run — the chaos begins
    print("Running DNS provisioning script...")
    print(f"Using API key: {API_KEY[:10]}... (hardcoded in script)")
    print()
    for r in records:
        time.sleep(0.3)
        print(f"  Creating {r['name']}.techcorp.local -> {r['ip']}...")
        if r["name"] == "webserver":
            print(f"    -> POST /dns/record ... 201 Created")
            print(f"    ⚠️  DUPLICATE! 'webserver' already exists with same IP.")
            print(f"       But the script doesn't check — it just created a second one.")
        elif r["name"] == "dbserver":
            print(f"    -> POST /dns/record ... 201 Created")
            print(f"    ⚠️  DUPLICATE! Now there are TWO 'dbserver' records.")
            print(f"       Which one is correct? Nobody knows.")
        elif r["name"] == "appserver":
            print(f"    -> POST /dns/record ... 500 Internal Server Error")
            print(f"    ❌ API hiccup! Record may or may not have been created.")
            print(f"       The script doesn't retry or check. It just moves on.")
    print()
    print(f"'Done'! But what actually happened?")
    print(f"  - 2 duplicate records created (webserver, dbserver)")
    print(f"  - 1 record in unknown state (appserver — 500 error)")
    print(f"  - No way to roll back without manually checking each one")
    print(f"  - No audit trail of who ran this or when")
    print()
    print("This is Stage 2: One-off scripts. Fragile and dangerous at scale.")
    print()
    print("Now imagine: 10 engineers, 500 records, 3 environments, Friday at 5pm.")
    print("Still think scripts are 'good enough'?")

else:
    # Third+ run — total chaos
    print("Running DNS provisioning script... (attempt #{})".format(run_count))
    print(f"Using API key: {API_KEY[:10]}... (hardcoded in script)")
    print()
    outcomes = ["201 Created (DUPLICATE!)", "409 Conflict", "500 Server Error", "201 Created (TRIPLICATE!)"]
    total_dupes = 0
    total_errors = 0
    for r in records:
        time.sleep(0.2)
        outcome = random.choice(outcomes)
        print(f"  Creating {r['name']}.techcorp.local -> {r['ip']}...")
        print(f"    -> POST /dns/record ... {outcome}")
        if "DUPLICATE" in outcome or "TRIPLICATE" in outcome:
            total_dupes += 1
        if "Conflict" in outcome or "Error" in outcome:
            total_errors += 1
    print()
    print(f"Run #{run_count} complete. Results:")
    print(f"  - {total_dupes} duplicate/triplicate records (maybe)")
    print(f"  - {total_errors} errors (unhandled)")
    print(f"  - {run_count * len(records)} total API calls across all runs")
    print(f"  - 0 rollback capability")
    print(f"  - 0 audit trail")
    print()
    print("☠️  Your DNS is now a mess. Good luck figuring out what's real.")
    print("   This is why enterprises need Terraform + Ansible.")
