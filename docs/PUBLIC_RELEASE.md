# Public release handoff — 28 October 2026

## Prepared deployment

`render.yaml` defines one Python web service on Render's `free` plan, installs `requirements.txt`, starts `uvicorn app:app --host 0.0.0.0 --port $PORT`, and checks `/health`. The YAML was parsed locally and the same app served successfully at `127.0.0.1:8767`. Render's [Blueprint specification](https://render.com/docs/blueprint-spec), [FastAPI guide](https://render.com/docs/deploy-fastapi), and [free-service limits](https://render.com/docs/free) support this configuration. Free services sleep after inactivity; the first visit can take about a minute. No database, paid service or key is required.

## Exact owner actions

1. Open a **normal, unsandboxed PowerShell window** as the Windows owner in this project directory. Do not change ACLs from the Codex sandbox. Run:

   ```powershell
   git add .gitignore README.md app.py engine.py requirements.txt requirements-dev.txt package.json package-lock.json render.yaml static tests docs learning
   git commit -m "Release QUBO Arena MVP"
   git status --short --branch
   ```

   In this sandbox `.git` has explicit ACL denies for writes; `index.lock` does **not** exist. The owner account has FullControl in the observed ACL. If an unsandboxed window still cannot commit, inspect `icacls .git` before modifying permissions.

2. Authenticate GitHub in that same owner session with `gh auth login -h github.com`. The currently configured `chapaevv123` token reports invalid. After choosing the intended GitHub account and reviewing repository visibility, publish with:

   ```powershell
   gh repo create qubo-arena --public --source . --remote origin --push
   ```

   Copy the **returned** URL into README and the Builder application. No GitHub URL is known yet.

3. In Render, connect the published GitHub repository and create a **Blueprint** from `render.yaml`, confirming the `Free` plan. Wait for deployment success, open the returned `onrender.com` URL and run the full browser journey there. Copy the **returned** URL into README and the application. No demo URL is known yet.

4. From a network-enabled owner machine or the deployed service, load `/api/qms/status`. Record chain ID, observed head, latest block number/hash/timestamp, `checked_at`, and the explorer link. If it remains `UNAVAILABLE`, preserve the diagnostic and do not claim live chain verification.

5. Review [the application draft](BUILDER_APPLICATION.md), add real owner/team details and the verified URLs, then submit through the official QMS form.

## Release gate

Local core: passed. Live QMS response: blocked by WinError 10013 in this environment. Git commit: blocked by `.git` write ACL. GitHub auth: current token invalid. Public deployment: not created. Therefore no public URLs or submitted application are claimed.
