# Django + Angular Architecture

This document records the architecture decisions and the steps taken to migrate the `agora-rivas-python` starter from FastAPI to a Python + Django backend with an Angular frontend, while keeping the clean architecture layering.

## 1. Goals

- Backend: Python with Django.
- Frontend: latest Angular, in the same repository.
- Keep the clean architecture layers (`domain`, `application`, `infrastructure`, `interfaces`, `bootstrap`).
- Provide a functional skeleton with a menu bar, a carousel, and a footer.

## 2. Target architecture

```
Browser
  │
  ├── Angular dev server (localhost:4200)
  │     └── proxy /api ──► Django (localhost:8000)
  │
Django (src/agora_rivas)
  interfaces/api      HTTP views and URLs (Django)
        │
  application         use cases and DTOs (no framework imports)
        │
  domain              entities, exceptions, repository interfaces (no framework imports)
        ▲
  infrastructure      Django settings, WSGI, persistence adapters
  bootstrap           composition root: wires repositories into use cases
```

Dependency rule: outer layers depend on inner layers. `domain` and `application` do not import Django or Angular.

## 3. Toolchain

| Tool | Version |
|------|---------|
| Python | 3.14.6 locally; 3.12 in Docker (Django 6.x needs ≥3.12) |
| Django | 6.1.x (`Django>=6.1,<6.2`) |
| pytest / pytest-django | 8.x / 4.x |
| Node.js | 24.16.0 |
| npm | 11.17.0 |
| Angular | 22.x (TypeScript ~6.0) |

## 4. Steps completed

### Step 1: Backend dependencies (`pyproject.toml`)
- Removed FastAPI, uvicorn, and httpx.
- Added `Django>=6.1,<6.2` as a runtime dependency.
- Added `pytest>=8.0.0` and `pytest-django>=4.8.0` as dev dependencies.
- Set `requires-python` to `>=3.12`.
- Added `[tool.pytest.ini_options]`:
  - `DJANGO_SETTINGS_MODULE = "agora_rivas.infrastructure.config.settings"`
  - `pythonpath = ["src"]`
  - `testpaths = ["tests"]`

### Step 2: Django settings (`src/agora_rivas/infrastructure/config/settings.py`)
- Replaced the FastAPI dataclass `Settings` with Django settings.
- `SECRET_KEY` comes from `DJANGO_SECRET_KEY`.
- `DEBUG` comes from the environment and defaults to `False`.
- `ALLOWED_HOSTS` comes from the environment and defaults to `localhost,127.0.0.1`.
- `INSTALLED_APPS` contains only `django.contrib.contenttypes`, since there are no ORM models, admin, or auth yet.
- Middleware is `CommonMiddleware` only.
- `ROOT_URLCONF = "agora_rivas.infrastructure.config.urls"`.
- SQLite database at `BASE_DIR/db.sqlite3`. It is configured but not used yet.
- `BASE_DIR` is resolved from the file location (`parents[3]`).

### Step 3: URL configuration
- `src/agora_rivas/infrastructure/config/urls.py` (new): mounts `api/` to `agora_rivas.interfaces.api.urls`.
- `src/agora_rivas/infrastructure/config/wsgi.py` (new): standard Django WSGI application.

### Step 4: Interface layer (Django)
- `src/agora_rivas/interfaces/api/urls.py` (new):
  - `health` → `health` view
  - `users` → `create_user` view (no trailing slash, matching the previous `/users` route)
- `src/agora_rivas/interfaces/api/views.py` (new):
  - `health`: GET returns `{"status": "ok"}`.
  - `create_user`: POST parses JSON, requires an object body with string `name` and `email`, calls the existing `CreateUser` use case, and returns `asdict(UserOutput)` with HTTP 200 to match the old behavior. `DomainError` and `ValueError` map to HTTP 400.
- `src/agora_rivas/interfaces/api/routes.py`: deleted (FastAPI routes).

### Step 5: Entry point (`src/agora_rivas/main.py`)
- `main()` sets `DJANGO_SETTINGS_MODULE` if unset and calls `execute_from_command_line`.
- With no arguments it runs `runserver 0.0.0.0:8000`, so `python -m agora_rivas.main` still works for the Dockerfile and docker-compose.

### Step 6: Composition root (`src/agora_rivas/bootstrap/container.py`)
- Content unchanged. It still wires `InMemoryUserRepository` into `CreateUser`.
- Known limitation (pre-existing): a new repository is created per request, so data does not persist across requests.

