def test_repository_and_local_rag(tmp_path,monkeypatch):
    import src.core.database as database
    database.DB_PATH=tmp_path/"test.db"
    database.init_db()
    from src.core.repository import create_job,get_job,upsert_knowledge,search_knowledge
    job=create_job("demo.mp4")
    assert get_job(job)["status"]=="QUEUED"
    upsert_knowledge("guide","low confidence requires human review")
    assert search_knowledge("confidence review")
