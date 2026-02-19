# atlas
Below is a full, detailed “hackathon-ready” documentation spec for your project (search-engine landing page → generates a mini-app workspace, **but keeps user agency via user-chosen sources + evidence-linked suggestions**). I’m writing it so you can basically copy/paste it into a README / Devpost submission, and also use it as your **prompt-engineering + build to-do list**.

---

# Project Documentation: **Atlas** (Search → Mini-App Workspace)

## 1) What Atlas Is

**Atlas is an AI-powered search engine that doesn’t answer questions for you.**
Instead, it turns your search query into a **user-controlled mini-app workspace** that helps you research, compare sources, and make decisions yourself.

Example query:

> “I’m planning a trip to Japan and want to focus on food and affordability”

Atlas generates a “Trip Research Workspace” with:

* a map panel
* a calendar/itinerary panel
* a budget/comparison panel
* a sources panel (user picks sources)
* a saved items panel (only user-curated)
* an “AI suggestions” panel that is **always evidence-linked** (no “just trust me” answers)

**Key philosophy:**

> AI builds the tools. Humans build the answers.

---

## 2) Why This Exists

Most AI products act like “answer machines,” which makes users passive and discourages real research.

Atlas is different:

* users **choose sources**
* users **open and read** resources
* AI **organizes** and **structures** work
* AI does **not** finalize decisions
* nothing gets added to the “Saved” area without user action

Atlas is a **research operating system**, not a chatbot.

---

## 3) Target Users

* Hackathon judges (need a wow demo in <30 seconds)
* Students doing research (travel, studying, purchases, projects)
* Anyone who wants AI assistance without losing control/critical thinking

---

## 4) Core Requirements (Must-Haves)

### R1 — Search Engine Landing Page

* Landing page looks like a search engine:

  * centered logo + search bar
  * suggested prompt chips (examples)
  * recent searches (optional)
* User enters a query and submits

### R2 — Query → Workspace Generator

Upon submission, Atlas must:

* classify the query into a “workspace type”
* generate a mini-app layout (panels)
* populate the “Sources” area with suggested resource categories
* populate “AI suggestions” with evidence-linked items

### R3 — User Agency Built Into Every Workspace

Every generated mini-app must include:

* **Sources Panel**: user selects which sources to include (toggles or “add sources”)
* **Saved Panel**: only user-selected items appear here
* **Evidence-linked AI Suggestions**: every suggestion includes citations/links/where it came from
* **No auto-commit**: AI can’t “finalize” itinerary, purchases, etc.

### R4 — Consistent Panel Pattern Across All Apps

Every workspace should follow the same mental model:

1. **Sources (User picks)**
2. **Workspace Tools (AI builds)**
3. **Suggestions (AI proposes, with evidence)**
4. **Saved (User commits)**

### R5 — Demo-Ready “Wow” Transition

The search page should “morph” into the workspace:

* simple animation is fine (fade/expand)
* but it must feel like the tab “turns into an app”

---

## 5) Nice-to-Haves (Premium / “Pro” Features)

These are optional but great for hackathon judging + business story:

