import json
from datetime import UTC, datetime
from .database import connect

def now_iso():
    return datetime.now(UTC).isoformat()

def create_job(filename):
    import uuid
    job_id=str(uuid.uuid4())
    with connect() as db:
        db.execute("INSERT INTO jobs(id,filename,status,created_at) VALUES(?,?,?,?)",(job_id,filename,"QUEUED",now_iso()))
    return job_id

def update_job(job_id,status,**fields):
    allowed={"output_path","error","started_at","completed_at","progress"}
    fields={k:v for k,v in fields.items() if k in allowed}
    columns=["status=?"]+[k+"=?" for k in fields]
    with connect() as db: db.execute("UPDATE jobs SET "+",".join(columns)+" WHERE id=?", [status,*fields.values(),job_id])  # nosec B608

def get_job(job_id):
    with connect() as db: row=db.execute("SELECT * FROM jobs WHERE id=?",(job_id,)).fetchone()
    return dict(row) if row else None

def save_detection(detection,job_id=None):
    with connect() as db:
        cur=db.execute("""INSERT INTO detections(job_id,frame,track_id,label,confidence,x1,y1,x2,y2)
                          VALUES(?,?,?,?,?,?,?,?,?)""",(job_id,detection.frame,detection.track_id,detection.label,detection.confidence,*detection.bbox))
        return int(cur.lastrowid)

def list_detections(job_id=None):
    with connect() as db:
        rows=db.execute("SELECT * FROM detections WHERE job_id=? ORDER BY frame,id",(job_id,)).fetchall() if job_id else db.execute("SELECT * FROM detections ORDER BY frame,id").fetchall()
    return [dict(r) for r in rows]

def create_review(detection_id,reason):
    with connect() as db:
        cur=db.execute("INSERT INTO reviews(detection_id,status,reason,created_at) VALUES(?,?,?,?)",(detection_id,"PENDING",reason,now_iso()))
        return int(cur.lastrowid)

def list_reviews(status="PENDING"):
    with connect() as db:
        rows=db.execute("""SELECT r.*,d.frame,d.track_id,d.label,d.confidence,d.job_id
                           FROM reviews r JOIN detections d ON d.id=r.detection_id
                           WHERE r.status=? ORDER BY r.created_at""",(status,)).fetchall()
    return [dict(r) for r in rows]

def get_review(review_id):
    with connect() as db: row=db.execute("SELECT * FROM reviews WHERE id=?",(review_id,)).fetchone()
    return dict(row) if row else None

def decide_review(review_id,decision,reviewer="human",final_label=None):
    if decision not in {"APPROVED","REJECTED"}: raise ValueError("decision must be APPROVED or REJECTED")
    with connect() as db:
        if not db.execute("SELECT 1 FROM reviews WHERE id=?",(review_id,)).fetchone(): raise KeyError("review not found")
        db.execute("""UPDATE reviews SET status=?,decision=?,reviewer=?,final_label=?,reviewed_at=?
                      WHERE id=?""",(decision,decision,reviewer,final_label,now_iso(),review_id))
    return get_review(review_id)

def add_event(job_id,event_type,payload):
    with connect() as db:
        cur=db.execute("INSERT INTO events(job_id,event_type,payload,created_at) VALUES(?,?,?,?)",(job_id,event_type,json.dumps(payload,ensure_ascii=False),now_iso()))
        return int(cur.lastrowid)

def list_events(job_id=None):
    with connect() as db:
        rows=db.execute("SELECT * FROM events WHERE job_id=? ORDER BY created_at",(job_id,)).fetchall() if job_id else db.execute("SELECT * FROM events ORDER BY created_at").fetchall()
    return [dict(r) for r in rows]

def upsert_knowledge(source,content):
    with connect() as db:
        cur=db.execute("INSERT INTO knowledge(source,content,created_at) VALUES(?,?,?)",(source,content,now_iso()))
        return int(cur.lastrowid)

def search_knowledge(query,top_k=5):
    terms=[t.lower() for t in query.split() if len(t)>2][:12]
    with connect() as db: rows=db.execute("SELECT * FROM knowledge ORDER BY id DESC").fetchall()
    scored=[]
    for row in rows:
        hay=(str(row["source"])+" "+str(row["content"])).lower()
        score=sum(hay.count(term) for term in terms)
        if score: scored.append((score,dict(row)))
    scored.sort(key=lambda x:x[0],reverse=True)
    return [{"source":r["source"],"content":r["content"],"score":s} for s,r in scored[:top_k]]
