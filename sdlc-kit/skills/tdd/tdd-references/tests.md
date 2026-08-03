# Good and Bad Tests

## Good Tests

**Integration-style**: Test through real interfaces, not mocks of internal parts.

```python
# GOOD: Tests observable behavior
def test_dungeon_round_trip(sample_dungeon):
    data = sample_dungeon.model_dump(mode="json")
    restored = Dungeon.model_validate(data)
    assert restored == sample_dungeon
```

Characteristics:

- Tests behavior users/callers care about
- Uses public API only
- Survives internal refactors
- Describes WHAT, not HOW
- One logical assertion per test

## Bad Tests

**Implementation-detail tests**: Coupled to internal structure.

```python
# BAD: Tests implementation details
def test_repository_calls_json_dumps(mocker):
    mock_dumps = mocker.patch("json.dumps")
    repo.save(dungeon, "test")
    mock_dumps.assert_called_once()
```

Red flags:

- Mocking internal collaborators
- Testing private methods
- Asserting on call counts/order of internal calls
- Test breaks when refactoring without behavior change
- Test name describes HOW not WHAT
- Verifying through external means instead of interface

```python
# BAD: Bypasses interface to verify
def test_save_writes_file(tmp_path):
    repo.save(dungeon, "test")
    raw = (tmp_path / "test.json").read_text()
    assert '"rooms"' in raw   # testing JSON internals

# GOOD: Verifies through interface
def test_save_makes_dungeon_loadable(tmp_path):
    repo = DungeonRepository(tmp_path)
    repo.save(dungeon, "test")
    loaded = repo.load("test")
    assert loaded == dungeon
```
