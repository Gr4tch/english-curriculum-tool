# Component Blueprint & UI Specification (`UI_SPEC.md`)

Companion specification to [`design-tokens.css`](./design-tokens.css). All templates below use the exact token variables, dimensions, borders, and typographic rules extracted from the workspace implementation ([`app.py`](./app.py), [`src/preview_renderer.py`](./src/preview_renderer.py), [`src/strategy_thumbnails.py`](./src/strategy_thumbnails.py), and [`pdf_exporter.py`](./pdf_exporter.py)).

---

## 1. Layout Rules & Spatial Architecture

### 1.1 Application Viewport & Container Rules
```css
/* Root Viewport & App Canvas */
body,
.app-canvas {
  background-color: var(--bg-app);          /* #f8fafc */
  color: var(--text-primary);               /* #0f172a */
  font-family: var(--font-sans);
  margin: 0;
  padding: 0;
  -webkit-font-smoothing: antialiased;
}

/* Primary Content Container */
.app-container {
  max-width: var(--layout-max-width);       /* 1400px */
  margin: 0 auto;
  padding-top: var(--layout-pad-top);       /* 1.0rem */
  padding-bottom: var(--layout-pad-bottom); /* 2.5rem */
  padding-left: 1.5rem;
  padding-right: 1.5rem;
  box-sizing: border-box;
}

/* Standard Structural Hairline Divider */
.section-divider {
  border: 0;
  border-top: 1px solid var(--border-subtle); /* #e2e8f0 */
  margin: var(--space-4) 0;                   /* 0.75rem 0 */
}
```

### 1.2 Grid Systems & Column Ratios
```css
/* 2-Column Hero Pathway Grid (50% / 50%) */
.grid-hero-2col {
  display: grid;
  grid-template-columns: repeat(2, minmax(0, 1fr));
  gap: 1.5rem;
  align-items: stretch;
}

/* 3-Column Contextual Metadata Banner Grid */
.grid-context-banner {
  display: grid;
  grid-template-columns: 1fr auto 2fr auto 1fr;
  align-items: center;
  gap: var(--space-6); /* 1.25rem */
}

/* 3-Column Strategy Selection Grid */
.grid-strategy-3col {
  display: grid;
  grid-template-columns: repeat(3, minmax(0, 1fr));
  gap: var(--space-4); /* 0.75rem */
  align-items: stretch;
}

/* 2-Column Split Studio Workspace (Controls Left / Live Preview Right) */
.grid-studio-workspace {
  display: grid;
  grid-template-columns: 5fr 7fr;
  gap: 1.5rem;
  align-items: start;
}

/* 4-Column Filter Bar */
.grid-filter-4col {
  display: grid;
  grid-template-columns: repeat(4, minmax(0, 1fr));
  gap: var(--space-5); /* 1.0rem */
  align-items: end;
}
```

### 1.3 Full-Card Overlay Hit-Target Pattern
Interactive cards use a relative wrapper containing a visual card element and an invisible full-surface `<button>` overlay (`z-index: 10`, `opacity: 0`). Secondary actions inside the card (such as a delete button) sit above the overlay at `z-index: 25`.

```css
.interactive-card-slot {
  position: relative;
}

.interactive-card-overlay-btn {
  position: absolute;
  inset: 0;
  width: 100%;
  height: 100%;
  opacity: 0;
  z-index: 10;
  cursor: pointer;
  border: none;
  background: transparent;
  padding: 0;
  margin: 0;
}

/* Hovering the invisible overlay triggers the sibling card's hover state */
.interactive-card-slot:hover .hero-card {
  transform: translateY(-4px) scale(1.015);
  box-shadow: var(--shadow-hero-hover);
}

.interactive-card-slot:hover .hero-blue {
  border-color: var(--accent-blue);
  border-top-color: var(--accent-blue-dark);
}

.interactive-card-slot:hover .hero-indigo {
  border-color: var(--accent-indigo);
  border-top-color: var(--accent-indigo-dark);
}
```

---

## 2. Canonical Component Templates

### 2.1 Passcode Authentication Gate Card

#### HTML Template
```html
<div class="auth-gate-card">
  <div class="auth-gate-badge">Workspace Access</div>
  <h1 class="auth-gate-title">Curriculum Design Studio</h1>
  <p class="auth-gate-subtitle">
    Enter the studio passcode to unlock curriculum generation, worksheet previews, and Google Docs export.
  </p>
  <form class="auth-gate-form">
    <label class="control-label" for="studio-passcode">Passcode</label>
    <input
      id="studio-passcode"
      type="password"
      class="input-control"
      placeholder="Enter passcode..."
    />
    <button type="submit" class="btn btn-primary" style="width: 100%; margin-top: 0.75rem;">
      Unlock Studio
    </button>
  </form>
</div>
```

#### CSS Rules
```css
.auth-gate-card {
  max-width: 520px;
  margin: 3.5rem auto 1.5rem auto;
  padding: 2.25rem;
  background: var(--bg-surface);            /* #ffffff */
  border: 1px solid var(--border-subtle);   /* #e2e8f0 */
  border-top: 5px solid var(--accent-navy); /* #1e3a8a */
  border-radius: var(--radius-xl);          /* 12px */
  box-shadow: var(--shadow-auth-card);      /* 0 4px 20px rgba(15, 23, 42, 0.08) */
}

.auth-gate-badge {
  display: inline-block;
  background: var(--status-info-bg);        /* #dbeafe */
  color: var(--accent-navy);                /* #1e3a8a */
  font-size: var(--text-xs);                /* 0.72rem */
  font-weight: var(--weight-extrabold);     /* 800 */
  text-transform: uppercase;
  letter-spacing: var(--tracking-wider);    /* 0.06em */
  padding: 0.2rem 0.6rem;
  border-radius: var(--radius-xs);          /* 4px */
  margin-bottom: 0.65rem;
}

.auth-gate-title {
  font-size: var(--text-3xl);               /* 1.55rem */
  font-weight: var(--weight-extrabold);     /* 800 */
  color: var(--text-primary);               /* #0f172a */
  margin: 0 0 0.4rem 0;
  letter-spacing: var(--tracking-tight);    /* -0.02em */
}

.auth-gate-subtitle {
  font-size: var(--text-md);                /* 0.88rem */
  color: var(--text-muted);                 /* #475569 */
  line-height: var(--leading-relaxed);      /* 1.45 */
  margin: 0 0 1.25rem 0;
}
```

