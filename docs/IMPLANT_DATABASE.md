# Patient-Specific Implant Sizing Database

## 1. Purpose
The Implant Sizing Database module satisfies Phase 8 of the project plan. It provides a structured data foundation containing dimensional specifications of femoral and tibial components. This repository makes it possible for future modules to evaluate patient anatomical dimensions against available component sizes.

## 2. Dataset Versioning & Demo Nature
**CRITICAL LIMITATION**: The current MVP utilizes completely synthetic, demonstration-only implant specifications.
- `dataset_version`: "demo-v1"
- `source_type`: "synthetic_demo"
- `is_demo`: true

This structure explicitly prevents the prototype from presenting mathematically derived synthetic specs as clinically validated commercial models.

## 3. Database Architecture
- **Technology**: SQLite / SQLAlchemy.
- **Models**: The `ImplantComponent` table unifies both femoral and tibial records via a `component_type` column.
- **Initialization**: Automatically managed via FastAPI lifecycle events (`startup`).
- **Seeding**: An idempotent `seed_demo_implants()` function guarantees the database is pre-populated without duplicate row entries upon backend restart.

## 4. API Endpoints
The following endpoints reside under `/api/v1/implants/`:
- `GET /` - Fetches all implants, supports optional `?component_type=` and `?size=` filtering.
- `GET /femoral` - Fetches exclusively femoral components.
- `GET /tibial` - Fetches exclusively tibial components.
- `GET /{implant_id}` - Fetch by specific UUID.

## 5. Schema Fields
- `id`: UUID Primary Key
- `component_type`: "femoral" | "tibial"
- `size`: Internal sizing string (e.g. "1", "2")
- `width`: Float mm
- `ap_dimension`: Float mm
- `manufacturer`: String
- `model_name`: String
- `is_demo`: Boolean flag for clinical isolation

## 6. Frontend Integration
The frontend utilizes `api.ts` to retrieve records and renders them in the `ImplantDatabasePanel`. The panel displays massive visual warnings that the dataset is "NOT for clinical or surgical use", ensuring safety compliance within the hackathon prototype.

## 7. Future Validated-Data Import
The schema accommodates a future `scripts/import_implants.py` integration capable of inserting validated CSV/JSON manufacturer documentation while toggling `is_demo=False`.
