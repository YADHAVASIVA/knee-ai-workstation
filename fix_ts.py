import os

filepath = os.path.join("frontend", "src", "App.tsx")
with open(filepath, "r", encoding="utf-8") as f:
    content = f.read()

content = content.replace("import type { RouteId } from './components/shell/Sidebar';", "")
with open(filepath, "w", encoding="utf-8") as f:
    f.write(content)
