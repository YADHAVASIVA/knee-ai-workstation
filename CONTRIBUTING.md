# Contributing to Knee AI Workstation

Thank you for your interest in contributing! This project is a research prototype.

## Code of Conduct

Please treat all contributors with respect.

## How to Contribute

1. **Fork the repository**
2. **Create a new branch** (`git checkout -b feature/amazing-feature`)
3. **Make your changes**
   - Ensure the frontend builds without errors (`cd frontend && npm run build`)
   - Ensure the backend tests pass (`cd backend && pytest`)
4. **Commit your changes** (`git commit -m 'Add amazing feature'`)
5. **Push to the branch** (`git push origin feature/amazing-feature`)
6. **Open a Pull Request**

## Development Guidelines

- **Strict Data Integrity:** Do not introduce "fake" or "mock" clinical data. If a feature requires data that is unavailable (e.g., specific DICOM metadata), handle it gracefully and mark the resulting state as incomplete or unavailable.
- **UI/UX Consistency:** The frontend uses a strict 8px grid system and a custom design token set. Follow the established patterns in `frontend/src/styles/tokens.css` and existing components. Do not use inline styles unless absolutely necessary.
- **Provenance Tracking:** Any data displayed to the user must carry a provenance tag (`[AI]`, `[USER]`, `[DICOM]`, `[CALCULATED]`).

## Reporting Bugs

Please use the GitHub Issue tracker to report bugs. Include:
- Steps to reproduce
- Expected behavior
- Actual behavior
- Screenshots (if applicable)