---

### 2.2 3-Column Contextual Metadata Banner

#### HTML Template
```html
<div class="context-banner">
  <div class="context-banner-col-left">
    <div class="context-banner-label">Unit</div>
    <div class="context-banner-value">Seeds of Change</div>
  </div>

  <div class="context-banner-divider"></div>

  <div class="context-banner-col-center">
    <div class="context-banner-label">Essential Question</div>
    <div class="context-banner-quote">
      "How did colonial tensions and revolutionary ideals shape a new American nation?"
    </div>
  </div>

  <div class="context-banner-divider"></div>

  <div class="context-banner-col-right">
    <div class="context-banner-label">Google Drive Folder</div>
    <div>
      <span class="context-banner-code-pill">#US History (English) Curriculum</span>
    </div>
  </div>
</div>
```

#### JSX Template
```jsx
export function ContextMetadataBanner({ unitTitle, essentialQuestion, driveFolder }) {
  return (
    <div className="context-banner">
      <div className="context-banner-col-left">
        <div className="context-banner-label">Unit</div>
        <div className="context-banner-value">{unitTitle}</div>
      </div>

      <div className="context-banner-divider" />

      <div className="context-banner-col-center">
        <div className="context-banner-label">Essential Question</div>
        <div className="context-banner-quote">"{essentialQuestion}"</div>
      </div>

      <div className="context-banner-divider" />

      <div className="context-banner-col-right">
        <div className="context-banner-label">Google Drive Folder</div>
        <div>
          <span className="context-banner-code-pill">{driveFolder}</span>
        </div>
      </div>
    </div>
  );
}
```

#### CSS Rules
```css
.context-banner {
  background: var(--bg-app);                /* #f8fafc */
  border: 1px solid var(--border-subtle);   /* #e2e8f0 */
  border-left: 5px solid var(--accent-navy);/* #1e3a8a */
  border-radius: var(--radius-md);          /* 8px */
  padding: 0.85rem 1.15rem;
  margin-top: 0.25rem;
  margin-bottom: 1.0rem;
  display: grid;
  grid-template-columns: 1fr auto 2fr auto 1fr;
  align-items: center;
  gap: 1.25rem;
}

.context-banner-divider {
  width: 1.5px;
  height: 38px;
  background: var(--border-default);        /* #cbd5e1 */
}

.context-banner-label {
  font-size: 0.72rem;
  font-weight: 800;
  color: var(--text-subtle);                /* #64748b */
  text-transform: uppercase;
  letter-spacing: 0.06em;
  margin-bottom: 0.2rem;
}

.context-banner-value {
  font-size: 1.0rem;
  font-weight: 800;
  color: var(--text-primary);               /* #0f172a */
  line-height: 1.25;
}

.context-banner-col-center {
  text-align: center;
  padding: 0 0.5rem;
}

.context-banner-quote {
  font-size: 0.98rem;
  font-weight: 600;
  color: var(--text-secondary);             /* #1e293b */
  font-style: italic;
  line-height: 1.35;
}

.context-banner-col-right {
  text-align: right;
}

.context-banner-code-pill {
  font-family: var(--font-mono);
  font-size: 0.82rem;
  font-weight: 600;
  color: var(--text-secondary);             /* #1e293b */
  background: var(--bg-badge-neutral);      /* #e2e8f0 */
  padding: 0.2rem 0.55rem;
  border-radius: 5px;
  display: inline-block;
  white-space: nowrap;
}
```

---

### 2.3 Gateway Hero Header & Interactive Pathway Cards

#### HTML Template
```html
<header class="gateway-header">
  <h1 class="gateway-title">Curriculum Design Studio</h1>
  <div class="gateway-subtitle">Wait less. Teach better.</div>
  <div class="gateway-accent-bar"></div>
  <div class="gateway-helper">Select a design workflow below to get started</div>
</header>

<div class="grid-hero-2col">
  <!-- Pathway 1: Blue Variant -->
  <div class="interactive-card-slot">
    <div class="hero-card hero-blue">
      <div>
        <div class="hero-card-title">Browse Strategy Gallery</div>
        <div class="hero-card-desc">
          Explore research-backed instructional strategies, compare standard vs. scaffolded
          editions side-by-side, and export single-page activities directly to Google Docs or PDF.
        </div>
      </div>
      <div class="hero-card-cta">Explore Strategies &rarr;</div>
    </div>
    <button
      type="button"
      class="interactive-card-overlay-btn"
      aria-label="Browse Strategy Gallery"
    ></button>
  </div>

  <!-- Pathway 2: Indigo Variant -->
  <div class="interactive-card-slot">
    <div class="hero-card hero-indigo">
      <div>
        <div class="hero-card-title">Build a Custom Packet</div>
        <div class="hero-card-desc">
          Assemble multi-page unit packets or section booklets using the interactive horizontal
          page tray, mix strategies across sections, and export a unified print-ready booklet.
        </div>
      </div>
      <div class="hero-card-cta">Open Packet Builder &rarr;</div>
    </div>
    <button
      type="button"
      class="interactive-card-overlay-btn"
      aria-label="Build a Custom Packet"
    ></button>
  </div>
</div>
```

