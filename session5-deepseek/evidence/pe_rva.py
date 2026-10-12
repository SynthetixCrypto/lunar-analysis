import json
p = r"C:\Users\Admin\Downloads\New folder\lunar-analysis\session4-sol\evidence-native\binding-pe-addresses.json"
d = json.load(open(p, encoding="utf-8"))
out = []
def walk(o):
    if isinstance(o, dict):
        if isinstance(o.get("name"), str) and "Java_com_moonsworth" in o["name"]:
            out.append(o)
        for v in o.values():
            walk(v)
    elif isinstance(o, list):
        for v in o:
            walk(v)
walk(d)
want = ["swapBuffers", "Session_getName", "setTimers", "invokeIteration0", "createEngine"]
for w in want:
    for e in out:
        if w in e["name"]:
            print(w, "->", json.dumps(e, ensure_ascii=False))
            break
print("total records:", len(out))
