with open('frontend/src/App.tsx', 'r') as f:
    for line in f.readlines()[:80]:
        print(line, end='')
