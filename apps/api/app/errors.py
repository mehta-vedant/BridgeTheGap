"""Structured domain errors.

An error a user sees is part of the product, not an accident of it.  Two rules:

**1. Every error says what to do next.**  A refusal without a remediation is a
dead end.  Gujarat's own instruments already work this way -- the land-readiness
evaluation says possession is 72% against a 90% threshold and names the
handover memorandum as the missing artefact (research record sec 2.5.2), and the
black-spot resolution names the distance, the accident count, the deadline and
the reporting interval (sec 4A).

**2. Every error cites the record that justifies it.**  The ``reference`` field
points at a section of ``docs/research_3phase_opencode.md``.  That is what stops
a plausible-but-wrong rule from being written into an error message and shipped.
If there is no source, the honest answer is a 501-shaped ``NOT_ESTABLISHED``,
not an invented rule.
"""

from __future__ import annotations

from typing import Any

from fastapi import HTTPException, Request, status
from fastapi.responses import JSONResponse


class DomainError(HTTPException):
    """An HTTP error that carries a machine code and a remediation.

    Subclasses ``HTTPException`` so existing handlers keep working, but the
    registered exception handler renders the full structured body.
    """

    def __init__(
        self,
        status_code: int,
        code: str,
        message: str,
        detail: str | None = None,
        remediation: list[str] | None = None,
        reference: str | None = None,
    ) -> None:
        super().__init__(status_code=status_code, detail=message)
        self.code = code
        self.message = message
        self.detail = detail
        self.remediation = remediation or []
        self.reference = reference

    def body(self) -> dict[str, Any]:
        payload: dict[str, Any] = {"code": self.code, "message": self.message}
        if self.detail:
            payload["detail"] = self.detail
        if self.remediation:
            payload["remediation"] = self.remediation
        if self.reference:
            payload["reference"] = self.reference
        return {"error": payload}


# --------------------------------------------------------------------------
# Reusable domain errors
# --------------------------------------------------------------------------


def gate_blocked(explanation: str, missing: list[str], reference: str) -> DomainError:
    return DomainError(
        status_code=status.HTTP_409_CONFLICT,
        code="GATE_NOT_PASSED",
        message="This action is blocked by a recorded gate evaluation.",
        detail=explanation,
        remediation=missing or ["Resolve the recorded shortfall, then re-evaluate the gate."],
        reference=reference,
    )


def role_denied(allowed: list[str], reference: str) -> DomainError:
    return DomainError(
        status_code=status.HTTP_403_FORBIDDEN,
        code="ROLE_NOT_PERMITTED",
        message="Your assigned role cannot perform this action.",
        detail="This action is reserved for: " + ", ".join(allowed) + ".",
        remediation=[
            "Sign in with a demo account that holds one of those roles.",
            "Roles are assigned per person and per organisation unit; they are not inferred from the UI.",
        ],
        reference=reference,
    )


def not_visible(what: str, reference: str) -> DomainError:
    return DomainError(
        status_code=status.HTTP_403_FORBIDDEN,
        code="NOT_IN_YOUR_SCOPE",
        message=f"You do not have visibility of this {what}.",
        detail=(
            "The query that would return this record is restricted by your role, so the record "
            "was never read. This is not a display filter."
        ),
        remediation=[
            "A contractor sees only bridges where its own company holds a contract or work order.",
            "Inspectors, quality and finance see only bridges that have been awarded.",
        ],
        reference=reference,
    )


def wrong_phase(current: str, attempted: str, blockers: list[str], reference: str) -> DomainError:
    return DomainError(
        status_code=status.HTTP_409_CONFLICT,
        code="PHASE_NOT_REACHED",
        message=f"This bridge is in {current.replace('_', ' ').title()}, so {attempted} does not apply to it yet.",
        detail=(
            "The lifecycle phase is derived from the records that exist for this bridge, not stored "
            "on it, so a bridge cannot be treated as further along than it actually is."
        ),
        remediation=blockers or ["No outstanding requirement is recorded against this transition."],
        reference=reference,
    )


def rule_violation(code: str, message: str, detail: str, remediation: list[str], reference: str) -> DomainError:
    return DomainError(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        code=code,
        message=message,
        detail=detail,
        remediation=remediation,
        reference=reference,
    )


def not_established(what: str, searched: str) -> DomainError:
    """The honest answer when a rule genuinely does not exist in the record.

    Refusing to compute is the correct behaviour.  Guessing a threshold and
    presenting it as a requirement is the failure mode the research record was
    written to prevent.
    """
    return DomainError(
        status_code=status.HTTP_501_NOT_IMPLEMENTED,
        code="NOT_ESTABLISHED",
        message=f"{what} is not established, so this is not computed.",
        detail=(
            "No source was found for this value. It is not inferred from general practice and not "
            "filled from another department's rules without saying so."
        ),
        remediation=[f"Recorded gap. What was searched: {searched}"],
        reference="docs/research_3phase_opencode.md §6 THE `NOT ESTABLISHED` REGISTER",
    )


def conflict(message: str, remediation: list[str] | None = None) -> DomainError:
    return DomainError(
        status_code=status.HTTP_409_CONFLICT,
        code="CONFLICT",
        message=message,
        remediation=remediation or [],
    )


def invalid(message: str, remediation: list[str] | None = None) -> DomainError:
    return DomainError(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        code="INVALID_INPUT",
        message=message,
        remediation=remediation or [],
    )


def missing(message: str, remediation: list[str] | None = None) -> DomainError:
    return DomainError(
        status_code=status.HTTP_404_NOT_FOUND,
        code="NOT_FOUND",
        message=message,
        remediation=remediation or [],
    )


# --------------------------------------------------------------------------
# Handler
# --------------------------------------------------------------------------


async def domain_error_handler(_request: Request, exc: DomainError) -> JSONResponse:
    return JSONResponse(status_code=exc.status_code, content=exc.body())
