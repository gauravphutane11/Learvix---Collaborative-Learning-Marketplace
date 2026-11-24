import React, { useEffect, useState } from "react";
import { Plus, X, Save, Award, Edit2, ShieldCheck, Camera, BadgeCheck, UserRound } from "lucide-react";
import { popularSkills } from "../data/staticData";

export default function Profile({ currentUser = {}, updateUser }) {
  const [isEditing, setIsEditing] = useState(false);
  const [saving, setSaving] = useState(false);
  const [formData, setFormData] = useState({ name: currentUser.name || "", bio: currentUser.bio || "", profileImage: currentUser.profileImage || null, skillsOffered: [...(currentUser.skillsOffered || [])], skillsWanted: [...(currentUser.skillsWanted || [])] });
  const [newSkillOffered, setNewSkillOffered] = useState("");
  const [newSkillWanted, setNewSkillWanted] = useState("");
  useEffect(() => setFormData({ name: currentUser.name || "", bio: currentUser.bio || "", profileImage: currentUser.profileImage || null, skillsOffered: [...(currentUser.skillsOffered || [])], skillsWanted: [...(currentUser.skillsWanted || [])] }), [currentUser]);

  const handlePhoto = (event) => {
    const file = event.target.files?.[0]; if (!file) return;
    if (!["image/jpeg", "image/png", "image/webp"].includes(file.type)) { alert("Choose a JPG, PNG or WEBP image."); return; }
    if (file.size > 450 * 1024) { alert("Please choose an image smaller than 450 KB."); return; }
    const reader = new FileReader(); reader.onload = () => setFormData(prev => ({ ...prev, profileImage: reader.result })); reader.readAsDataURL(file);
  };
  const handleSave = async () => { setSaving(true); try { await updateUser(formData); setIsEditing(false); } finally { setSaving(false); } };
  const addSkill = (type) => { const skill = type === "offered" ? newSkillOffered : newSkillWanted; const key = type === "offered" ? "skillsOffered" : "skillsWanted"; if (skill && !formData[key].includes(skill)) setFormData(prev => ({ ...prev, [key]: [...prev[key], skill] })); if (type === "offered") setNewSkillOffered(""); else setNewSkillWanted(""); };
  const removeSkill = (key, skill) => setFormData(prev => ({ ...prev, [key]: prev[key].filter(item => item !== skill) }));
  const avatar = formData.profileImage ? <img src={formData.profileImage} alt="Profile" className="sp-profile-photo"/> : <span>{(formData.name || "Learner").split(" ").map(n => n[0]).join("").slice(0,2).toUpperCase()}</span>;

  return <main className="page-container profile-page">
    <section className="profile-hero"><div><span className="sp-overline">YOUR LEARVIX IDENTITY</span><h1>Profile & reputation</h1><p>Show your strengths, learning goals and verified skills to the community.</p></div><div className="profile-hero-mark"><UserRound size={38}/></div></section>
    <div className="profile-layout">
      <section className="profile-identity-card">
        <div className="profile-photo-wrap"><div className="profile-photo-large">{avatar}</div>{isEditing && <label className="profile-photo-edit" title="Upload profile photo"><Camera size={17}/><input type="file" accept="image/png,image/jpeg,image/webp" onChange={handlePhoto}/></label>}</div>
        {isEditing ? <input className="form-input profile-name-input" value={formData.name} maxLength={80} onChange={e => setFormData(p => ({ ...p, name: e.target.value }))} aria-label="Name"/> : <h2>{currentUser.name || "Learvix Member"}</h2>}
        <p className="profile-email">{currentUser.email}</p>
        <div className="profile-statuses">{(currentUser.verifiedSkills || []).length > 0 ? <span className="profile-status verified"><BadgeCheck size={14}/> SkillProof verified</span> : <span className="profile-status"><ShieldCheck size={14}/> Member</span>}{currentUser.trustedMember && <span className="profile-status trusted"><Award size={14}/> Trusted Member</span>}</div>
        <div className="profile-reputation"><div><strong>{currentUser.rating || "—"}</strong><small>Community rating</small></div><div><strong>{currentUser.completedExchanges || 0}</strong><small>Exchanges completed</small></div></div>
        {isEditing && <p className="profile-photo-help">Upload JPG, PNG or WEBP · maximum 450 KB</p>}
        <div className="profile-actions">{!isEditing ? <button className="sp-primary-btn" onClick={() => setIsEditing(true)}><Edit2 size={16}/> Edit profile</button> : <><button className="sp-secondary-btn" onClick={() => { setIsEditing(false); setFormData({ name: currentUser.name || "", bio: currentUser.bio || "", profileImage: currentUser.profileImage || null, skillsOffered: [...(currentUser.skillsOffered || [])], skillsWanted: [...(currentUser.skillsWanted || [])] }); }}>Cancel</button><button className="sp-primary-btn" disabled={saving} onClick={handleSave}><Save size={16}/>{saving ? "Saving…" : "Save changes"}</button></>}</div>
      </section>
      <section className="profile-details">
        <article className="profile-detail-card"><div className="profile-detail-heading"><div><span className="sp-overline">INTRODUCTION</span><h3>About me</h3></div></div>{isEditing ? <textarea className="form-input profile-bio-input" maxLength={500} value={formData.bio} onChange={e => setFormData(p => ({ ...p, bio: e.target.value }))} placeholder="Tell the community what you enjoy learning and teaching…"/> : <p className="profile-bio">{currentUser.bio || "Add a short introduction to help other learners connect with you."}</p>}</article>
        {[{key:"skillsOffered",title:"Skills I can teach",desc:"Share the knowledge you can offer.",color:"teach",state:newSkillOffered,set:setNewSkillOffered},{key:"skillsWanted",title:"Skills I want to learn",desc:"Tell the community what you want to explore.",color:"learn",state:newSkillWanted,set:setNewSkillWanted}].map(group => <article className={`profile-detail-card ${group.color}`} key={group.key}><div className="profile-detail-heading"><div><span className="sp-overline">{group.color === "teach" ? "SHARE KNOWLEDGE" : "GROW YOURSELF"}</span><h3>{group.title}</h3><p>{group.desc}</p></div><strong className="profile-skill-count">{formData[group.key].length}</strong></div><div className="profile-skill-list">{formData[group.key].length ? formData[group.key].map(skill => <span className="profile-skill-chip" key={skill}>{skill}{isEditing && <button onClick={() => removeSkill(group.key, skill)} aria-label={`Remove ${skill}`}><X size={13}/></button>}</span>) : <span className="profile-no-skills">No skills added yet.</span>}</div>{isEditing && <div className="profile-skill-add"><select className="form-input" value={group.state} onChange={e => group.set(e.target.value)}><option value="">Choose a skill…</option>{popularSkills.filter(skill => !formData[group.key].includes(skill)).map(skill => <option key={skill}>{skill}</option>)}</select><button className="sp-primary-btn" disabled={!group.state} onClick={() => addSkill(group.color === "teach" ? "offered" : "wanted")}><Plus size={16}/> Add</button></div>}</article>)}
        <article className="profile-detail-card"><div className="profile-detail-heading"><div><span className="sp-overline">PROOF OF ABILITY</span><h3>Verified skills</h3><p>Skills you passed with 80% or higher in SkillProof.</p></div><BadgeCheck className="profile-verified-icon"/></div><div className="profile-skill-list">{(currentUser.verifiedSkills || []).length ? currentUser.verifiedSkills.map(skill => <span className="profile-skill-chip verified-chip" key={skill}><BadgeCheck size={14}/>{skill}</span>) : <span className="profile-no-skills">No verified skills yet. Complete a SkillProof assessment to earn your first badge.</span>}</div></article>
      </section>
    </div>
  </main>;
}
