# VS Code MCP Integration Anleitung

## Der Server läuft bereits! 🎉

Du hast den MCP Server erfolgreich gestartet. Er läuft im Hintergrund und wartet auf Client-Verbindungen.

## Nutzung in VS Code

### Option 1: GitHub Copilot mit MCP (Empfohlen)

1. **VS Code Command Palette** öffnen (`Ctrl+Shift+P` / `Cmd+Shift+P`)
2. Suche nach **"GitHub Copilot: Chat"**
3. Der MCP Server wird automatisch erkannt und eingebunden
4. Stelle Fragen wie:
   - "List all Sentinel workspaces"
   - "Show me analytics rules from workspace X"
   - "Export all workbooks"

### Option 2: MCP Extension installieren

Wenn du eine dedizierte MCP Extension nutzen möchtest:

```powershell
# Installation über Extensions
code --install-extension <mcp-extension-id>
```

### Option 3: Claude Desktop Integration

Füge die Server-Konfiguration zu Claude Desktop hinzu:

**Windows**: `%APPDATA%\Claude\claude_desktop_config.json`

```json
{
  "mcpServers": {
    "sentinel-mcp-server": {
      "command": "python",
      "args": [
        "C:\\Users\\PhillipeChaves\\projects\\sentinel-mcp-server\\src\\__main__.py"
      ],
      "env": {
        "AZURE_TENANT_ID": "your-tenant-id",
        "AZURE_SUBSCRIPTION_ID": "your-subscription-id"
      }
    }
  }
}
```

Nach Neustart von Claude Desktop kannst du Sentinel-Befehle nutzen:
- "List my Sentinel workspaces"
- "Create a new analytics rule"
- "Export all workbooks from workspace X"

## Tools die verfügbar sind (39 PowerShell Funktionen)

### Table Management
- `New-SentinelTable` - Erstelle neue Tables
- `Get-SentinelTables` - Liste alle Tables
- `Remove-SentinelTable` - Lösche Tables
- `Update-TablePlan` - Ändere Pricing Plan
- `Update-TableRetention` - Setze Retention
- `View-TableRetention` - Zeige Retention Settings

### Analytics Rules
- `Get-AnalyticsRules` - Liste alle Rules
- `Get-AnalyticsRuleDetails` - Details zu einer Rule
- `Enable-AnalyticsRule` - Aktiviere Rule
- `Disable-AnalyticsRule` - Deaktiviere Rule
- `Export-AnalyticsRules` - Exportiere Rules als JSON

### Workbooks
- `Get-SentinelWorkbooks` - Liste Workbooks
- `Export-SentinelWorkbook` - Exportiere Workbook
- `Import-SentinelWorkbook` - Importiere Workbook

### Incidents
- `Get-SentinelIncidents` - Liste Incidents
- `Close-SentinelIncident` - Schließe Incident

### Data Collection Rules (DCR)
- `Get-DataCollectionRules` - Liste DCRs
- `New-DCRForTable` - Erstelle DCR für Table
- `Test-DCRIngestion` - Teste Daten-Ingestion

### Watchlists
- `Export-Watchlists` - Exportiere alle Watchlists
- `Backup-SentinelConfig` - Komplettes Config Backup

## Server Status prüfen

Der Server läuft wenn du siehst:
```
╭──────────────────────────────────────────────╮
│      ▄▀▀ ▄▀█ █▀▀ ▀█▀ █▀▄▀█ █▀▀ █▀█         │
│      █▀  █▀█ ▄▄█  █  █ ▀ █ █▄▄ █▀▀         │
│                                              │
│           FastMCP 2.13.1                     │
│                                              │
│  🖥 Server: sentinel-mcp-server              │
│  📦 Transport: STDIO                         │
╰──────────────────────────────────────────────╯
```

## Server neu starten

Falls du den Server neu starten musst:

```powershell
Set-Location C:\Users\PhillipeChaves\projects\sentinel-mcp-server
python src/__main__.py
```

## Troubleshooting

**Problem**: "Server not responding"
- Prüfe ob der Server-Prozess läuft
- Neu starten mit obigem Befehl

**Problem**: "Authentication failed"
- Setze Azure Umgebungsvariablen:
  ```powershell
  $env:AZURE_TENANT_ID = "your-tenant-id"
  $env:AZURE_SUBSCRIPTION_ID = "your-subscription-id"
  ```

**Problem**: "Tool not found"
- Server neu starten
- Prüfe Logs auf Fehler bei Tool-Registrierung

## Beispiel-Queries

Probiere diese Befehle in GitHub Copilot Chat:

1. **Liste Workspaces**: "Show me all Sentinel workspaces"
2. **Analytics Rules**: "Get all enabled analytics rules"
3. **Workbooks**: "Export the workbook 'Security Overview'"
4. **Tables**: "Show me all custom tables in workspace X"
5. **Incidents**: "List open incidents from the last 24 hours"

## Next Steps

1. ✅ Server läuft
2. → Verbinde mit GitHub Copilot Chat
3. → Teste erste Queries
4. → Konfiguriere Azure Credentials
5. → Production Deployment

---

**Weitere Hilfe**: Siehe `docs/02-getting-started.md` und `QUICK-START.md`
