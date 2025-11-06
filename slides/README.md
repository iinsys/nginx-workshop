# Presentation Slides

This directory contains the presentation slides for the nginx workshop.

## How to Present

### Option 1: Using Marp (Recommended)

**Install Marp CLI:**
```bash
npm install -g @marp-team/marp-cli
```

**Convert to HTML:**
```bash
marp PRESENTATION.md -o presentation.html
```

**Or use Marp for VS Code:**
1. Install "Marp for VS Code" extension
2. Open `PRESENTATION.md`
3. Click "Open Preview" (or press `Ctrl+Shift+V`)

**Or use Marp Web:**
1. Go to https://web.marp.app/
2. Copy and paste the content of `PRESENTATION.md`
3. Present directly from browser

### Option 2: Using Reveal.js

**Install reveal.js:**
```bash
npm install -g reveal-md
```

**Present:**
```bash
reveal-md PRESENTATION.md
```

### Option 3: Export to PDF

**Using Marp:**
```bash
marp PRESENTATION.md --pdf
```

**Using Marp for VS Code:**
1. Open `PRESENTATION.md`
2. Click "Export Slide Deck"
3. Choose PDF format

### Option 4: Online Tools

1. **Marp Web:** https://web.marp.app/
   - Copy content from `PRESENTATION.md`
   - Present directly in browser
   - Export to PDF/PPTX

2. **Slide.com:** https://slides.com/
   - Import markdown
   - Create beautiful slides

## File Structure

```
slides/
├── PRESENTATION.md    # Main slide deck (Marp format)
└── README.md          # This file
```

## Presentation Tips

1. **Use Presenter Mode:**
   - Marp supports presenter notes
   - Use `<!-- Note: Your notes here -->` for speaker notes

2. **Keyboard Shortcuts:**
   - `→` / `←`: Navigate slides
   - `F`: Fullscreen
   - `Esc`: Overview mode

3. **Print Handouts:**
   - Export to PDF with multiple slides per page
   - Use: `marp PRESENTATION.md --pdf --allow-local-files`

4. **Customize Theme:**
   - Edit the `style:` section in `PRESENTATION.md`
   - Change colors, fonts, sizes

## Quick Start

**Easiest Method (No Installation):**

1. Go to https://web.marp.app/
2. Open `PRESENTATION.md` in your editor
3. Copy all content
4. Paste into Marp Web
5. Present from browser!

**For VS Code Users:**

1. Install "Marp for VS Code" extension
2. Open `PRESENTATION.md`
3. Press `Ctrl+Shift+V` to preview
4. Present in fullscreen mode

## Customization

To customize the presentation:

1. **Change Theme:**
   ```yaml
   theme: default  # Options: default, gaia, uncover
   ```

2. **Change Colors:**
   Edit the `style:` section:
   ```css
   h1 { color: #your-color; }
   ```

3. **Add Your Logo:**
   ```yaml
   header: '![logo](logo.png) nginx Workshop'
   ```

## Troubleshooting

**Marp not rendering?**
- Make sure you have the frontmatter (---) at the top
- Check for syntax errors

**Images not showing?**
- Use absolute paths or relative to markdown file
- For web.marp.app, images need to be hosted online

**Export not working?**
- Make sure Marp CLI is installed: `npm install -g @marp-team/marp-cli`
- Try: `marp --version` to verify installation