* **P1: Workspace Persistence** (save and return later)
* **P2: Multi-Workspace Tabs** (run multiple apps side-by-side)
* **P3: Source Packs** (e.g., “Reddit pack,” “Academic pack,” “YouTube pack”)
* **P4: Export** (export itinerary / table / notes as PDF/Markdown/JSON)
* **P5: Edit Mode** (rearrange panels, add modules like “comparison table”)
* **P6: Evidence Score** (shows “# of sources” behind suggestion)

For hackathon: implement P1 + P4 if you can.

---

## 6) Non-Goals (To Stay Hackathon-Scoped)

* Not building a full web crawler
* Not building a new search index
* Not trying to “beat Google”
* Not implementing complex authentication unless necessary
* Not implementing live flight/hotel booking

Your demo can be “smartly faked”:

* use APIs for a few things
* use curated sample sources for others
* focus on UX + workflow + clarity

---

# 7) Product UX Specification

## 7.1 Landing Page (Search UI)

**Components:**

* Logo: “Atlas”
* Search input
* Prompt chips:

  * “Plan a Japan trip focused on food & affordability”
  * “Find a gym routine for beginners”
  * “Choose a laptop for CS student under $900”
  * “Build a 4-week React learning plan”
* Minimal nav:

  * “Workspaces”
  * “Premium”
  * “About”

**Submission flow:**

* Enter query → hit enter → transition to workspace view

## 7.2 Workspace Layout (Default)

**Left Sidebar: Sources**

* toggles / checkboxes:

  * Web
  * Reddit
  * YouTube
  * Maps
  * Academic
* “Add custom source link”
* “Search within sources” box

**Center: Main Tools**
Depends on workspace type:

* travel: map + itinerary calendar
* purchase research: comparison table + spec tracker
* study plan: schedule + curriculum checklist

**Right Sidebar: Saved**

* Saved items list
* user notes
* tags

**Bottom Drawer: AI Suggestions**

* Suggestions with:

  * “why suggested”
  * linked evidence
  * “Save” button

**Rule:** Suggestions never appear in Saved until user hits Save.

---

# 8) Functional Architecture

## 8.1 High-Level Flow

1. User enters query
2. Backend “Planner” classifies query → `workspace_type`
3. Backend generates:

   * `workspace_schema` (layout + modules)
   * `source_strategy` (which sources recommended)
   * `suggested_queries` (what to search in each source)
4. Frontend renders workspace
5. User selects sources and explores
6. Backend fetches results (or uses APIs / curated lists)
7. AI summarizes *only after user selects items* (optional)
8. User saves items + exports

---

## 8.2 Data Model (Simple JSON)

### Workspace

```json
{
  "id": "ws_123",
  "query": "plan japan food trip affordable",
  "workspace_type": "travel_research",
  "modules": [
    { "type": "sources_panel" },
    { "type": "map_panel" },
    { "type": "itinerary_panel" },
    { "type": "budget_panel" },
    { "type": "saved_panel" },
    { "type": "suggestions_panel" }
  ],
  "enabled_sources": ["web", "maps", "reddit"],
  "suggestions": [],
  "saved_items": []
}
```

### Suggestion item (must include evidence)

```json
{
  "title": "Tsukiji Outer Market",
  "category": "food",
  "reason": "High density of affordable street food options",
  "evidence": [
    { "source": "maps", "label": "Google Maps", "url": "..." },
    { "source": "reddit", "label": "Reddit thread", "url": "..." }
  ],
  "actions": ["save", "open"]
}
```

### Saved item (user-curated)

```json
{
  "type": "place",
  "title": "Ichiran Ramen Shibuya",
  "notes": "Go early to avoid lines",
  "links": ["..."],
  "tags": ["ramen", "budget"]
}
```

---

# 9) Tech Stack (Aligned With Your Skills)

You’ve used **Python**, **Streamlit**, OpenCV/MediaPipe, AWS S3, general web dev. For a hackathon, you want speed + clean UI.

## Recommended Stack (Fast + Modern + You-friendly)

### Frontend

* **Next.js (React)** — quick routing, easy deployment
* **Tailwind CSS** — fast UI polish
* **Framer Motion** — the “search → app morph” animation
* Optional: **shadcn/ui** for clean components

### Backend (AI Orchestrator)

Pick ONE:

**Option A (fastest for you if you like Python):**

* **FastAPI (Python)** — endpoints for classification + schema generation + suggestions
* Great for prompt iteration + quick logic changes

**Option B (one-stack JS):**

* Next.js API routes — okay, but Python is often faster for you to iterate prompts

### AI / LLM Layer

* Any accessible LLM provider (keep it abstract in your doc)
* Prompt templates (below)

### Integrations (Pick 1–2 max)

* **Google Maps Embed** (simple) or Mapbox
* “Web results” can be:

  * curated / mocked (hackathon acceptable)
  * or via a search API if you have one

### Storage (for persistence)

* **LocalStorage** for MVP
* Optional upgrade:

  * **Supabase** (super fast)
  * or **Firebase**
  * or your familiar **AWS S3** (but DB fits better than object store here)

### Deployment

* Vercel for Next.js
* Render/Railway for FastAPI

**Hackathon MVP recommendation:**
Next.js + FastAPI + LocalStorage + Maps Embed

---

# 10) Prompt Engineering Spec (Core of the Product)

Your backend should do 3 prompt tasks:

1. **Classifier**: what workspace type is this query?
2. **Schema Generator**: what modules should the workspace include?
3. **Suggestion Generator**: what should the AI suggest WITH evidence placeholders?

## 10.1 Workspace Types (Start with 4)

* `travel_research`
* `purchase_research`
* `learning_plan`
* `project_planner`

(You can add more later.)

---

## 10.2 Prompt: Classifier

**Goal:** output JSON only.

**System:**

* You are a classifier. Return strict JSON.
* Choose one workspace_type from list.
* Provide confidence 0–1.
* Provide a 1-sentence rationale.

**User:**

* Query: “{user_query}”

**Expected JSON:**

```json
{
  "workspace_type": "travel_research",
  "confidence": 0.86,
  "rationale": "User is planning a trip with constraints on food and affordability."
}
```

---

## 10.3 Prompt: Schema Generator

**Inputs:**

* user_query
* workspace_type

**Outputs:**

* modules list
* default sources to recommend
* suggested queries per source (what to search)

**Expected JSON:**

```json
{
  "title": "Japan Food & Budget Trip Workspace",
  "modules": [
    {"type":"sources_panel"},
    {"type":"map_panel"},
    {"type":"itinerary_panel"},
    {"type":"budget_panel"},
    {"type":"saved_panel"},
    {"type":"suggestions_panel"}
  ],
  "recommended_sources": ["maps","web","reddit","youtube"],
  "source_queries": {
    "maps": ["cheap ramen tokyo", "street food osaka"],
    "reddit": ["best cheap eats tokyo reddit", "japan budget food itinerary"],
    "youtube": ["tokyo food guide budget", "osaka street food"]
  }
}
```

---

## 10.4 Prompt: Suggestions Generator (Evidence-Linked)

**Important:** The model must not “decide” — only propose options with evidence slots.

**Rules:**

* Never state final answers.
* Every suggestion must include evidence links (or placeholders if not fetched).
* Suggestions go to “Suggestions panel,” not “Saved.”

**Expected JSON:**

```json
{
  "suggestions": [
    {
      "title": "Tsukiji Outer Market",
      "category": "food",
      "reason": "Commonly recommended for affordable street food and sampling.",
      "evidence_needed": ["maps", "reddit", "youtube"],
      "followup_user_action": "Open sources and decide whether to save."
    }
  ]
}
```

---

# 11) Build Plan + Running To-Do List (Hackathon Checklist)

This is your “do it in order” plan.

## Phase 0 — Repo Setup

* [ ] Create Next.js app + Tailwind
* [ ] Add basic pages: `/` (search), `/workspace/[id]`
* [ ] Create FastAPI backend scaffold (if using Python)
* [ ] Setup `.env` for API keys

## Phase 1 — Landing Page (Search Engine Feel)

* [ ] Centered logo + search bar
* [ ] Prompt chips
* [ ] On submit: call backend `POST /api/workspace/create`
* [ ] Animate transition (Framer Motion): search → workspace

## Phase 2 — Workspace Rendering (Static First)

* [ ] Build layout grid:

  * left: Sources
  * center: Main panel (placeholder)
  * right: Saved
  * bottom: Suggestions
* [ ] Create module components:

  * [ ] SourcesPanel
  * [ ] SavedPanel
  * [ ] SuggestionsPanel
  * [ ] MapPanel (embed)
  * [ ] ItineraryPanel (simple list/calendar)
  * [ ] Comparison/BudgetPanel (table)

## Phase 3 — AI Orchestration (Core)

* [ ] Implement classifier prompt call
* [ ] Implement schema prompt call
* [ ] Implement suggestions prompt call
* [ ] Return `workspace_schema` JSON to frontend

## Phase 4 — User Agency Rules (Differentiator)

* [ ] Suggestions have **Save** button
* [ ] Only clicking Save moves it to SavedPanel
* [ ] Evidence links show under every suggestion
* [ ] Sources toggles update “what suggestions are generated”
* [ ] Add “Add custom source link” input

## Phase 5 — “Research Flow” UX

* [ ] Clicking a source opens it in:

  * [ ] new tab OR
  * [ ] in-app webview panel (optional)
* [ ] “Save excerpt” / “Save link” button (MVP can be “save link” only)
* [ ] Notes per saved item

## Phase 6 — Persistence + Export (Premium-ish)

* [ ] Save workspace to LocalStorage
* [ ] Export workspace as JSON / Markdown
* [ ] (Optional) Supabase persistence

## Phase 7 — Demo Polish

* [ ] 2–3 workspace types fully demoable
* [ ] Beautiful empty states
* [ ] Fast loading skeleton UI
* [ ] A scripted demo query set

---

# 12) “Prompt Engineering To-Do List” (Operational)

This is your iterative prompt checklist.

## Prompt Iteration Checklist

* [ ] Classifier always returns valid JSON
* [ ] Schema generator always returns valid JSON
* [ ] Suggestions always include evidence fields
* [ ] Suggestions never “finalize” decisions
* [ ] Suggestions phrased as options, not conclusions
* [ ] Limit suggestions to 5–8 for clarity
* [ ] Ensure module selection fits workspace type
* [ ] Add guardrails: “do not add to saved list automatically”

## Prompt Regression Tests (Copy/paste queries)

Use these queries to test stability:

1. “Plan Japan trip focused on food & affordability”
2. “Help me choose a laptop for CS under $900”
3. “Make me a 4-week plan to learn React”
4. “Plan a hackathon project idea around accessibility”

Expected:

* correct workspace type
* consistent layout
* evidence-linked suggestions

---

# 13) Acceptance Criteria (What “Done” Means)

You can call the project complete if:

* Search page feels like a search engine
* Submitting query generates a workspace
* Workspace contains Sources + Suggestions + Saved at minimum
* Suggestions include evidence links/slots
* User must click “Save” to commit anything
* At least 2 workspace types work end-to-end
* Demo is smooth and visually impressive

---

# 14) Devpost / Pitch Blurb (Use This)

**Atlas is an AI search engine that transforms your query into a mini-app workspace—without replacing your thinking.**
Instead of generating answers, Atlas generates **tools**: source panels, maps, calendars, comparison tables, and evidence-linked suggestions. Users choose their sources, conduct their own research, and build conclusions themselves. AI organizes the workflow; humans stay in control.

---

If you want, I can also generate:

* a complete README version of this (formatted + badges + run commands)
* a 36-hour hackathon timeline (hour-by-hour)
* the exact JSON schemas + FastAPI endpoints + prompt templates you can paste into code immediately
