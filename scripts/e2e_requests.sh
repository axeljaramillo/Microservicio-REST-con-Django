#!/usr/bin/env bash
set -euo pipefail

# End-to-end: start docker, wait for API, run example requests (create user, token, curso, lección, inscripción, comentario), and save outputs.

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")"/.. && pwd)"
cd "$ROOT_DIR"

OUT="$ROOT_DIR/docs/ejemplos_requests.txt"
mkdir -p "$ROOT_DIR/docs"

echo "[+] Building and starting services..." >&2
docker compose up -d --build

echo "[+] Waiting for API to be ready..." >&2
for i in {1..60}; do
  code=$(curl -s -o /dev/null -w "%{http_code}" http://localhost:8500/swagger.json || true)
  if [[ "$code" == "200" ]]; then echo "ready" >&2; break; fi
  sleep 1
done

: > "$OUT"
echo "=== Ejemplos de requests ($(date)) ===" | tee -a "$OUT" >/dev/null
echo "web ready" | tee -a "$OUT" >/dev/null

# Unique username per run
TS=$(date +%s)
USERNAME="demo_api_${TS}"
PASSWORD="demopass"

printf "\n--- registrar usuario (POST /api/users/) ---\n" | tee -a "$OUT" >/dev/null
printf "USERNAME=%s\n" "$USERNAME" | tee -a "$OUT" >/dev/null
U=$(curl -sS -X POST http://localhost:8500/api/users/ \
  -H "Accept: application/json" -H "Content-Type: application/json" \
  -d "{\"username\":\"$USERNAME\",\"email\":\"$USERNAME@example.com\",\"password\":\"$PASSWORD\",\"first_name\":\"De\",\"last_name\":\"Mo\"}")
printf "%s\n" "$U" | tee -a "$OUT" >/dev/null

printf "\n--- obtener token (POST /api/token-auth/) ---\n" | tee -a "$OUT" >/dev/null
T=$(curl -sS -X POST http://localhost:8500/api/token-auth/ \
  -H "Accept: application/json" -H "Content-Type: application/json" \
  -d "{\"username\":\"$USERNAME\",\"password\":\"$PASSWORD\"}")
printf "%s\n" "$T" | tee -a "$OUT" >/dev/null
TOKEN=$(printf "%s" "$T" | python3 - "$OUT" << 'PY'
import sys, json
data = sys.stdin.read().strip()
try:
    print(json.loads(data)["token"])  # noqa: T201
except Exception:
    print("")  # noqa: T201
PY
)

printf "\n--- crear curso (POST /api/cursos/) ---\n" | tee -a "$OUT" >/dev/null
C=$(curl -sS -X POST http://localhost:8500/api/cursos/ \
  -H "Authorization: Token $TOKEN" \
  -H "Accept: application/json" -H "Content-Type: application/json" \
  -d '{"title":"Python 103","description":"Avanzado"}')
printf "%s\n" "$C" | tee -a "$OUT" >/dev/null
COURSE_ID=$(printf "%s" "$C" | python3 - << 'PY'
import sys, json
data = sys.stdin.read().strip()
try:
    print(json.loads(data)["id"])  # noqa: T201
except Exception:
    print("")  # noqa: T201
PY
)
echo "COURSE_ID=$COURSE_ID" | tee -a "$OUT" >/dev/null

printf "\n--- crear leccion (POST /api/lecciones/) ---\n" | tee -a "$OUT" >/dev/null
L=$(curl -sS -X POST http://localhost:8500/api/lecciones/ \
  -H "Authorization: Token $TOKEN" \
  -H "Accept: application/json" -H "Content-Type: application/json" \
  -d '{"course":'$COURSE_ID',"title":"Intro Avanzada","content":"Contenido","order":1,"duration_minutes":10}')
printf "%s\n" "$L" | tee -a "$OUT" >/dev/null
LESSON_ID=$(printf "%s" "$L" | python3 - << 'PY'
import sys, json
data = sys.stdin.read().strip()
try:
    print(json.loads(data)["id"])  # noqa: T201
except Exception:
    print("")  # noqa: T201
PY
)
echo "LESSON_ID=$LESSON_ID" | tee -a "$OUT" >/dev/null

printf "\n--- crear inscripcion (POST /api/inscripciones/) ---\n" | tee -a "$OUT" >/dev/null
E=$(curl -sS -X POST http://localhost:8500/api/inscripciones/ \
  -H "Authorization: Token $TOKEN" \
  -H "Accept: application/json" -H "Content-Type: application/json" \
  -d '{"course":'$COURSE_ID',"is_active":true}')
printf "%s\n" "$E" | tee -a "$OUT" >/dev/null
ENROLL_ID=$(printf "%s" "$E" | python3 - << 'PY'
import sys, json
data = sys.stdin.read().strip()
try:
    print(json.loads(data)["id"])  # noqa: T201
except Exception:
    print("")  # noqa: T201
PY
)
echo "ENROLL_ID=$ENROLL_ID" | tee -a "$OUT" >/dev/null

printf "\n--- crear comentario (POST /api/comentarios/) ---\n" | tee -a "$OUT" >/dev/null
M=$(curl -sS -X POST http://localhost:8500/api/comentarios/ \
  -H "Authorization: Token $TOKEN" \
  -H "Accept: application/json" -H "Content-Type: application/json" \
  -d '{"course":'$COURSE_ID',"content":"Excelente","rating":5}')
printf "%s\n" "$M" | tee -a "$OUT" >/dev/null
COMMENT_ID=$(printf "%s" "$M" | python3 - << 'PY'
import sys, json
data = sys.stdin.read().strip()
try:
    print(json.loads(data)["id"])  # noqa: T201
except Exception:
    print("")  # noqa: T201
PY
)
echo "COMMENT_ID=$COMMENT_ID" | tee -a "$OUT" >/dev/null

printf "\n--- listar (GET) ---\n" | tee -a "$OUT" >/dev/null
printf "API root:\n" | tee -a "$OUT" >/dev/null
curl -sS http://localhost:8500/api/ | tee -a "$OUT" >/dev/null; echo "" | tee -a "$OUT" >/dev/null
printf "Cursos:\n" | tee -a "$OUT" >/dev/null
curl -sS http://localhost:8500/api/cursos/ | tee -a "$OUT" >/dev/null; echo "" | tee -a "$OUT" >/dev/null
printf "Lecciones:\n" | tee -a "$OUT" >/dev/null
curl -sS http://localhost:8500/api/lecciones/ | tee -a "$OUT" >/dev/null; echo "" | tee -a "$OUT" >/devnull
printf "Inscripciones:\n" | tee -a "$OUT" >/dev/null
curl -sS http://localhost:8500/api/inscripciones/ | tee -a "$OUT" >/dev/null; echo "" | tee -a "$OUT" >/dev/null
printf "Comentarios:\n" | tee -a "$OUT" >/dev/null
curl -sS http://localhost:8500/api/comentarios/ | tee -a "$OUT" >/dev/null; echo "" | tee -a "$OUT" >/dev/null

echo "\nArchivo generado: $OUT" | tee -a "$OUT" >/dev/null
echo "[+] Done. Outputs saved to $OUT" >&2
