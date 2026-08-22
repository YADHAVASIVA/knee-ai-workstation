import os

def insert_prop(filepath, prop_decl, prop_usage):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    if prop_decl not in content:
        content = content.replace('onNavigate: (route: string) => void;', f'onNavigate: (route: string) => void;\\n  {prop_decl}')
    if prop_usage not in content:
        content = content.replace('onNavigate,', f'onNavigate,\\n  {prop_usage}')
        
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)

insert_prop('frontend/src/pages/CaseOverview.tsx', 'onReset?: () => void;', 'onReset,')
insert_prop('frontend/src/pages/Anatomy.tsx', 'isDemo?: boolean;', 'isDemo,')

with open('frontend/src/App.Navigation.test.tsx', 'r', encoding='utf-8') as f:
    lines = f.readlines()
with open('frontend/src/App.Navigation.test.tsx', 'w', encoding='utf-8') as f:
    for line in lines:
        if 'import * as api from' not in line:
            f.write(line)
