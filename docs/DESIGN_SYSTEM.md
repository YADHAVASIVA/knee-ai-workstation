# Design System Foundation

## 1. CSS Tokens (`tokens.css`)

The application uses a unified CSS variables token system for a dark medical workstation aesthetic.

### Colors
```css
  --color-bg: #0f172a; 
  --color-surface: #1e293b; 
  --color-surface-elevated: #334155; 
  --color-surface-muted: #0f172a;
  --color-border: #334155;
  --color-border-strong: #475569;
  --color-text-primary: #f8fafc;
  --color-text-secondary: #cbd5e1;
  --color-text-muted: #94a3b8;
  --color-text-disabled: #475569;
  
  --color-primary: #0f766e; 
  --color-primary-hover: #115e59;
  --color-primary-active: #134e4a; 
  
  --color-secondary: #334155;
  --color-secondary-hover: #475569;
  
  --color-success: #15803d;
  --color-warning: #b45309; 
  --color-error: #b91c1c; 
  --color-info: #0369a1; 
  --color-demo: #6d28d9; 
```

### Typography
```css
  --font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
  --font-mono: 'ui-monospace', 'SFMono-Regular', Consolas, monospace;
```
Font sizes scale from `--font-size-xs` (12px) to `--font-size-3xl` (30px).

### Spacing
8px grid foundation:
```css
  --space-1: 4px;
  --space-2: 8px;
  --space-3: 12px;
  --space-4: 16px;
  --space-5: 24px;
  --space-6: 32px;
  --space-7: 40px;
  --space-8: 48px;
  --space-9: 64px;
```

### Radius & Shadows
```css
  --radius-sm: 4px;
  --radius-md: 6px;
  --radius-lg: 8px;
  --radius-xl: 12px;
  
  --shadow-sm: 0 1px 2px rgba(0, 0, 0, 0.3);
  --shadow-md: 0 4px 6px -1px rgba(0, 0, 0, 0.4), 0 2px 4px -1px rgba(0, 0, 0, 0.24);
  --shadow-lg: 0 10px 15px -3px rgba(0, 0, 0, 0.5), 0 4px 6px -2px rgba(0, 0, 0, 0.25);
```

## 2. Foundational Components

### Layout Shell (`AppShell`, `Sidebar`, `TopBar`)
Provides the dark workstation wrapper. Features a 260px fixed sidebar and a 64px top bar. Responsive down to 768px (sidebar moves to top horizontally).

### Interactive Primitives
- **Button:** Supports `primary`, `secondary`, `ghost`, and `danger` variants. Explicitly handles `:hover`, `:active`, and `:disabled` states.
- **StatusBadge:** Semantic pill component rendering distinct colors and icons based on status (`SUCCESS`, `WARNING`, `DEMO`, etc.).
- **Card / Panel:** Container primitives using the `--color-surface` tokens. Includes elevated variations and header integration.
- **SectionHeader:** Unified title + optional action button wrapper.

## 3. Accessibility & Motion
- **Focus:** All interactive elements use `:focus-visible` with a `2px solid var(--color-primary)` outline.
- **Motion:** Fade and color transitions utilize `--transition-fast` (150ms). No excessive bounding or continuous animation.
