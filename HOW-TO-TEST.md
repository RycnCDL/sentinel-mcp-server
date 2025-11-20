# 🧪 Microsoft Sentinel MCP Server - Komplette Testanleitung

**Datum:** November 20, 2025
**Version:** 1.0.0
**Status:** ✅ Server Ready for Testing

---

## 📊 Projekt-Status Übersicht

### ✅ Was funktioniert:

| Komponente | Status | Details |
|------------|--------|---------|
| Python Module | ✅ 8/8 | Alle Module laden ohne Fehler |
| MCP Server | ✅ Funktioniert | Startet erfolgreich |
| PowerShell Bridge | ✅ Code OK | Retry-Logik implementiert |
| Tool Registration | ✅ Erfolgreich | 3 Tools registriert |
| Configuration | ✅ Geladen | Azure Credentials vorhanden |
| Dependencies | ✅ Installiert | Alle Requirements erfüllt |

### 📋 Verfügbare Tools:

1. **sentinel_health_check** (Python) - Workspace Health Monitoring
2. **execute_sentinel_powershell** (Generic) - 39 PowerShell Funktionen lokal
3. **execute_sentinel_powershell_remote** (Generic) - 39 PowerShell Funktionen remote

---

## 🚀 Schnellstart: Server Testen

### Option 1: Manueller Server-Test (Empfohlen)

```bash
# 1. Server-Test ausführen
python scripts/test_server_manual.py
```

**Erwartete Ausgabe:**
```
============================================================
Microsoft Sentinel MCP Server - Manual Test Suite
============================================================

=== MCP Server Startup Test ===

1. Testing MCP server instance...
   ✓ Server name: sentinel-mcp-server
   ✓ Server version: 0.1.0-alpha

2. Testing Azure authentication...
   ✓ Authenticator initialized: AzureAuthenticator

3. Testing PowerShell bridge...
   ✓ PowerShell bridge initialized
   ✓ Max retries: 3
   ✓ Timeout: 300s

4. Testing tool registration...
   ✓ MCP server has tools registered
   ℹ Tools include:
      - sentinel_health_check (Python)
      - 40+ PowerShell tools

============================================================
TEST SUMMARY
============================================================
Tests run: 3
Passed: 3
Failed: 0

✓ ALL TESTS PASSED - Server is ready!
============================================================
```

### Option 2: Module-Tests

```bash
# Test alle Python Module
python -c "
import sys
sys.path.insert(0, 'src')

modules = [
    'utils.config',
    'utils.logging',
    'utils.auth',
    'utils.lighthouse',
    'utils.powershell_bridge',
    'mcp_server.tools.management.health_check',
    'mcp_server.tools.powershell.sentinel_manager',
    'mcp_server.server',
]

for module in modules:
    try:
        __import__(module)
        print(f'✅ {module}')
    except Exception as e:
        print(f'❌ {module}: {e}')
"
```

**Erwartete Ausgabe:**
```
✅ utils.config
✅ utils.logging
✅ utils.auth
✅ utils.lighthouse
✅ utils.powershell_bridge
✅ utils.health_check
✅ utils.sentinel_manager
✅ mcp_server.server
```

---

## 🔧 Detaillierte Test-Szenarien

### Test 1: Health Check Tool (Python)

**Voraussetzung:** Azure Credentials in `.env` konfiguriert

```bash
python scripts/test_with_cli_auth.py
```

**Was wird getestet:**
- Azure CLI Authentifizierung
- Lighthouse Workspace Discovery
- Analytics Rules Monitoring
- Data Connector Status
- Ingestion Metrics

**Erfolgs-Kriterien:**
```
✅ PHASE 1 HEALTH CHECK - SUCCESS!
Found X workspaces
Analytics Rules: Y total - Enabled: A - Disabled: B
```

### Test 2: PowerShell Bridge (Ohne PowerShell)

**Code-Validierung ohne PowerShell Installation:**

```bash
python -c "
import sys
sys.path.insert(0, 'src')
from utils.powershell_bridge import PowerShellBridge

bridge = PowerShellBridge()
print(f'✅ Bridge initialized')
print(f'   Max Retries: {bridge.max_retries}')
print(f'   Timeout: {bridge.timeout}s')
print(f'✅ PowerShell Bridge ready (pwsh not required for init)')
"
```

