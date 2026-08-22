import re
with open('frontend/src/App.tsx', 'r', encoding='utf-8') as f:
    app = f.read()

report_block = re.search(r'<Report\s+.*?\s*/>', app, re.DOTALL).group(0)
new_report_block = report_block.replace('<Report', '<Report onNavigate={handleNavigate as any}')
app = app.replace(report_block, new_report_block)

with open('frontend/src/App.tsx', 'w', encoding='utf-8') as f:
    f.write(app)
