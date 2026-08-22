import os

with open('frontend/src/App.tsx', 'r', encoding='utf-8') as f:
    content = f.read()

content = content.replace('onReset={resetWorkflow}', '')
content = content.replace('isDemo={isDemo}', '')

with open('frontend/src/App.tsx', 'w', encoding='utf-8') as f:
    f.write(content)

with open('frontend/src/App.Navigation.test.tsx', 'r', encoding='utf-8') as f:
    content = f.read()

content = content.replace("import * as api from './api';", "")

with open('frontend/src/App.Navigation.test.tsx', 'w', encoding='utf-8') as f:
    f.write(content)