#### CSS Rules
```css
.gateway-header {
  text-align: center;
  padding: 1.5rem 0 2.0rem 0;
}

.gateway-title {
  font-size: 2.25rem;
  font-weight: 800;
  color: #0f172a;
  letter-spacing: -0.025em;
  margin: 0;
  line-height: 1.15;
}

.gateway-subtitle {
  font-size: 1.22rem;
  font-weight: 600;
  color: #2563eb;
  font-style: italic;
  margin-top: 0.45rem;
  letter-spacing: -0.01em;
}

.gateway-accent-bar {
  width: 44px;
  height: 3px;
  background: #93c5fd;
  border-radius: 2px;
  margin: 0.7rem auto 0.6rem auto;
}

.gateway-helper {
  font-size: 0.92rem;
  font-weight: 500;
  color: #64748b;
}

.hero-card {
  border-radius: 14px;
  padding: 2.2rem 2.0rem 2.0rem 2.0rem;
  border: 1.5px solid #e2e8f0;
  box-shadow: 0 4px 12px rgba(15, 23, 42, 0.05);
  min-height: 200px;
  display: flex;
  flex-direction: column;
  justify-content: space-between;
  transition: transform 0.22s cubic-bezier(0.34, 1.56, 0.64, 1),
              box-shadow 0.22s ease,
              border-color 0.22s ease;
  cursor: pointer;
  position: relative;
  overflow: hidden;
  background: #ffffff;
}

.hero-blue {
  border-top: 6px solid #2563eb;
  background: linear-gradient(180deg, #eff6ff 0%, #ffffff 48%);
}

.hero-indigo {
  border-top: 6px solid #6366f1;
  background: linear-gradient(180deg, #eef2ff 0%, #ffffff 48%);
}

.hero-card-title {
  font-size: 1.45rem;
  font-weight: 800;
  color: #0f172a;
  margin-bottom: 0.65rem;
  letter-spacing: -0.015em;
  line-height: 1.25;
}

.hero-card-desc {
  font-size: 0.96rem;
  color: #475569;
  line-height: 1.55;
  margin-bottom: 1.4rem;
}

.hero-card-cta {
  display: inline-flex;
  align-items: center;
  gap: 0.4rem;
  font-size: 0.92rem;
  font-weight: 800;
  padding-top: 0.75rem;
  border-top: 1px solid #f1f5f9;
}

.hero-blue .hero-card-title,
.hero-blue .hero-card-cta {
  color: #1d4ed8;
}

.hero-indigo .hero-card-title,
.hero-indigo .hero-card-cta {
  color: #4338ca;
}
```

---

### 2.4 Dynamic Horizontal Page Tray & Live Preview Tiles

The page tray renders a non-wrapping horizontal strip where each page slot has a locked width (`185px`) so tiles never compress, regardless of whether the packet contains 3 pages or 34 pages.

#### HTML Template
```html
<div class="tray-scroll-strip">
  <!-- Active Tray Tile (Standard Edition) -->
  <div class="tray-slot">
    <div class="tray-preview-card active">
      <div class="tray-card-top-bar">
        <span class="tray-page-badge">PAGE 1</span>
      </div>
      <div class="tray-sheet-mockup">
        <div class="tray-sheet-sec">Sec 1.1</div>
        <div class="tray-sheet-strat">Key Content Vocabulary</div>
        <div class="tray-sheet-lines">
          <div class="tray-line w-full"></div>
          <div class="tray-line w-3-4"></div>
          <div class="tray-line w-5-6"></div>
        </div>
      </div>
      <div class="tray-card-footer">
        <span class="badge-pill badge-gray">Standard</span>
        <div class="tray-hint-text">Click again to open full preview</div>
      </div>
    </div>
    <button type="button" class="interactive-card-overlay-btn" aria-label="Select Page 1"></button>
    <button type="button" class="tray-delete-btn" title="Remove Page 1">&times;</button>
  </div>

  <!-- Inactive Tray Tile (Scaffolded Edition) -->
  <div class="tray-slot">
    <div class="tray-preview-card">
      <div class="tray-card-top-bar">
        <span class="tray-page-badge">PAGE 2</span>
      </div>
      <div class="tray-sheet-mockup">
        <div class="tray-sheet-sec">Sec 1.1</div>
        <div class="tray-sheet-strat">Because, But, So</div>
        <div class="tray-sheet-lines">
          <div class="tray-line w-full"></div>
          <div class="tray-line w-3-4"></div>
          <div class="tray-line w-5-6"></div>
        </div>
      </div>
      <div class="tray-card-footer">
        <span class="badge-pill badge-scaf">Scaffolded</span>
        <div class="tray-hint-text">Click to edit page</div>
      </div>
    </div>
    <button type="button" class="interactive-card-overlay-btn" aria-label="Select Page 2"></button>
    <button type="button" class="tray-delete-btn" title="Remove Page 2">&times;</button>
  </div>

  <!-- Dashed Add Page Slot -->
  <div class="tray-slot">
    <div class="tray-add-card">
      <div style="font-size: 1.5rem; line-height: 1; margin-bottom: 0.35rem;">+</div>
      <div>Add New Page</div>
    </div>
    <button type="button" class="interactive-card-overlay-btn" aria-label="Add New Page"></button>
  </div>
</div>
```

