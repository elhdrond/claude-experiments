# Spec: [Feature Name]

> **Status:** Draft | In Review | Approved | Implemented
> **Date:** YYYY-MM-DD
> **Author:** elhdrond

---

## 1. Goal

_One sentence: what problem does this solve and for whom._

---

## 2. Actors

| Actor | Description |
|-------|-------------|
| User | |
| Admin | |
| System | |

_Remove rows that do not apply._

---

## 3. Functional Requirements

| ID | Requirement | Priority |
|----|-------------|----------|
| FR-01 | The system shall… | Must |
| FR-02 | The system shall… | Should |
| FR-03 | The system shall… | Could |

**Priority levels:** Must (non-negotiable) · Should (important) · Could (nice to have)

---

## 4. Non-Functional Requirements

| ID | Requirement | Metric |
|----|-------------|--------|
| NFR-01 | Performance: … | e.g. response < 500ms |
| NFR-02 | Security: … | e.g. no unauthenticated access |
| NFR-03 | Scalability: … | e.g. handles N concurrent users |

---

## 5. Data Model

```
Entity: [Name]
- field_name: type (constraints)
- field_name: type (FK → OtherEntity.id)

Entity: [Name]
- field_name: type (constraints)
```

_Or paste an ER diagram / SQL DDL if preferred._

---

## 6. Acceptance Criteria

```
Scenario: [Name]
  Given [initial context]
  When  [action is taken]
  Then  [expected outcome]
```

```
Scenario: [Edge case name]
  Given [initial context]
  When  [edge case action]
  Then  [expected outcome]
```

_Add one scenario per FR. Add extra scenarios for edge cases and error paths._

---

## 7. Out of Scope

- [Explicitly list what this feature does NOT include]
- [This prevents scope creep and misunderstandings]

---

## 8. Open Questions

- [ ] Question 1
- [ ] Question 2

_Remove this section once all questions are resolved before implementation starts._

---

## 9. Implementation Notes

_Filled in after approval — not before. Claude can suggest this section during implementation._

- Suggested approach:
- Files to create/modify:
- Dependencies:
