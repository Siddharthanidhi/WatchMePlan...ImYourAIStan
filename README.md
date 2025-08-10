# 🗂️ AI Task / Event Planner 🗺️
This is a small Streamlit app that uses Google Gemini (flash model) to autonomously infer a user’s planning request, ask only necessary clarifying questions, and produce a clear, emoji-rich step-by-step plan. 
Includes a “Download as PDF” button.
---

## Key features:
- Auto-detects planning type (trip✈️, event🥂, study plan📒, etc.)
- Asks clarifying questions before generating a plan
- Human-readable, emoji-enhanced plans (no raw JSON shown to users)
- PDF export with clean margins and line wrapping
---

## Usage:
- Type a task (e.g., “Plan a 3-day trip to Kathmandu 🗺️ for 2 people 🍕 under 💵 25000 NPR”).
- If needed, answer clarifying questions the agent asks.
- View the final plan and click 📥 Download Plan as PDF.
---

## Notes:
- Uses a Gemini flash model (e.g., gemini-2.5-flash) — use the exact model your API key supports.
- ReportLab is used for PDF generation (Unicode/font support). Place DejaVuSans.ttf in the project if you need emoji/unicode preserved in PDFs.

## Future Work:
- To integrate this with Google Notes and Google Calendar to set automatic reminders
- Improved UI and hosting platform