#### CSS Rules
```css
.tray-scroll-strip {
  display: flex;
  flex-wrap: nowrap;
  overflow-x: auto;
  gap: 14px;
  padding: 0.6rem 0.4rem 1.1rem 0.4rem;
  align-items: stretch;
  scrollbar-width: thin;
  scrollbar-color: #94a3b8 #f1f5f9;
}

.tray-scroll-strip::-webkit-scrollbar {
  height: 10px;
}

.tray-scroll-strip::-webkit-scrollbar-track {
  background: #f1f5f9;
  border-radius: 6px;
}

.tray-scroll-strip::-webkit-scrollbar-thumb {
  background: #94a3b8;
  border-radius: 6px;
  border: 2px solid #f1f5f9;
}

.tray-scroll-strip::-webkit-scrollbar-thumb:hover {
  background: #64748b;
}

.tray-slot {
  position: relative;
  flex: 0 0 185px;
  width: 185px;
  min-width: 185px;
  max-width: 185px;
}

.tray-preview-card {
  border-radius: 12px;
  padding: 0.6rem 0.6rem 0.5rem 0.6rem;
  min-height: 220px;
  display: flex;
  flex-direction: column;
  justify-content: space-between;
  transition: all 0.16s ease;
  position: relative;
  box-sizing: border-box;
  background: #ffffff;
  border: 1.5px solid #cbd5e1;
  box-shadow: 0 1px 3px rgba(15, 23, 42, 0.05);
}

.tray-preview-card.active {
  border: 2.5px solid #1e3a8a;
  background: #f0f7ff;
  box-shadow: 0 4px 12px rgba(30, 58, 138, 0.12);
}

.tray-slot:hover .tray-preview-card {
  border-color: #2563eb;
  transform: translateY(-2px);
  box-shadow: 0 6px 14px rgba(37, 99, 235, 0.12);
}

.tray-card-top-bar {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 0.35rem;
  padding-right: 26px; /* Clears floating delete button */
}

.tray-page-badge {
  font-size: 0.68rem;
  font-weight: 800;
  color: #1e3a8a;
  background: #dbeafe;
  padding: 2px 7px;
  border-radius: 999px;
  letter-spacing: 0.03em;
}

.tray-sheet-mockup {
  background: #ffffff;
  border: 1px solid #e2e8f0;
  border-radius: 6px;
  padding: 0.5rem 0.55rem;
  height: 110px;
  display: flex;
  flex-direction: column;
  justify-content: space-between;
  box-shadow: inset 0 1px 2px rgba(15, 23, 42, 0.03);
  overflow: hidden;
  position: relative;
}

.tray-preview-card.active .tray-sheet-mockup {
  border-color: #bfdbfe;
  background: #ffffff;
}

.tray-sheet-sec {
  font-size: 0.65rem;
  font-weight: 800;
  color: #64748b;
  text-transform: uppercase;
  letter-spacing: 0.04em;
  border-bottom: 1.5px solid #0f172a;
  padding-bottom: 2px;
  margin-bottom: 4px;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.tray-sheet-strat {
  font-size: 0.78rem;
  font-weight: 800;
  color: #0f172a;
  line-height: 1.22;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
  margin-bottom: 4px;
}

.tray-sheet-lines {
  display: flex;
  flex-direction: column;
  gap: 4px;
  margin-top: auto;
  padding-top: 4px;
}

.tray-line {
  height: 3px;
  background: #e2e8f0;
  border-radius: 2px;
}

.tray-line.w-full { width: 100%; }
.tray-line.w-3-4  { width: 75%; }
.tray-line.w-5-6  { width: 85%; }

.tray-card-footer {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 3px;
  margin-top: 0.4rem;
}

.tray-hint-text {
  font-size: 0.64rem;
  font-weight: 700;
  color: #475569;
  text-align: center;
}

.tray-preview-card.active .tray-hint-text {
  color: #1e3a8a;
}

.tray-delete-btn {
  position: absolute;
  top: 8px;
  right: 10px;
  z-index: 25;
  width: 24px;
  height: 24px;
  border-radius: 999px;
  background: #f8fafc;
  border: 1px solid #cbd5e1;
  color: #64748b;
  font-size: 0.72rem;
  font-weight: 700;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  padding: 0;
  line-height: 1;
}

.tray-delete-btn:hover {
  background: #fee2e2;
  border-color: #ef4444;
  color: #b91c1c;
}

.tray-add-card {
  border-radius: 12px;
  padding: 0.75rem;
  min-height: 220px;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  border: 2px dashed #94a3b8;
  background: #f8fafc;
  color: #334155;
  font-weight: 700;
  font-size: 0.85rem;
  text-align: center;
  box-sizing: border-box;
  transition: all 0.16s ease;
}

.tray-slot:hover .tray-add-card {
  border-color: #1e3a8a;
  background: #eff6ff;
  color: #1e3a8a;
}
```

---

### 2.5 3-Column Visual Strategy Selection Grid & Miniature Wireframe Thumbnails

Each strategy tile displays a category badge, title, 3-line clamped description, and a `74px`-tall CSS wireframe diagram representing the layout of that instructional strategy.

#### HTML Template (Strategy Grid + 4 Canonical Wireframe Diagrams)
```html
<!-- Compact Active Selection Indicator Bar -->
<div class="active-strategy-bar">
  <span>Selected Strategy: <strong>Cornell Notes (2-Column)</strong></span>
  <span class="badge-pill badge-gray">Note-Taking &amp; Graphic Organizers</span>
</div>

<!-- 3-Column Strategy Card Grid -->
<div class="grid-strategy-3col">

  <!-- Tile 1: Active Strategy with 2-Column Cornell Notes Wireframe -->
  <div class="interactive-card-slot">
    <div class="strategy-tile-card active">
      <div>
        <div class="strategy-tile-badge">Note-Taking</div>
        <div class="strategy-tile-title">Cornell Notes</div>
        <div class="strategy-tile-desc">
          Two-column note-taking layout pairing left-hand cue questions with right-hand section notes and a bottom summary box.
        </div>
      </div>
      <!-- Wireframe: Cornell 2-Column + Bottom Summary -->
      <div class="wireframe-box" style="display: flex; flex-direction: column; justify-content: space-between;">
        <div style="display: grid; grid-template-columns: 1fr 2fr; gap: 4px; height: 44px;">
          <div style="background: #ffffff; border: 1px solid #94a3b8; border-radius: 2px; padding: 3px;">
            <div style="font-size: 6.5px; font-weight: 800; color: #1e3a8a;">CUES</div>
            <div class="wf-line-dotted"></div>
            <div class="wf-line-dotted"></div>
          </div>
          <div style="background: #ffffff; border: 1px solid #94a3b8; border-radius: 2px; padding: 3px;">
            <div style="font-size: 6.5px; font-weight: 800; color: #334155;">NOTES</div>
            <div class="wf-line-dotted"></div>
            <div class="wf-line-dotted"></div>
          </div>
        </div>
        <div style="background: #ffffff; border: 1px solid #64748b; border-radius: 2px; padding: 2px 4px; height: 14px;">
          <div style="font-size: 6px; font-weight: 800; color: #475569;">SUMMARY</div>
        </div>
      </div>
    </div>
    <button type="button" class="interactive-card-overlay-btn" aria-label="Select Cornell Notes"></button>
  </div>

  <!-- Tile 2: Inactive Strategy with Because, But, So 3-Row Wireframe -->
  <div class="interactive-card-slot">
    <div class="strategy-tile-card">
      <div>
        <div class="strategy-tile-badge">Sentence-Level Writing</div>
        <div class="strategy-tile-title">Because, But, So</div>
        <div class="strategy-tile-desc">
          Sentence expansion routine prompting students to explain cause (because), contrast (but), and effect (so) from a shared stem.
        </div>
      </div>
      <!-- Wireframe: Because / But / So Stems -->
      <div class="wireframe-box" style="display: flex; flex-direction: column; justify-content: space-around;">
        <div class="wf-stem-row">
          <span class="wf-Tag wf-tag-blue">...because</span>
          <span class="wf-line-solid"></span>
        </div>
        <div class="wf-stem-row">
          <span class="wf-Tag wf-tag-amber">...but</span>
          <span class="wf-line-solid"></span>
        </div>
        <div class="wf-stem-row">
          <span class="wf-Tag wf-tag-green">...so</span>
          <span class="wf-line-solid"></span>
        </div>
      </div>
    </div>
    <button type="button" class="interactive-card-overlay-btn" aria-label="Select Because, But, So"></button>
  </div>

  <!-- Tile 3: Inactive Strategy with 4-Box Grid / Frayer Wireframe -->
  <div class="interactive-card-slot">
    <div class="strategy-tile-card">
      <div>
        <div class="strategy-tile-badge">Vocabulary</div>
        <div class="strategy-tile-title">Frayer Model (4-Quad)</div>
        <div class="strategy-tile-desc">
          Four-quadrant graphic organizer analyzing target vocabulary through definition, historical context, examples, and non-examples.
        </div>
      </div>
      <!-- Wireframe: 2x2 Quadrant Grid with Center Pill -->
      <div class="wireframe-box" style="position: relative; display: grid; grid-template-columns: 1fr 1fr; grid-template-rows: 1fr 1fr; gap: 3px;">
        <div class="wf-quad">DEF</div>
        <div class="wf-quad">CHAR</div>
        <div class="wf-quad">EX</div>
        <div class="wf-quad">NON-EX</div>
        <div style="position: absolute; top: 50%; left: 50%; transform: translate(-50%, -50%); background: #1e3a8a; color: #ffffff; font-size: 6px; font-weight: 800; padding: 1px 5px; border-radius: 8px;">
          TERM
        </div>
      </div>
    </div>
    <button type="button" class="interactive-card-overlay-btn" aria-label="Select Frayer Model"></button>
  </div>

</div>
```

