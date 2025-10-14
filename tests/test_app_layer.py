# tests/test_app_layer.py
from __future__ import annotations
from automation_backup_cli import app as app_module
from automation_backup_cli.domain.models import BackupResult

def test_run_backup_job_calls_setup_and_service(monkeypatch, tmp_path):
    called = {"setup": False, "service": False}

    def fake_setup_logging(verbose: bool = False):
        called["setup"] = True

    def fake_execute_backup(job):
        called["service"] = True
        br = BackupResult()
        br.files_planned = ["x"]
        return br

    monkeypatch.setattr(app_module, "setup_logging", fake_setup_logging)
    monkeypatch.setattr(app_module, "execute_backup", fake_execute_backup)

    res = app_module.run_backup_job(
        source=str(tmp_path),
        destination=str(tmp_path),
        exclude_patterns=[],
        compress_format=None,
        dry_run=True,
        verbose=True,
    )
    assert called["setup"] and called["service"]
    assert res.files_planned == ["x"]
