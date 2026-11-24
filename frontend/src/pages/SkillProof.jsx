import React, { useEffect, useState } from "react";
import { Award, BadgeCheck, BookOpen, CheckCircle2, ChevronLeft, ChevronRight, Clock3, LockKeyhole, Medal, RotateCcw, ShieldCheck, Sparkles, Target, Trophy, XCircle } from "lucide-react";
import { api } from "../api";

const SKILL_META = {
  Python: { icon: "Py", color: "#3478a8", description: "Language fundamentals, data structures, runtime behaviour and practical Python reasoning." },
  JavaScript: { icon: "JS", color: "#d5a51d", description: "Closures, promises, coercion, event flow and modern JavaScript semantics." },
  SQL: { icon: "DB", color: "#287f79", description: "Joins, aggregation, indexes, transactions and relational database reasoning." },
  React: { icon: "Re", color: "#2389a5", description: "Hooks, rendering, state, effects, reconciliation and component architecture." },
  "UI/UX Design": { icon: "UX", color: "#d7654d", description: "Research, usability, accessibility, responsive systems and design decisions." }
};

export default function SkillProof({ currentUser = {}, onProfileRefresh }) {
  const [catalog, setCatalog] = useState([]);
  const [attempts, setAttempts] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");
  const [quiz, setQuiz] = useState(null);
  const [answers, setAnswers] = useState({});
  const [index, setIndex] = useState(0);
  const [result, setResult] = useState(null);
  const [submitting, setSubmitting] = useState(false);
  const [tab, setTab] = useState("assessments");

  const refresh = async () => {
    setLoading(true); setError("");
    try {
      const [data, history] = await Promise.all([api.getSkillProofSkills(), api.getSkillProofAttempts()]);
      setCatalog(data.skills || []); setAttempts(history || []);
    } catch (e) { setError(e.message || "Could not load SkillProof data"); }
    finally { setLoading(false); }
  };
  useEffect(() => { refresh(); }, []);

  const startQuiz = async (skill) => {
    setError(""); setResult(null); setAnswers({}); setIndex(0);
    try { setQuiz(await api.getSkillProofQuiz(skill)); setTab("quiz"); }
    catch (e) { setError(e.message || "Could not start assessment"); }
  };
  const submit = async () => {
    if (Object.keys(answers).length !== 10) { setError("Please answer all 10 questions before submitting."); return; }
    setSubmitting(true); setError("");
    try {
      const data = await api.submitSkillProof(quiz.skill, answers);
      setResult(data); setQuiz(null); setTab("result"); await refresh(); if (onProfileRefresh) await onProfileRefresh();
    } catch (e) { setError(e.message || "Assessment could not be submitted"); }
    finally { setSubmitting(false); }
  };
  const activeQuestion = quiz?.questions?.[index];
  const verified = catalog.filter(s => s.verified).length;
  const bestScore = catalog.reduce((best, s) => Math.max(best, s.bestScore || 0), 0);

  return <main className="page-container skillproof-page">
    <section className="sp-hero">
      <div className="sp-hero-orbit sp-orbit-one"/><div className="sp-hero-orbit sp-orbit-two"/>
      <div className="sp-hero-copy">
        <span className="sp-kicker"><Sparkles size={15}/> LEARVIX SKILL INTELLIGENCE</span>
        <h1>Show what you<br/><em>can actually do.</em></h1>
        <p>Take a challenging 10-question assessment. Earn evidence-backed skill badges and build a profile people can trust.</p>
        <div className="sp-hero-stats"><span><strong>{catalog.length || 5}</strong> skill tracks</span><span><strong>10</strong> questions each</span><span><strong>80%</strong> pass score</span></div>
      </div>
      <div className="sp-hero-art"><div className="sp-score-ring"><div><ShieldCheck size={34}/><strong>{verified}</strong><small>VERIFIED</small></div></div><div className="sp-floating-chip chip-top"><BadgeCheck size={16}/> Evidence based</div><div className="sp-floating-chip chip-bottom"><Trophy size={16}/> SkillProof badge</div></div>
    </section>

    <section className="sp-trust-strip">
      <div><ShieldCheck/><span><b>Assessment verified</b><small>Badge earned at 80% or above</small></span></div>
      <div><LockKeyhole/><span><b>Fair scoring</b><small>Answers evaluated securely on the server</small></span></div>
      <div><Target/><span><b>Clear evidence</b><small>Review score and explanations after each attempt</small></span></div>
    </section>

    {error && <div className="sp-error" role="alert">{error}</div>}

    <div className="sp-tabs">
      <button className={tab !== "history" ? "active" : ""} onClick={() => { setTab("assessments"); setQuiz(null); setResult(null); }}>Skill assessments</button>
      <button className={tab === "history" ? "active" : ""} onClick={() => { setTab("history"); setQuiz(null); setResult(null); }}>My results <span>{attempts.length}</span></button>
    </div>

    {loading ? <div className="sp-loading">Loading your SkillProof profile…</div> : null}

    {!loading && tab === "assessments" && !quiz && !result && <>
      <div className="sp-section-heading"><div><span className="sp-overline">CHOOSE YOUR CHALLENGE</span><h2>Five skills. Real proof.</h2><p>Each assessment contains 10 advanced questions. You need 8 correct answers to earn a verified badge.</p></div><div className="sp-best-score"><span>YOUR BEST SCORE</span><strong>{bestScore}%</strong></div></div>
      <div className="sp-skill-grid">{catalog.map((item) => { const meta = SKILL_META[item.name] || {}; return <article className="sp-skill-card" key={item.name}>
        <div className="sp-skill-card-top"><span className="sp-skill-icon" style={{ "--skill-color": meta.color }}>{meta.icon}</span>{item.verified ? <span className="sp-verified-pill"><BadgeCheck size={14}/> Verified</span> : <span className="sp-question-count">10 QUESTIONS</span>}</div>
        <h3>{item.name}</h3><p>{meta.description}</p>
        <div className="sp-skill-meta"><span><BookOpen size={14}/> Advanced level</span><span><Clock3 size={14}/> ~12 min</span></div>
        {item.bestScore !== null && item.bestScore !== undefined ? <div className="sp-best-line"><span>Best attempt</span><b>{item.bestScore}%</b></div> : <div className="sp-best-line"><span>No attempts yet</span><b>—</b></div>}
        <button className="sp-start-btn" onClick={() => startQuiz(item.name)}>{item.verified ? "Retake assessment" : "Start assessment"}<ChevronRight size={17}/></button>
      </article>; })}</div>
      <div className="sp-member-banner"><div className="sp-member-icon"><Medal size={25}/></div><div><h3>{currentUser.trustedMember || verified > 0 ? "You're building a trusted profile" : "Your path to Trusted Member starts here"}</h3><p>Pass at least one SkillProof assessment with 80% or higher to earn a verified skill badge and Trusted Member status.</p></div><span className="sp-member-status">{currentUser.trustedMember || verified > 0 ? "TRUSTED MEMBER" : "NOT YET VERIFIED"}</span></div>
    </>}

    {quiz && activeQuestion && <section className="sp-quiz-panel">
      <div className="sp-quiz-top"><button className="sp-back-btn" onClick={() => { setQuiz(null); setTab("assessments"); }}><ChevronLeft size={17}/> Exit assessment</button><span>{quiz.skill} <b>· Advanced</b></span></div>
      <div className="sp-quiz-progress"><div style={{ width: `${(Object.keys(answers).length / 10) * 100}%` }}/></div>
      <div className="sp-quiz-meta"><span>QUESTION {index + 1} <small>OF 10</small></span><span>{Object.keys(answers).length}/10 answered</span></div>
      <h2>{activeQuestion.question}</h2>
      <div className="sp-options">{activeQuestion.options.map((option, i) => <button key={i} className={`sp-option ${answers[activeQuestion.id] === i ? "selected" : ""}`} onClick={() => setAnswers(prev => ({ ...prev, [activeQuestion.id]: i }))}><span className="sp-option-letter">{String.fromCharCode(65 + i)}</span><span>{option}</span>{answers[activeQuestion.id] === i && <CheckCircle2 size={19}/>}</button>)}</div>
      <div className="sp-quiz-footer"><button className="sp-secondary-btn" disabled={index === 0} onClick={() => setIndex(i => i - 1)}><ChevronLeft size={17}/> Previous</button>{index < 9 ? <button className="sp-primary-btn" onClick={() => setIndex(i => i + 1)}>Next question <ChevronRight size={17}/></button> : <button className="sp-primary-btn" disabled={submitting || Object.keys(answers).length !== 10} onClick={submit}>{submitting ? "Scoring…" : "Submit assessment"}<ShieldCheck size={17}/></button>}</div>
      <p className="sp-quiz-note"><LockKeyhole size={13}/> Your answers are scored securely. You can review explanations after submission.</p>
    </section>}

    {result && <section className="sp-result-panel">
      <div className={`sp-result-icon ${result.attempt.passed ? "passed" : "not-passed"}`}>{result.attempt.passed ? <Trophy size={35}/> : <Target size={35}/>}</div>
      <span className="sp-overline">ASSESSMENT COMPLETE</span><h2>{result.attempt.passed ? "Skill verified." : "Keep building your proof."}</h2>
      <div className="sp-result-score">{result.attempt.score}<small>/100</small></div>
      <p>{result.message}</p>
      {result.trustedMember && <div className="sp-trusted-earned"><BadgeCheck/> Trusted Member status unlocked</div>}
      <div className="sp-answer-review"><h3>Answer review</h3>{result.details.map((d, i) => <div className="sp-review-row" key={d.id}><span className={d.isCorrect ? "correct" : "incorrect"}>{d.isCorrect ? <CheckCircle2 size={17}/> : <XCircle size={17}/>}</span><div><b>{i + 1}. {d.question}</b><p>Correct answer: {d.correctOption}</p><small>{d.explanation}</small></div></div>)}</div>
      <div className="sp-result-actions"><button className="sp-primary-btn" onClick={() => { setResult(null); setTab("assessments"); }}>Back to skills</button><button className="sp-secondary-btn" onClick={() => startQuiz(result.attempt.skill)}><RotateCcw size={16}/> Retake quiz</button></div>
    </section>}

    {tab === "history" && !quiz && !result && <section className="sp-history"><div className="sp-section-heading"><div><span className="sp-overline">YOUR PROGRESS</span><h2>Assessment history</h2><p>Every submitted attempt is saved to your Learvix account.</p></div></div>{attempts.length ? attempts.map(a => <div className="sp-history-row" key={a.id}><div className="sp-history-icon"><Award/></div><div className="sp-history-name"><b>{a.skill}</b><small>{new Date(a.createdAt).toLocaleString()}</small></div><strong>{a.score}%</strong><span className={a.passed ? "sp-verified-pill" : "sp-question-count"}>{a.passed ? "Verified" : "Not yet verified"}</span></div>) : <div className="sp-empty"><Trophy size={32}/><h3>No assessments yet</h3><p>Complete your first skill assessment to start building your proof.</p><button className="sp-primary-btn" onClick={() => setTab("assessments")}>Explore assessments</button></div>}</section>}
  </main>;
}