#### CSS Rules
```css
.active-strategy-bar {
  display: flex;
  align-items: center;
  justify-content: space-between;
  background: #f0fdf4;
  border: 1.5px solid #86efac;
  border-radius: 8px;
  padding: 0 0.9rem;
  height: 38px;
  margin-bottom: 0.75rem;
  color: #166534;
  font-size: 0.85rem;
  font-weight: 600;
}

.strategy-tile-card {
  border-radius: 10px;
  padding: 0.75rem;
  min-height: 255px;
  display: flex;
  flex-direction: column;
  justify-content: space-between;
  transition: all 0.15s ease;
  box-sizing: border-box;
  background: #ffffff;
  border: 1.5px solid #cbd5e1;
  box-shadow: 0 1px 2px rgba(15, 23, 42, 0.04);
}

.strategy-tile-card.active {
  border: 2.5px solid #1e3a8a;
  background: #eff6ff;
  box-shadow: 0 3px 10px rgba(30, 58, 138, 0.12);
}

.interactive-card-slot:hover .strategy-tile-card {
  border-color: #2563eb;
  box-shadow: 0 4px 12px rgba(37, 99, 235, 0.10);
}

.strategy-tile-badge {
  display: inline-block;
  font-size: 0.66rem;
  font-weight: 800;
  text-transform: uppercase;
  letter-spacing: 0.04em;
  color: #475569;
  background: #f1f5f9;
  padding: 2px 6px;
  border-radius: 4px;
  margin-bottom: 0.35rem;
}

.strategy-tile-card.active .strategy-tile-badge {
  background: #dbeafe;
  color: #1e3a8a;
}

.strategy-tile-title {
  font-size: 0.88rem;
  font-weight: 800;
  color: #0f172a;
  margin-bottom: 0.25rem;
  line-height: 1.25;
}

.strategy-tile-desc {
  font-size: 0.75rem;
  color: #475569;
  line-height: 1.35;
  display: -webkit-box;
  -webkit-line-clamp: 3;
  -webkit-box-orient: vertical;
  overflow: hidden;
  margin-bottom: 0.45rem;
}

/* Miniature Wireframe Thumbnail Primitives */
.wireframe-box {
  height: 74px;
  background: #f8fafc;
  border: 1px solid #cbd5e1;
  border-radius: 4px;
  padding: 5px 6px;
  box-sizing: border-box;
  overflow: hidden;
}

.wf-line-dotted {
  border-bottom: 1px dotted #94a3b8;
  height: 7px;
  width: 100%;
}

.wf-line-solid {
  border-bottom: 1px solid #64748b;
  flex: 1;
  height: 8px;
}

.wf-stem-row {
  display: flex;
  align-items: center;
  gap: 4px;
}

.wf-Tag {
  font-size: 7px;
  font-weight: 800;
  padding: 1px 4px;
  border-radius: 2px;
  white-space: nowrap;
}

.wf-tag-blue  { background: #dbeafe; color: #1e3a8a; }
.wf-tag-amber { background: #fef3c7; color: #92400e; }
.wf-tag-green { background: #dcfce7; color: #166534; }

.wf-quad {
  background: #ffffff;
  border: 1px solid #94a3b8;
  border-radius: 2px;
  padding: 2px 4px;
  font-size: 6.5px;
  font-weight: 800;
  color: #475569;
}
```

---

### 2.6 Horizontal Page Inspector Carousel

#### HTML Template
```html
<div class="inspector-carousel-row">
  <button type="button" class="inspector-arrow-btn" aria-label="Previous Page">&larr;</button>

  <div class="inspector-tiles-strip">
    <div class="interactive-card-slot" style="flex: 1;">
      <div class="inspector-tile active">
        <div class="inspector-tile-num">PAGE 1 &bull; SEC 1.1</div>
        <div class="inspector-tile-title">Key Content Vocabulary</div>
        <span class="badge-pill badge-gray">Standard</span>
      </div>
      <button type="button" class="interactive-card-overlay-btn" aria-label="Inspect Page 1"></button>
    </div>

    <div class="interactive-card-slot" style="flex: 1;">
      <div class="inspector-tile">
        <div class="inspector-tile-num">PAGE 2 &bull; SEC 1.1</div>
        <div class="inspector-tile-title">Because, But, So</div>
        <span class="badge-pill badge-scaf">Scaffolded</span>
      </div>
      <button type="button" class="interactive-card-overlay-btn" aria-label="Inspect Page 2"></button>
    </div>
  </div>

  <button type="button" class="inspector-arrow-btn" aria-label="Next Page">&rarr;</button>
</div>
```

