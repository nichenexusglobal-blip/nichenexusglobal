import shutil, os, sys, time

# Key directories and files to copy from the hermes profile
src = r"C:\Users\Administrator\AppData\Local\hermes\profiles\nichenexusglobal"
dst = r"D:\hermes\profiles\nichenexusglobal"

# Copy all non-DB, non-node_modules files first
def should_skip(name, path):
    # Skip .db files (copy separately)
    if name.endswith(('.db', '.db-wal', '.db-shm')):
        return True
    # Skip node_modules (they're desktop source files, already on D)
    if 'node_modules' in path.split(os.sep):
        return True
    # Skip pycache
    if '__pycache__' in path.split(os.sep):
        return True
    return False

total = 0
copied = 0
errors = 0
skipped = 0

for dirpath, dirnames, filenames in os.walk(src):
    rel = os.path.relpath(dirpath, src)
    if rel == '.':
        dest_dir = dst
    else:
        dest_dir = os.path.join(dst, rel)
    
    # Skip node_modules entirely
    if 'node_modules' in rel.split(os.sep):
        continue
    
    os.makedirs(dest_dir, exist_ok=True)
    
    for f in filenames:
        src_f = os.path.join(dirpath, f)
        dst_f = os.path.join(dest_dir, f)
        total += 1
        
        if should_skip(f, dirpath):
            skipped += 1
            continue
        
        if os.path.exists(dst_f) and os.path.getsize(dst_f) == os.path.getsize(src_f):
            skipped += 1
            continue
            
        try:
            shutil.copy2(src_f, dst_f)
            copied += 1
        except Exception as e:
            if errors < 5:
                print(f"ERR: {f} -> {e}")
            errors += 1

print(f"Profile files: total={total}, copied={copied}, skipped={skipped}, errors={errors}")

# Copy important DB files
db_files = ['state.db', 'memory_store.db', 'response_store.db']
for db in db_files:
    src_db = os.path.join(src, db)
    dst_db = os.path.join(dst, db)
    for attempt in range(3):
        try:
            if os.path.exists(src_db):
                shutil.copy2(src_db, dst_db)
                sz = os.path.getsize(dst_db) / 1024 / 1024
                print(f"DB OK: {db} ({sz:.0f} MB)")
            break
        except Exception as e:
            if attempt < 2:
                print(f"DB retry {db}: {e}")
                time.sleep(2)
            else:
                print(f"DB SKIP: {db} -> locked by running process")
                errors += 1

# Also copy the top-level hermes config files and tool directories
top_src = r"C:\Users\Administrator\AppData\Local\hermes"
top_dst = r"D:\hermes"

# Config files
for f in ['active_profile', '.env', 'config.yaml']:
    sf = os.path.join(top_src, f)
    df = os.path.join(top_dst, f)
    try:
        if os.path.exists(sf):
            shutil.copy2(sf, df)
            print(f"Top OK: {f}")
    except Exception as e:
        print(f"Top ERR: {f} -> {e}")

# Tool directories (bin/, bootstrap-cache/)
for d in ['bin', 'bootstrap-cache']:
    sd = os.path.join(top_src, d)
    dd = os.path.join(top_dst, d)
    if os.path.isdir(sd):
        try:
            shutil.copytree(sd, dd, dirs_exist_ok=True,
                ignore=shutil.ignore_patterns('__pycache__'))
            print(f"Dir OK: {d}/")
        except Exception as e:
            print(f"Dir ERR: {d} -> {e}")

# Verify
ok = all([
    os.path.exists(r"D:\hermes\profiles\nichenexusglobal\config.yaml"),
    os.path.exists(r"D:\hermes\profiles\nichenexusglobal\skills"),
    os.path.exists(r"D:\hermes\active_profile")
])
print(f"Verification: {'PASS' if ok else 'FAIL'}")
if not ok:
    sys.exit(1)
