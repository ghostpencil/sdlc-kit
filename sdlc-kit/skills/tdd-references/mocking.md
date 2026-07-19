# When to Mock

Mock at **system boundaries** only:

- External APIs (LLM providers, payment, email)
- File system (when testing logic, not I/O)
- Time/randomness
- Arcade draw_* functions (no display available in headless tests)

Don't mock:

- Your own Pydantic models
- Internal collaborators (DungeonRepository internals)
- Anything you fully control

## Designing for Mockability

At system boundaries, design interfaces that are easy to mock:

**1. Use dependency injection**

Pass external dependencies in rather than creating them internally:

```python
# Easy to mock — LLMProvider is injected
class DesignAgent:
    def __init__(self, provider: LLMProvider) -> None:
        self._provider = provider

# Hard to mock — creates its own provider
class DesignAgent:
    def __init__(self) -> None:
        self._provider = AnthropicProvider()
```

**2. Prefer specific interfaces over generic ones**

```python
# GOOD: Each method is independently testable
class DungeonRepository:
    def load(self, name: str) -> Dungeon: ...
    def save(self, dungeon: Dungeon, name: str) -> None: ...
    def load_session(self, name: str) -> SessionState | None: ...

# BAD: One generic method requires conditional logic in mocks
class DungeonRepository:
    def execute(self, operation: str, **kwargs): ...
```