#### CSS Rules
```css
.inspector-carousel-row {
  display: flex;
  align-items: stretch;
  gap: 0.5rem;
  margin-bottom: 0.85rem;
}

.inspector-tiles-strip {
  display: flex;
  flex: 1;
  gap: 0.5rem;
}

.inspector-tile {
  border-radius: 8px;
  padding: 0.45rem 0.5rem;
  height: 75px;
  display: flex;
  flex-direction: column;
  justify-content: space-between;
  align-items: center;
  text-align: center;
  transition: all 0.15s ease;
  box-sizing: border-box;
  background: #ffffff;
  border: 1.5px solid #cbd5e1;
}

.inspector-tile.active {
  border: 2px solid #1e3a8a;
  background: #eff6ff;
  box-shadow: 0 2px 6px rgba(30, 58, 138, 0.10);
}

.inspector-tile-num {
  font-size: 0.66rem;
  font-weight: 800;
  color: #64748b;
  letter-spacing: 0.04em;
}

.inspector-tile.active .inspector-tile-num {
  color: #1e3a8a;
}

.inspector-tile-title {
  font-size: 0.78rem;
  font-weight: 700;
  color: #0f172a;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
  max-width: 100%;
}

.inspector-arrow-btn {
  width: 44px;
  height: 75px;
  border-radius: 8px;
  border: 1.5px solid #cbd5e1;
  background: #ffffff;
  color: #1e293b;
  font-size: 1.1rem;
  font-weight: 800;
  cursor: pointer;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  transition: all 0.15s ease;
}

.inspector-arrow-btn:hover:not(:disabled) {
  background: #eff6ff;
  border-color: #2563eb;
  color: #1d4ed8;
}

.inspector-arrow-btn:disabled {
  opacity: 0.45;
  cursor: not-allowed;
}
```

---

### 2.7 Badges, Status Pills & Edition Indicators

Scaffolded editions do not render a separate rectangular edition badge on student worksheets; instead, the section/page header badge switches from `.ws-badge-blue` (`#dbeafe` / `#1e3a8a`) to `.ws-badge-amber` (`#fef3c7` / `#b45309`).

#### HTML Template
```html
<!-- Application UI Pill Badges -->
<span class="badge-pill badge-gray">Standard</span>
<span class="badge-pill badge-scaf">Scaffolded</span>

<!-- Worksheet Top-Left Section Badges -->
<span class="ws-title-badge ws-badge-blue">Section 1.1: Early Colonial Tensions (pp. 4-9)</span>
<span class="ws-title-badge ws-badge-amber">Section 1.1: Early Colonial Tensions (pp. 4-9)</span>
```

#### CSS Rules
```css
.badge-pill {
  font-size: 0.65rem;
  font-weight: 700;
  padding: 2px 7px;
  border-radius: 999px;
  display: inline-block;
  line-height: 1.3;
}

.badge-scaf {
  background: #fef3c7;
  color: #92400e;
  border: 1px solid #fde68a;
}

.badge-gray {
  background: #f1f5f9;
  color: #475569;
  border: 1px solid #cbd5e1;
}

.ws-title-badge {
  display: inline-block;
  font-size: 0.72rem;
  font-weight: 800;
  text-transform: uppercase;
  letter-spacing: 0.05em;
  padding: 0.18rem 0.55rem;
  border-radius: 4px;
  margin-bottom: 0.35rem;
}

.ws-badge-blue {
  background: #dbeafe;
  color: #1e3a8a;
}

.ws-badge-amber {
  background: #fef3c7;
  color: #b45309;
  border: 1px solid #fcd34d;
}
```

---

### 2.8 Action Buttons & Form Controls

#### HTML Template
```html
<div style="display: flex; gap: 0.75rem; align-items: center; flex-wrap: wrap;">
  <!-- Primary CTA -->
  <button type="button" class="btn btn-primary">
    Generate &amp; Download PDF Booklet
  </button>

  <!-- Secondary Outline CTA -->
  <button type="button" class="btn btn-secondary">
    Reset Packet Tray
  </button>

  <!-- Google Drive Export Action -->
  <a href="#export-drive" class="btn btn-drive">
    Open Editable Copy in Google Docs
  </a>
</div>

<!-- Form Select Control -->
<div style="max-width: 320px; margin-top: 1rem;">
  <label class="control-label" for="section-select">Target Textbook Section</label>
  <select id="section-select" class="select-control">
    <option value="1.1">Section 1.1: Limits on Freedom</option>
    <option value="1.2">Section 1.2: Colonial Resistance</option>
  </select>
</div>
```

#### CSS Rules
```css
.btn {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  gap: 0.45rem;
  font-family: var(--font-sans);
  font-size: 0.92rem;
  font-weight: 700;
  border-radius: 6px;
  padding: 0.55rem 1.1rem;
  cursor: pointer;
  transition: all 0.15s ease;
  text-decoration: none;
  box-sizing: border-box;
}

.btn-primary {
  background-color: #1e3a8a;
  color: #ffffff;
  border: 2px solid #172554;
  box-shadow: 0 2px 4px rgba(15, 23, 42, 0.12);
}

.btn-primary:hover {
  background-color: #172554;
  border-color: #0f172a;
  color: #ffffff;
  box-shadow: 0 4px 8px rgba(15, 23, 42, 0.18);
}

.btn-secondary {
  background-color: #f8fafc;
  color: #1e3a8a;
  border: 2px solid #1e3a8a;
  font-weight: 600;
  box-shadow: 0 1px 3px rgba(15, 23, 42, 0.06);
}

.btn-secondary:hover {
  background-color: #1e3a8a;
  color: #ffffff;
  border-color: #172554;
  box-shadow: 0 3px 6px rgba(30, 58, 138, 0.18);
}

.btn-drive {
  background-color: #1e40af;
  color: #ffffff;
  border: 1.5px solid #1d4ed8;
  border-radius: 8px;
  font-size: 0.85rem;
  padding: 0.5rem 1.0rem;
}

.btn-drive:hover {
  background-color: #1e3a8a;
  border-color: #172554;
}

.control-label {
  display: block;
  font-size: 0.78rem;
  font-weight: 700;
  color: #334155;
  margin-bottom: 0.3rem;
}

.input-control,
.select-control {
  width: 100%;
  font-family: var(--font-sans);
  font-size: 0.88rem;
  color: #0f172a;
  background-color: #ffffff;
  border: 1.5px solid #94a3b8;
  border-radius: 6px;
  padding: 0.48rem 0.75rem;
  box-shadow: 0 1px 2px rgba(15, 23, 42, 0.04);
  box-sizing: border-box;
  transition: border-color 0.15s ease, box-shadow 0.15s ease;
}

.input-control:hover,
.select-control:hover {
  border-color: #1e3a8a;
}

.input-control:focus,
.select-control:focus {
  outline: none;
  border-color: #1e3a8a;
  box-shadow: 0 0 0 2px rgba(30, 58, 138, 0.20);
}
```