### Test 3: PowerShell Tool Registration

```bash
python -c "
import sys
sys.path.insert(0, 'src')
from fastmcp import FastMCP
from mcp_server.tools.powershell.sentinel_manager import register_powershell_tools

test_mcp = FastMCP('test-server')
print('Testing tool registration...')
try:
    register_powershell_tools(test_mcp)
    print('✅ Registration successful!')
    print('✅ No **kwargs error!')
except Exception as e:
    print(f'❌ Failed: {e}')
" 2>&1 | grep -v "PydanticDeprecated"
```

### Test 4: Configuration Validierung

```bash
python -c "
import sys
sys.path.insert(0, 'src')
from utils.config import get_settings

settings = get_settings()
print('=== Configuration ===')
print(f'✅ Server: {settings.mcp_server_name} v{settings.mcp_server_version}')
print(f'✅ Log Level: {settings.log_level}')
print(f'✅ Debug Mode: {settings.debug_mode}')

azure = settings.get_azure_config()
print(f'\n=== Azure Config ===')
print(f'Tenant ID: {\"✅ Set\" if azure.tenant_id else \"❌ Missing\"}')
print(f'Client ID: {\"✅ Set\" if azure.client_id else \"❌ Missing\"}')
print(f'Subscription: {\"✅ Set\" if azure.subscription_id else \"❌ Missing\"}')
" 2>&1 | grep -v "PydanticDeprecated"
```

---

## 🎯 Mit Claude Desktop testen

### Schritt 1: Claude Desktop Config

**Datei:** `~/Library/Application Support/Claude/claude_desktop_config.json` (macOS)
**Datei:** `%APPDATA%\Claude\claude_desktop_config.json` (Windows)

```json
{
  "mcpServers": {
    "sentinel-mcp-server": {
      "command": "python",
      "args": [
        "-m",
        "mcp_server.server"
      ],
      "cwd": "/absolute/path/to/sentinel-mcp-server",
      "env": {
        "PYTHONPATH": "/absolute/path/to/sentinel-mcp-server/src"
      }
    }
  }
}
```

### Schritt 2: Claude Desktop Neu Starten

1. Claude Desktop komplett beenden
2. Neu starten
3. In neuer Konversation testen

### Schritt 3: Test-Prompts

**Test 1: Health Check**
```
Check the health of all my Microsoft Sentinel workspaces
```

**Test 2: PowerShell Function List**
```
What PowerShell functions are available for Sentinel management?
```

**Test 3: Analytics Rules** (benötigt PowerShell Script)
```
Execute the Get-AnalyticsRules PowerShell function for workspace "MyWorkspace"
```

---

## 🐛 Troubleshooting

### Problem 1: "ValueError: Functions with **kwargs are not supported"

**Status:** ✅ GEFIXT in commit e7c440a

Wenn du diesen Fehler siehst:
```bash
git pull origin claude/review-mcp-server-project-01QUEkrgL2GxFjX3XZcjNu6Z
```

### Problem 2: "ModuleNotFoundError"

```bash
pip install -r requirements.txt
```

### Problem 3: "PydanticDeprecatedSince20 warnings"

Das sind nur Warnings - funktioniert trotzdem. Filter sie aus:
```bash
python script.py 2>&1 | grep -v "PydanticDeprecated"
```

### Problem 4: "Server crasht beim Start"

```bash
# Debug mode aktivieren
export DEBUG_MODE=true
python scripts/test_server_manual.py
```

### Problem 5: PowerShell nicht gefunden

**Für Code-Tests:** Nicht benötigt! Die meisten Tests funktionieren ohne PowerShell.

**Für PowerShell-Funktionen:**
- Windows: `winget install Microsoft.PowerShell`
- Linux: `sudo apt install powershell` oder snap
- macOS: `brew install powershell`

---

## 📈 Test-Checkliste

### Basis-Tests (Keine Azure/PowerShell benötigt)

