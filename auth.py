"""Optional shared-password gate.

Deliberately opt-in: with no password configured this is a no-op, so running
locally or screen-sharing the demo stays friction-free. Set CEPH_PASSWORD (env
or Streamlit secrets) and the app refuses to render until it is entered.

This is a demo door, not an identity system. It gives one shared secret to a
room of people and knows nothing about who they are, so it cannot attribute an
Approve/Reject to a person. Before this console drives real shipments, replace
it with proper SSO — Streamlit's native st.login() OIDC, or an authenticating
proxy in front of the app.
"""

from __future__ import annotations

import hmac
import os

import streamlit as st


def _configured_password() -> str:
    password = os.environ.get("CEPH_PASSWORD", "")
    if not password:
        try:
            password = st.secrets.get("CEPH_PASSWORD", "")  # type: ignore[assignment]
        except Exception:
            password = ""
    return str(password)


def require_password() -> None:
    """Halt the script until the shared password is entered. No-op when unset."""
    expected = _configured_password()
    if not expected:
        return
    if st.session_state.get("auth_ok"):
        return

    st.markdown("#### DSV Ceph AI")
    entered = st.text_input("Access code", type="password")
    if entered:
        # compare_digest keeps the check from leaking length/prefix via timing
        if hmac.compare_digest(entered, expected):
            st.session_state["auth_ok"] = True
            st.rerun()
        else:
            st.caption("Not recognised.")
    st.stop()
