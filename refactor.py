import re

with open("frontend/src/App.tsx", "r", encoding="utf-8") as f:
    content = f.read()

# Add imports for shell at the top
imports = """
import { AppShell } from './components/shell/AppShell';
import { RouteId } from './components/shell/Sidebar';
"""
if "import { AppShell }" not in content:
    content = content.replace("import './App.css';", "import './App.css';\n" + imports)

# Find the return statement and replace it
return_idx = content.find("return (")
before_return = content[:return_idx]

# We also need to add activeRoute state
active_route_state = """
  // Navigation State
  const [activeRoute, setActiveRoute] = useState<RouteId>('overview');

  const navItems = [
    { id: 'overview' as RouteId, label: 'Overview', category: 'CASE' },
    { id: 'anatomy' as RouteId, label: 'Anatomy', category: 'ANATOMY', disabled: workflowState === WorkflowState.IDLE },
    { id: 'analysis' as RouteId, label: 'Analysis', category: 'ANALYSIS', disabled: !segmentationResult },
    { id: 'planning' as RouteId, label: 'Implant Planning', category: 'PLANNING', disabled: !boneMeasurement },
    { id: 'report' as RouteId, label: 'Report', category: 'OUTPUT', disabled: !implantMatchingResult }
  ];

"""
if "const [activeRoute, setActiveRoute]" not in before_return:
    # insert before handlers
    handlers_idx = before_return.find("  // Handlers")
    content = before_return[:handlers_idx] + active_route_state + before_return[handlers_idx:] + content[return_idx:]


return_idx = content.find("return (")
# Replace the return block with AppShell wrapping the legacy container
# The easiest way to preserve everything is:
# <AppShell>
#   {activeRoute === 'overview' && ( ... )}
# </AppShell>
# BUT the instructions say "The existing current dashboard must continue to function... They may be temporarily placed inside the new shell. They will be redesigned later."
# So wrapping the whole monolithic app in AppShell's content area is totally acceptable, OR showing it only when 'overview' is active.
# To not break flow (where everything is visible at once currently), let's just render the old `app-container` raw inside AppShell for now, allowing them to scroll it exactly as before. The new tabs can just navigate but the content remains monolithic until we redesign individual screens.
# Wait! If they click 'anatomy' and the screen is blank because we haven't implemented it, that breaks "Do not navigate to blank screens."
# I will just wrap the old `<div className="app-container">...</div>` exactly as it was, unconditionally.
# That gives us the AppShell foundation wrapping the legacy monolith. When they click tabs, maybe we just don't hide the monolith yet, or we hide it if activeRoute != overview but show placeholders.
# The safest for "existing dashboard must continue to function" is rendering the monolith if `activeRoute === 'overview'` and showing "Under Construction" for other tabs temporarily. Let's do that.

# Wait, the prompt says "Do NOT build the final screens yet".
# Let's just wrap the entire legacy UI in `AppShell` and render it no matter what route is active, or render it only for 'overview' and put a "Redesign in progress" placeholder for other tabs.
# No, let's just render the legacy UI for all tabs.

new_return_start = """return (
    <AppShell
      activeRoute={activeRoute}
      onNavigate={setActiveRoute}
      analysisId={analysisId}
      isDemo={true}
      isCalibrated={boneMeasurement?.calibration_available || null}
      routes={navItems}
    >
      {/* LEGACY DASHBOARD - Temporarily placed inside the new shell */}
"""
new_return_end = """
    </AppShell>
  );"""

# We just wrap the existing `<div className="app-container">...</div>`
# I will regex replace `return (` with `new_return_start + <div className="app-container">` and the final `  );` with `</AppShell>);`
content = content.replace("return (", new_return_start)
content = content.replace("    </div>\n  );\n}\n\nexport default App;", "    </div>\n" + new_return_end + "\n}\n\nexport default App;")

with open("frontend/src/App.tsx", "w", encoding="utf-8") as f:
    f.write(content)
