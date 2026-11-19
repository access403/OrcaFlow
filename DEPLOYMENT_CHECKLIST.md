# Deployment Checklist

## Before starting

- [ ] Install and start Docker Desktop (or another Docker Engine with Compose v2).
- [ ] Confirm `docker compose version` works.
- [ ] Use a supported Python installation for local tests.
- [ ] Keep the frontend bound to localhost unless an authenticated ingress is configured.
- [ ] Set `ORCAFLOW_WEB_PORT` if port `8080` is already in use.

## Verify backend tests

From the repository root:

```powershell
python -m pytest -q
```

Expected result: all current tests pass.

## Build and start services

From the repository root:

```powershell
docker compose config
docker compose up --build -d
docker compose ps
```

Confirm the backend reports healthy and the frontend is running.

## Smoke checks

Open `http://127.0.0.1:8080/` (or the configured `ORCAFLOW_WEB_PORT`) and confirm the OrcaFlow placeholder page loads.

Check the task-routing API through the local frontend proxy:

```powershell
$body = @{ task = "Compare two deployment approaches" } | ConvertTo-Json
Invoke-RestMethod -Uri "http://127.0.0.1:8080/manager/tasks" -Method Post -ContentType "application/json" -Body $body
```

The response should contain `task_type`, `selected_agent`, and `execution_plan`. This endpoint plans and routes tasks; it does not execute agent work.

## Stop services

```powershell
docker compose down
```

## Release limitations

- The Compose port is bound to `127.0.0.1`; do not change it to a public bind without adding an access-control policy.
- The frontend is a static deployment placeholder, not a product UI.
- The Research, Developer, and Analyst agents are not implemented as task executors.
- SQLite persistence and migrations are not implemented.
