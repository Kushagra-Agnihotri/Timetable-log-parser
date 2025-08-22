from collections import Counter, defaultdict

PATH="timetable.log"

def to_ms(n, u):
    v=float(n)
    u=u.lower()
    return v/1000.0 if u in ("µs","us") else v*1000.0 if u=="s" else v

def parse_time(tok):
    i=0
    while i<len(tok) and (tok[i].isdigit() or tok[i]=='.'): i+=1
    return (tok[:i], tok[i:]) if i else ("0","ms")

alg=Counter()
endpoints=Counter()
status=Counter()
times=defaultdict(list)
ids_by_year=defaultdict(set)
found_total=found_count=total_reqs=0

for line in open(PATH,encoding="utf-8",errors="ignore"):
    line=line.strip()
    
    if "Using " in line and "Strategy" in line:
        start=line.find("Using ")+6
        end=line.find(" Strategy",start)
        alg[line[start:end].strip()]+=1

    if "Generation Complete" in line and "Found" in line and "timetables" in line:
        k=line.split("Found",1)[1].strip().split()[0]
        if k.isdigit(): found_total+=int(k)
        found_count+=1

    parts=line.split()

    for i,t in enumerate(parts):
        if t in ("GET","POST") and i+3<len(parts):
            ep=parts[i+1]; st=''.join(ch for ch in parts[i+2] if ch.isdigit())
            n,u=parse_time(parts[i+3].strip().strip("(),"))
            try:
                ms=to_ms(n,u); total_reqs+=1
                endpoints[ep]+=1; status[st]+=1; times[ep].append(ms)
            except: pass
            break
    s=line
    while True:
        a=s.find('['); b=s.find(']',a+1)
        if a==-1 or b==-1: 
            break
        val=s[a+1:b]
        if len(val)>=4 and val[:4].isdigit(): ids_by_year[val[:4]].add(val)
        s=s[b+1:]

# REPORT PRINT
print("TRAFFIC & USAGE ANALYSIS\n","-"*30)
print("Total API Requests Logged:", total_reqs)
print("HTTP Status codes:")
for i,t in dict(status).items():
    print("-->",i,":",t,"times")
print("\nEndpoint Popularity: \n")
for ep,c in endpoints.most_common(5):
    t=times[ep]
    avg=maxv=(0,)
    if t: avg=sum(t)/len(t)
    maxv=max(t)
    print(f" -{ep}: {c} reqs, avg={avg:.3f}ms, max={maxv:.3f}ms")
print("-"*30)
print("Timetables found:", found_total)
print("\nTotal generate calls:", found_count)
print("\navg:", (found_total/found_count) if found_count else 0)
print("\nAlgorithms:")
for i,t in dict(alg).items():
    print(f" - {i}: {t} times")
print("\nUnique IDs total:", sum(len(s) for s in ids_by_year.values()))
print("IDs by year:")
for i,t in ids_by_year.items():
    print(f"Batch of {i}: {len(t)}  unique")
