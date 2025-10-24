1) Claude → produce ready-to-drop code/JSON per spec.
2) ChatGPT → integrate into workflows/phase0+1.json and update docs/airtable_schema.json.
3) Atlas → run fix_codex_config.sh, then implement_workflow.sh.
4) Atlas → n8n UI: import/replace workflow, Run once, download execution log to .logs/.
5) Atlas → Airtable: confirm writes by field IDs, not names.
6) Atlas → commit changes and logs.