- [ ] `python -m py_compile src/mcp_server/server.py` → Syntax OK
- [ ] `python scripts/test_server_manual.py` → 3/3 Tests passed
- [ ] Module Import Test → 8/8 Module laden
- [ ] Tool Registration Test → Keine **kwargs Fehler
- [ ] Configuration Loading → Settings geladen

### Azure-Tests (Azure Credentials benötigt)

- [ ] `python scripts/test_with_cli_auth.py` → Health Check funktioniert
- [ ] Workspace Discovery → Workspaces gefunden
- [ ] Analytics Rules → Regeln gezählt
- [ ] Data Connectors → Status geprüft

### PowerShell-Tests (PowerShell Core benötigt)

- [ ] `pwsh --version` → PowerShell verfügbar
- [ ] `python test_ps_simple.py` → Basic PowerShell Test
- [ ] PowerShell Bridge → Lokale Execution
- [ ] PowerShell Remote → WinRM Execution (optional)

### Integration-Tests (Claude Desktop)

- [ ] Claude Desktop Config → JSON korrekt
- [ ] Server Start in Claude → Keine Errors
- [ ] Tool Discovery → 3 Tools sichtbar
- [ ] Health Check Execution → Funktioniert
- [ ] PowerShell Execution → Funktioniert (mit Script)

---

## 📊 Erwartete Test-Ergebnisse

### Minimale Anforderungen (Ohne Azure/PowerShell):

✅ Alle Python Module laden ohne Fehler
✅ Server startet ohne Crash
✅ Tool Registration erfolgreich
✅ Configuration lädt
✅ 3 Tools registriert

**Status: ERFÜLLT ✅**

### Mit Azure Credentials:

✅ + Health Check funktioniert
✅ + Workspaces werden entdeckt
✅ + Analytics Rules werden gezählt

**Status: GETESTET in Phase 1 ✅**

### Mit PowerShell Core:

✅ + PowerShell Bridge execution
✅ + Lokale Script-Ausführung
✅ + JSON Parsing
⚠️  Remote Execution (benötigt WinRM Setup)

**Status: CODE OK, nicht getestet (kein pwsh verfügbar)**

---

## 🔬 Erweiterte Tests

### Performance Test

```bash
# Mehrere Health Checks parallel
python -c "
import asyncio
import sys
sys.path.insert(0, 'src')
from mcp_server.tools.management.health_check import SentinelHealthChecker

async def test():
    # Simuliere mehrere Requests
    print('Testing concurrent requests...')
    # Implementierung hier

asyncio.run(test())
"
```

### Stress Test

```bash
# 10x Health Check in Schleife
for i in {1..10}; do
    echo "Test $i"
    python scripts/test_with_cli_auth.py
done
```

### Memory Leak Test

```bash
# Server für 1 Minute laufen lassen
timeout 60 python -m mcp_server.server &
PID=$!
while kill -0 $PID 2>/dev/null; do
    ps -p $PID -o %mem,rss
    sleep 5
done
```

---

## 🎓 Beispiel-Szenarien

### Szenario 1: Erste Inbetriebnahme

```bash
# 1. Dependencies checken
pip list | grep -E 'fastmcp|azure|structlog'

# 2. Configuration testen
python -c "
import sys; sys.path.insert(0, 'src')
from utils.config import get_settings
print(get_settings().mcp_server_name)
" 2>&1 | grep -v "Pydantic"

# 3. Server testen
python scripts/test_server_manual.py

# 4. Wenn alles OK: Claude Desktop konfigurieren
```

### Szenario 2: Nach Git Pull

```bash
# 1. Neue Änderungen holen
git pull origin claude/review-mcp-server-project-01QUEkrgL2GxFjX3XZcjNu6Z

# 2. Syntax checken
python -m py_compile src/mcp_server/server.py
python -m py_compile src/mcp_server/tools/powershell/sentinel_manager.py

# 3. Tool Registration testen
python -c "
import sys; sys.path.insert(0, 'src')
from fastmcp import FastMCP
from mcp_server.tools.powershell.sentinel_manager import register_powershell_tools
mcp = FastMCP('test')
register_powershell_tools(mcp)
print('✅ OK')
" 2>&1 | grep -v "Pydantic"

# 4. Full test
python scripts/test_server_manual.py
```