---

### 2.9 Student Worksheet & Teacher Exemplar Components

#### HTML Template (Student Handout + Teacher Answer Key)
```html
<!-- 1. STUDENT HANDOUT SHEET (Scaffolded Edition uses .ws-badge-amber) -->
<article class="ws-container">
  <header class="ws-header">
    <div>
      <div class="ws-title-badge ws-badge-amber">
        Section 1.1: Limits on Freedom (pp. 4-8)
      </div>
      <h2 class="ws-title">Because, But, So (Cause, Contrast, Effect)</h2>
    </div>
    <div class="ws-student-meta">
      <div>Name: <span class="ws-meta-line"></span></div>
      <div>Date: <span class="ws-meta-line" style="min-width: 75px;"></span> Per: <span class="ws-meta-line" style="min-width: 40px;"></span></div>
    </div>
  </header>

  <div class="ws-strategy-focus">
    <div class="ws-strategy-focus-label">Strategy Focus: Because, But, So (Cause, Contrast, Effect)</div>
    <div class="ws-strategy-focus-body">
      Complete each sentence stem below using historical evidence from the textbook passage:
      <strong>because</strong> explains why something happened, <strong>but</strong> shows a contrasting perspective or obstacle, and <strong>so</strong> states the historical result.
    </div>
  </div>

  <!-- Optional Word Bank Callout (Included on Scaffolded Edition) -->
  <div class="ws-callout">
    <div class="ws-callout-title">Word Bank &amp; Key Historical Terms</div>
    <div style="font-size: 0.86rem; color: #1e293b;">
      Proclamation of 1763 &bull; Appalachian Mountains &bull; Parliament &bull; War Debt &bull; Colonists
    </div>
  </div>

  <div class="ws-section-title">Part 1: Sentence Expansion</div>

  <div class="ws-question-row">
    <div style="font-weight: 600;">1. Tensions grew between Britain and the colonies because...</div>
    <div class="ws-dotted-line"></div>
    <div class="ws-dotted-line"></div>
  </div>

  <div class="ws-question-row">
    <div style="font-weight: 600;">2. Tensions grew between Britain and the colonies, but...</div>
    <div class="ws-dotted-line"></div>
    <div class="ws-dotted-line"></div>
  </div>

  <div class="ws-question-row">
    <div style="font-weight: 600;">3. Tensions grew between Britain and the colonies, so...</div>
    <div class="ws-dotted-line"></div>
    <div class="ws-dotted-line"></div>
  </div>
</article>

<!-- 2. TEACHER EXEMPLAR / ANSWER KEY SHEET -->
<article class="ws-exemplar-container" style="margin-top: 1.5rem;">
  <header class="ws-header">
    <div>
      <div class="ws-title-badge ws-badge-blue">Teacher Exemplar &bull; Section 1.1</div>
      <h2 class="ws-title">Because, But, So (Cause, Contrast, Effect)</h2>
    </div>
    <div class="ws-grade-box">10 / 10</div>
  </header>

  <div class="ws-question-row">
    <div style="font-weight: 600;">1. Tensions grew between Britain and the colonies because...</div>
    <div class="ws-student-answer">
      Tensions grew between Britain and the colonies because King George III issued the Proclamation of 1763, which forbade colonists from settling west of the Appalachian Mountains after the French and Indian War.
    </div>
  </div>
</article>
```

#### CSS Rules
```css
.ws-container {
  background: #ffffff;
  border: 1px solid #cbd5e1;
  border-radius: 6px;
  padding: 2.0rem 2.25rem;
  box-shadow: 0 4px 12px rgba(15, 23, 42, 0.06);
  font-family: var(--font-sans);
  color: #0f172a;
  max-width: 850px;
  margin: 0 auto 1.25rem auto;
  line-height: 1.45;
  box-sizing: border-box;
}

.ws-exemplar-container {
  background: #fffbeb;
  border: 2px solid #cbd5e1;
  border-radius: 6px;
  padding: 2.0rem 2.25rem;
  box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1),
              0 4px 6px -2px rgba(0, 0, 0, 0.05);
  font-family: var(--font-sans);
  color: #0f172a;
  max-width: 850px;
  margin: 0 auto 1.25rem auto;
  line-height: 1.45;
  box-sizing: border-box;
}

.ws-header {
  border-bottom: 2.5px solid #0f172a;
  padding-bottom: 0.65rem;
  margin-bottom: 1.1rem;
  display: flex;
  justify-content: space-between;
  align-items: flex-end;
  gap: 1rem;
}

.ws-title {
  font-size: 1.35rem;
  font-weight: 800;
  color: #0f172a;
  margin: 0;
  line-height: 1.2;
}

.ws-student-meta {
  font-size: 0.82rem;
  color: #334155;
  text-align: right;
  white-space: nowrap;
  line-height: 1.65;
}

.ws-meta-line {
  display: inline-block;
  border-bottom: 1px solid #475569;
  min-width: 120px;
  margin-left: 4px;
}

.ws-strategy-focus {
  background: #f0f9ff;
  border: 1px solid #bae6fd;
  border-left: 4px solid #0284c7;
  border-radius: 4px;
  padding: 0.6rem 0.85rem;
  margin-bottom: 0.9rem;
}

.ws-strategy-focus-label {
  font-size: 0.72rem;
  font-weight: 800;
  text-transform: uppercase;
  letter-spacing: 0.05em;
  color: #0369a1;
  margin-bottom: 0.15rem;
}

.ws-strategy-focus-body {
  font-size: 0.84rem;
  color: #0c4a6e;
  line-height: 1.4;
}

.ws-callout {
  background: #f8fafc;
  border: 1px solid #cbd5e1;
  border-left: 4px solid #1e3a8a;
  border-radius: 4px;
  padding: 0.65rem 0.85rem;
  margin-bottom: 1.0rem;
}

.ws-callout-title {
  font-size: 0.76rem;
  font-weight: 800;
  text-transform: uppercase;
  letter-spacing: 0.04em;
  color: #1e3a8a;
  margin-bottom: 0.25rem;
}

.ws-section-title {
  font-size: 0.92rem;
  font-weight: 800;
  text-transform: uppercase;
  letter-spacing: 0.04em;
  color: #0f172a;
  background: #f1f5f9;
  border-left: 4px solid #1e3a8a;
  padding: 0.35rem 0.65rem;
  margin: 1.0rem 0 0.65rem 0;
}

.ws-question-row {
  margin-bottom: 0.85rem;
  font-size: 0.9rem;
  color: #0f172a;
}

.ws-dotted-line {
  border-bottom: 1.5px dotted #64748b;
  height: 1.55rem;
  width: 100%;
  margin-top: 0.15rem;
}

.ws-solid-line {
  border-bottom: 1px solid #475569;
  height: 1.55rem;
  width: 100%;
  margin-top: 0.15rem;
}

.ws-table {
  width: 100%;
  border-collapse: collapse;
  margin: 0.65rem 0 1.0rem 0;
  font-size: 0.86rem;
}

.ws-table th {
  background: #f1f5f9;
  color: #0f172a;
  font-weight: 800;
  text-align: left;
  padding: 0.5rem 0.65rem;
  border: 1px solid #64748b;
  font-size: 0.8rem;
  text-transform: uppercase;
  letter-spacing: 0.03em;
}

.ws-table td {
  padding: 0.55rem 0.65rem;
  border: 1px solid #64748b;
  vertical-align: top;
  color: #1e293b;
}

.ws-grade-box {
  display: inline-block;
  border: 2px solid #dc2626;
  color: #dc2626;
  font-weight: 900;
  font-size: 1.05rem;
  padding: 0.15rem 0.55rem;
  border-radius: 6px;
  transform: rotate(-3deg);
  background: rgba(254, 242, 242, 0.85);
}

.ws-student-answer {
  font-family: var(--font-handwriting);
  color: #1d4ed8;
  font-weight: 600;
  font-size: 0.92rem;
  line-height: 1.45;
  background: rgba(239, 246, 255, 0.55);
  border-left: 3px solid #2563eb;
  padding: 0.35rem 0.6rem;
  margin-top: 0.25rem;
  border-radius: 0 4px 4px 0;
}
```