### Step 7: Tests
- `tests/unit/test_api_create_user.py` migrated to the pytest-django `client` fixture. Covers:
  - create user → 200
  - invalid email → 400
  - health → 200 `{"status": "ok"}`
- `tests/unit/test_create_user.py` (use case) unchanged.
- Result: `python -m pytest` → 4 passed.

### Step 8: Angular scaffold (`src/frontend`)
- Generated with:
  `npx @angular/cli@latest new frontend --defaults --skip-git --skip-install --style=css --ssr=false --routing=false --skip-tests`
- Run from `src`.

### Step 9: Angular components (`src/frontend/src/app/components/`)
- `menu-bar/`: `MenuBar` (`app-menu-bar`). Brand, links to Home, About, Services, and Contact (anchors), mobile toggle via a `menuOpen` signal. OnPush.
- `carousel/`: `Carousel` (`app-carousel`). Three slides, `currentIndex` signal, previous/next and dot navigation, auto-advance every 5 seconds. The timer is cleared with `DestroyRef`. OnPush.
- `footer/`: `Footer` (`app-footer`). Copyright year and backend status (`checking`, `online`, `offline`) from `GET /api/health`. OnPush.

### Step 10: Root wiring
- `src/frontend/src/app/app.ts`: standalone `App` imports `MenuBar`, `Carousel`, `Footer`. OnPush.
- `src/frontend/src/app/app.html`: renders `<app-menu-bar />`, `<main><app-carousel /></main>`, `<app-footer />`.
- `src/frontend/src/app/app.css`: flex column layout so the footer sits at the bottom.
- The default scaffold `title` signal and template were removed.

### Step 11: HTTP client and dev proxy
- `src/frontend/src/app/app.config.ts`: added `provideHttpClient()`.
- `src/frontend/proxy.conf.json` (new): `/api` → `http://localhost:8000`, with `changeOrigin` on.
- `src/frontend/angular.json`: `serve` options set `proxyConfig` to `proxy.conf.json`.

### Step 12: Build and verification
- `npm install` in `src/frontend` completed. npm reported skipped install scripts for `esbuild`, `lmdb`, and `msgpackr-extract`; the build still succeeded.
- `npx ng build` succeeded. Initial bundle is about 147.76 kB raw, 43.68 kB transfer.
- `python -m pytest` → 4 passed.
- `.gitignore` coverage confirmed: `src/frontend/.gitignore` ignores `/node_modules` and `/dist`; root `.gitignore` ignores `db.sqlite3`.

## 5. Pending work

- [ ] Update `README.md` to describe the Django + Angular setup and run instructions. It still describes FastAPI.
- [ ] Update `.env.example`: remove `API_PREFIX`; add `DJANGO_SECRET_KEY` and `ALLOWED_HOSTS`.
- [ ] Update `docker-compose.yml`: remove `API_PREFIX`; add the Django variables.
- [ ] Update the `Dockerfile` comment that says "FastAPI service only".
- [ ] Run the end-to-end check: `python -m agora_rivas.main` plus `npx ng serve`. Confirm the footer shows "Backend: online" and the carousel advances.
- [ ] Decide production serving. Currently `runserver` is used, which is not production-grade. Options are gunicorn behind a reverse proxy, or Django serving the built Angular bundle.
- [ ] Decide whether the in-memory repository should become a persistent adapter (Django ORM) in `infrastructure`.

## 6. How to run (development)

Backend:
```powershell
pip install -e ".[dev]"
$env:DJANGO_SECRET_KEY = "change-me"
python -m agora_rivas.main
```

Frontend:
```powershell
cd src\frontend
npm install
npx ng serve
```

Open `http://localhost:4200`. API requests to `/api/*` are proxied to `http://localhost:8000`.

## 7. Test

```powershell
python -m pytest
```

## 8. Architecture decisions

| Decision | Reason |
|----------|--------|
| Django without ORM models or auth/admin for now | Keeps the skeleton small. Persistence stays behind the repository interface. |
| Angular in `src/frontend` | Keeps the frontend in the same repository and within `src`, as requested. |
| Dev proxy instead of CORS | Same-origin requests in development; no CORS configuration needed. |
| Keep `domain` and `application` framework-free | Preserves clean architecture; these layers are testable without Django. |
| Keep `CreateUser` id `"user-1"` | Pre-existing behavior that the test relies on. Change only with the test. |