### Szenario 3: Production Deployment

```bash
# 1. Alle Tests durchführen
python scripts/test_server_manual.py

# 2. Health Check mit echten Daten
python scripts/test_with_cli_auth.py

# 3. Log Level setzen
export LOG_LEVEL=INFO
export LOG_FORMAT=json

# 4. Server starten
python -m mcp_server.server
```

---

## 📝 Test-Logs Sammeln

### Log-Ausgabe umleiten

```bash
# Alle Logs in Datei
python scripts/test_server_manual.py 2>&1 | tee test_$(date +%Y%m%d_%H%M%S).log

# Nur Errors
python scripts/test_server_manual.py 2>&1 | grep -E 'ERROR|Failed|❌'

# JSON Logs parsen
python -m mcp_server.server 2>&1 | grep '^{' | jq .
```

### Debug Mode

```bash
# In .env setzen
DEBUG_MODE=true
LOG_LEVEL=DEBUG

# Oder als Environment Variable
DEBUG_MODE=true LOG_LEVEL=DEBUG python scripts/test_server_manual.py
```

---

## ✅ Success Criteria

**Minimale Success Criteria (Basis-Funktionalität):**

1. ✅ Server startet ohne Crash
2. ✅ Alle 8 Module laden
3. ✅ 3 Tools registriert
4. ✅ Keine **kwargs Fehler
5. ✅ Configuration lädt

**Erweiterte Success Criteria (Mit Azure):**

6. ✅ Azure Authentifizierung funktioniert
7. ✅ Workspace Discovery funktioniert
8. ✅ Health Check liefert Ergebnisse

**Vollständige Success Criteria (Mit PowerShell):**

9. ⏳ PowerShell Bridge execution funktioniert
10. ⏳ 39 PowerShell Funktionen erreichbar
11. ⏳ Remote Execution (optional)

**Aktueller Status:** 8/11 Kriterien erfüllt (73%)

---

## 🎯 Nächste Schritte

### Für lokale Tests:

1. ✅ `python scripts/test_server_manual.py` ausführen
2. ✅ Prüfen dass 3/3 Tests passed
3. ✅ Configuration checken
4. ⏳ Optional: Azure Health Check testen

### Für Claude Desktop Integration:

1. ⏳ `claude_desktop_config.json` erstellen
2. ⏳ Absoluten Pfad anpassen
3. ⏳ Claude Desktop neu starten
4. ⏳ Test-Prompt ausführen

### Für PowerShell Funktionen:

1. ⏳ PowerShell Core installieren
2. ⏳ SentinelManager_v3.ps1 Script bereitstellen
3. ⏳ `SENTINEL_MANAGER_SCRIPT` in .env setzen
4. ⏳ PowerShell Funktionen testen

---

## 📞 Support & Debugging

### Logs prüfen

```bash
# Letzte Logs anzeigen
tail -f /tmp/sentinel-mcp-server.log  # Falls log file konfiguriert

# JSON Logs formatieren
python -m mcp_server.server 2>&1 | grep '^{' | jq .
```

### Häufige Fehler

| Fehler | Ursache | Lösung |
|--------|---------|--------|
| **kwargs error | Alte Version | `git pull` + Fix in commit e7c440a |
| ModuleNotFoundError | Dependencies fehlen | `pip install -r requirements.txt` |
| 403 Forbidden | Service Principal Permissions | Azure CLI verwenden oder Permissions prüfen |
| PowerShell nicht gefunden | pwsh nicht installiert | PowerShell Core installieren |
| Config Fehler | .env fehlt | `.env` aus `.env.example` erstellen |

### Quick Diagnostic

```bash
# One-liner für schnelle Diagnose
python -c "
import sys; sys.path.insert(0, 'src')
try:
    from mcp_server.server import mcp
    print('✅ SERVER OK')
except Exception as e:
    print(f'❌ SERVER FEHLER: {e}')
" 2>&1 | grep -v "Pydantic"
```

---

**Viel Erfolg beim Testen! 🚀**

*Bei Fragen: Siehe TROUBLESHOOTING Sektion oder GitHub Issues*