---

### 2.10 Print & 2-Up Half-Sheet Geometry (`@page` Letter Specification)

Used by [`pdf_exporter.py`](./pdf_exporter.py) (Playwright Chromium headless PDF generator) to fit either a full-page handout or two identical half-sheet Exit Tickets onto a single 8.5" x 11" sheet with a centered cut line.

#### HTML Template
```html
<div class="half-sheet-page-wrapper">
  <div class="half-sheet-item">
    <!-- Top Half-Sheet Content -->
  </div>

  <div class="half-sheet-cut-divider">
    <span>&#9986; Cut Here &#9986;</span>
  </div>

  <div class="half-sheet-item">
    <!-- Bottom Half-Sheet Content -->
  </div>
</div>
```

#### CSS Rules
```css
@page {
  size: letter portrait;
  margin: 0.4in 0.45in;
}

.half-sheet-page-wrapper {
  height: 10.10in;
  max-height: 10.10in;
  display: flex;
  flex-direction: column;
  justify-content: space-between;
  box-sizing: border-box;
  page-break-after: always;
  break-after: page;
}

.half-sheet-item {
  height: 4.88in;
  max-height: 4.88in;
  overflow: hidden;
  box-sizing: border-box;
}

.half-sheet-cut-divider {
  height: 0.22in;
  display: flex;
  align-items: center;
  justify-content: center;
  border-top: 1.5px dashed #64748b;
  color: #475569;
  font-size: 8pt;
  font-weight: 700;
  letter-spacing: 0.08em;
  text-transform: uppercase;
}
```

---

## 3. Tailwind CSS Theme Extension (`tailwind.config.js`)

For React, Next.js, or Vite projects using Tailwind CSS, drop the following extension into `tailwind.config.js` alongside [`design-tokens.css`](./design-tokens.css):

```js
// tailwind.config.js
module.exports = {
  theme: {
    extend: {
      colors: {
        studio: {
          bg: "#f8fafc",
          surface: "#ffffff",
          muted: "#f1f5f9",
          exemplar: "#fffbeb",
          navy: {
            DEFAULT: "#1e3a8a",
            dark: "#172554",
            deep: "#0f172a",
          },
          blue: {
            DEFAULT: "#2563eb",
            dark: "#1d4ed8",
            drive: "#1e40af",
            tint: "#eff6ff",
            active: "#f0f7ff",
            badge: "#dbeafe",
          },
          indigo: {
            DEFAULT: "#6366f1",
            dark: "#4338ca",
            tint: "#eef2ff",
          },
          sky: {
            DEFAULT: "#0284c7",
            dark: "#0369a1",
            deep: "#0c4a6e",
            tint: "#f0f9ff",
            border: "#bae6fd",
          },
          scaf: {
            bg: "#fef3c7",
            border: "#fde68a",
            accent: "#fcd34d",
            text: "#92400e",
            badgeText: "#b45309",
          },
        },
      },
      fontFamily: {
        sans: [
          "Inter",
          "Segoe UI",
          "Roboto",
          "-apple-system",
          "BlinkMacSystemFont",
          "sans-serif",
        ],
        mono: ["ui-monospace", "SFMono-Regular", "Menlo", "Consolas", "monospace"],
        handwriting: ["Comic Sans MS", "Bradley Hand", "Chalkboard SE", "cursive", "sans-serif"],
      },
      boxShadow: {
        "studio-xs": "0 1px 2px rgba(15, 23, 42, 0.04)",
        "studio-sm": "0 1px 3px rgba(15, 23, 42, 0.05)",
        "studio-card": "0 4px 12px rgba(15, 23, 42, 0.05)",
        "studio-auth": "0 4px 20px rgba(15, 23, 42, 0.08)",
        "studio-active": "0 4px 12px rgba(30, 58, 138, 0.12)",
        "studio-hero-hover": "0 14px 28px rgba(37, 99, 235, 0.14)",
      },
      borderRadius: {
        "studio-xs": "4px",
        "studio-sm": "6px",
        "studio-md": "8px",
        "studio-lg": "10px",
        "studio-xl": "12px",
        "studio-2xl": "14px",
      },
      maxWidth: {
        studio: "1400px",
        worksheet: "850px",
      },
    },
  },
};
```
