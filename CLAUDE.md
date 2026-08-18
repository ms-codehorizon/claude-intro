# Identity

You are helping build a learning workspace for Claude API experiments and prompt evaluation.

## Rules

- Write in plain, clear language.
- Ask clarifying questions before making assumptions.
- When unsure, say so.
- Provide code in small, modular, testable chunks — not large notebook dumps.
- Keep the user's workflow simple; avoid over-engineering.

## Where code lives

| Location | Put here |
|----------|----------|
| `helper_*.py` | Reusable logic shared across notebooks |
| `001_*.ipynb` | Experiments, parameters, `run_prompt`, one-off calls |

**Do not** duplicate helper logic in notebooks. If it appears in two notebooks, extract it to a `helper_*.py` file.

**Do not** use `%run notebook.ipynb` for shared code.

### Module chain (respect this order)

```
helper_client_setup → helper_chat → helper_prompt_evaluator → helper_report_builder
```

- `helper_client_setup` — env, `client`, `model` only
- `helper_chat` — `add_user_message`, `add_assistant_message`, `chat()`
- `helper_prompt_evaluator` — `PromptEvaluator` class
- Notebooks import helpers; import `client`/`model` directly only when calling the API outside `chat()` (e.g. streaming)

## When editing notebooks

- `001_prompting.ipynb` / `001_prompting_excercise.ipynb` — use `PromptEvaluator`; notebook should only define `run_prompt` and call `generate_dataset` / `run_evaluation`
- `001_prompt_eval.ipynb` — self-contained AWS eval (not yet on `PromptEvaluator`); do not force-merge unless asked
- `001_requests.ipynb` — API basics; should use `helper_chat` when refactored

Each notebook uses its own dataset/output filenames (e.g. `dataset_prompting.json`, `output_prompting.html`). Do not overwrite another notebook's artifacts.

## API conventions (must follow)

- `client.messages.create()` requires `messages` (list) and `max_tokens` — never `message`, `token`, or `max_token`
- Evaluation prompts must use **f-strings** to inject task/solution — literal `{task}` causes score 0
- `temperature=0.0` for grading; higher for dataset idea generation
- `generate_dataset()` caches to disk; use `force_regenerate=True` when task or `num_cases` changes

## Do not

- Commit `.env` or API keys
- Hardcode absolute paths in helpers — use `Path(__file__).resolve().parent`
- Add dependencies without updating `pyproject.toml`
- Refactor notebooks the user did not ask to change

## Known pitfalls

- Stale cached dataset after changing `task_description`
- `PromptEvaluator` rate limits — keep `max_concurrent_tasks` at 1–3
- Import errors if kernel cwd is not the project root
